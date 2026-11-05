"""Create (or reset the password of) a user from the command line.

    python -m scripts.create_admin --email admin@exampro.io --name "Admin" --password "Str0ng!pass" --role ADMIN
    python -m scripts.create_admin --demo          # admin@exampro.io / student@exampro.io with demo passwords
"""
from __future__ import annotations

import argparse

from sqlalchemy import select

from app.core.security import hash_password
from app.database import SessionLocal
from app.models import User

DEMO = [
    ("Admin", "admin@exampro.io", "Admin@12345", "ADMIN"),
    ("Demo Student", "student@exampro.io", "Student@12345", "STUDENT"),
]


def upsert(name: str, email: str, password: str, role: str) -> str:
    with SessionLocal() as db:
        user = db.scalar(select(User).where(User.email == email.lower()))
        if user is None:
            db.add(User(name=name, email=email.lower(), hashed_password=hash_password(password), role=role, is_active=True))
            action = "created"
        else:
            user.hashed_password, user.role, user.name, user.is_active = hash_password(password), role, name, True
            action = "updated"
        db.commit()
    return f"{action}: {email} ({role})"


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--email"), p.add_argument("--name", default="Admin"), p.add_argument("--password")
    p.add_argument("--role", default="ADMIN", choices=["ADMIN", "INSTRUCTOR", "STUDENT"])
    p.add_argument("--demo", action="store_true", help="create the demo admin and student (development only!)")
    args = p.parse_args()
    if args.demo:
        for row in DEMO:
            print(upsert(*row))
        return
    if not (args.email and args.password):
        p.error("--email and --password are required (or use --demo)")
    if len(args.password) < 8:
        p.error("password must be at least 8 characters")
    print(upsert(args.name, args.email, args.password, args.role))


if __name__ == "__main__":
    main()
