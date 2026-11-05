"""WebSocket endpoints: admin alert stream and per-device session channel."""
from __future__ import annotations

import logging

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from starlette.concurrency import run_in_threadpool

from app.core.constants import ROLE_ADMIN
from app.core.deps import authenticate_token
from app.core.exceptions import AppError
from app.core.websocket_manager import ws_manager
from app.database import SessionLocal

router = APIRouter(prefix="/ws", tags=["websocket"])
logger = logging.getLogger("exampro.ws")

WS_UNAUTHORIZED = 4401
WS_FORBIDDEN = 4403


def _auth(token: str) -> tuple[str, str]:
    """Validate the JWT + server-side session; return ``(role, device_id)`` as plain values."""
    with SessionLocal() as db:
        ctx = authenticate_token(db, token)
        return ctx.user.role, ctx.session.device_id


async def _authenticate(ws: WebSocket, token: str | None) -> tuple[str, str] | None:
    if not token:
        await ws.close(code=WS_UNAUTHORIZED)
        return None
    try:
        return await run_in_threadpool(_auth, token)
    except AppError:
        await ws.close(code=WS_UNAUTHORIZED)
        return None


async def _hold_open(ws: WebSocket) -> None:
    """Keep the socket alive; answer client pings. Server-to-client pushes happen via ws_manager."""
    while True:
        message = await ws.receive_text()
        if message == "ping":
            await ws.send_text("pong")


@router.websocket("/admin")
async def admin_stream(ws: WebSocket, token: str | None = None) -> None:
    identity = await _authenticate(ws, token)
    if identity is None:
        return
    if identity[0] != ROLE_ADMIN:
        await ws.close(code=WS_FORBIDDEN)
        return
    await ws_manager.connect_admin(ws)
    try:
        await _hold_open(ws)
    except WebSocketDisconnect:
        pass
    finally:
        await ws_manager.disconnect(ws)


@router.websocket("/session/{device_id}")
async def session_channel(ws: WebSocket, device_id: str, token: str | None = None) -> None:
    identity = await _authenticate(ws, token)
    if identity is None:
        return
    if identity[1] != device_id:
        await ws.close(code=WS_FORBIDDEN)
        return
    await ws_manager.connect_session(device_id, ws)
    try:
        await _hold_open(ws)
    except WebSocketDisconnect:
        pass
    finally:
        await ws_manager.disconnect(ws, device_id)
