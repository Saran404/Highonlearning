"""In-process WebSocket registry.

* ``admin_connections``   - every connected admin dashboard (receives alerts).
* ``session_connections`` - one socket per *device* (receives ``SESSION_REVOKED``).

Sync endpoints run in a worker thread, so services call the thread-safe ``publish_*`` helpers,
which schedule the coroutine on the event loop captured at start-up.

NOTE: state lives in process memory. If you run several Uvicorn workers/containers, put a
Redis pub/sub (or similar) behind ``broadcast_to_admins`` / ``notify_device`` so events reach
sockets held by other workers.
"""
from __future__ import annotations

import asyncio
import logging
from typing import Any

from fastapi import WebSocket

logger = logging.getLogger("exampro.ws")


class WebSocketManager:
    def __init__(self) -> None:
        self.admin_connections: list[WebSocket] = []
        self.session_connections: dict[str, WebSocket] = {}
        self._loop: asyncio.AbstractEventLoop | None = None

    # ---- lifecycle ---------------------------------------------------------------
    def bind_loop(self, loop: asyncio.AbstractEventLoop) -> None:
        """Remember the server event loop so threads can publish events."""
        self._loop = loop

    async def connect_admin(self, ws: WebSocket) -> None:
        await ws.accept()
        self.admin_connections.append(ws)

    async def connect_session(self, device_id: str, ws: WebSocket) -> None:
        await ws.accept()
        previous = self.session_connections.get(device_id)
        self.session_connections[device_id] = ws
        if previous is not None and previous is not ws:
            try:
                await previous.close(code=1000)
            except Exception:  # noqa: BLE001 - already closed
                pass

    async def disconnect(self, ws: WebSocket, device_id: str | None = None) -> None:
        if ws in self.admin_connections:
            self.admin_connections.remove(ws)
        if device_id and self.session_connections.get(device_id) is ws:
            del self.session_connections[device_id]

    # ---- sending -----------------------------------------------------------------
    async def broadcast_to_admins(self, event: dict[str, Any]) -> None:
        for ws in list(self.admin_connections):
            try:
                await ws.send_json(event)
            except Exception:  # noqa: BLE001 - dead socket
                await self.disconnect(ws)

    async def notify_device(self, device_id: str, event: dict[str, Any]) -> None:
        ws = self.session_connections.get(device_id)
        if ws is None:
            return
        try:
            await ws.send_json(event)
        except Exception:  # noqa: BLE001
            await self.disconnect(ws, device_id)

    # ---- thread-safe entry points (used by sync services) ------------------------
    def _submit(self, coro: Any) -> None:
        if self._loop is None or self._loop.is_closed():
            coro.close()
            return
        asyncio.run_coroutine_threadsafe(coro, self._loop)

    def publish_admin(self, event: dict[str, Any]) -> None:
        """Broadcast ``event`` to admins from any thread; never raises."""
        try:
            self._submit(self.broadcast_to_admins(event))
        except Exception:  # noqa: BLE001
            logger.exception("publish_admin failed")

    def publish_device(self, device_id: str, event: dict[str, Any]) -> None:
        """Push ``event`` to one device from any thread; never raises."""
        try:
            self._submit(self.notify_device(device_id, event))
        except Exception:  # noqa: BLE001
            logger.exception("publish_device failed")


ws_manager = WebSocketManager()
