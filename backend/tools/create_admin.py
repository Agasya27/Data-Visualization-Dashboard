import argparse
import os
import sys

# Ensure project root is on sys.path so 'backend' package can be imported
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.app.core.database import SessionLocal
from backend.app.models.user import User, UserRole
from backend.app.core.security import get_password_hash


def upsert_admin(email: str, password: str, username: str, overwrite: bool = False):
    s = SessionLocal()
    try:
        admin_exists = s.query(User).filter(User.role == UserRole.ADMIN).first()
        user = s.query(User).filter((User.email == email) | (User.username == username)).first()

        if user:
            user.role = UserRole.ADMIN
            if overwrite:
                user.password_hash = get_password_hash(password)
            s.commit()
            return f"Promoted existing user to Admin: email={user.email}, username={user.username}, overwrite={overwrite}"

        # If no user, create one; if an Admin already exists, still allow creating another Admin explicitly
        new_user = User(
            username=username,
            email=email,
            password_hash=get_password_hash(password),
            role=UserRole.ADMIN,
        )
        s.add(new_user)
        s.commit()
        return f"Created Admin user: email={email}, username={username}"
    finally:
        s.close()


def main():
    p = argparse.ArgumentParser(description="Create or promote an Admin user.")
    p.add_argument("--email", required=True)
    p.add_argument("--password", required=True)
    p.add_argument("--username", default="admin")
    p.add_argument("--overwrite", action="store_true", help="Overwrite password if user exists")
    args = p.parse_args()
    msg = upsert_admin(args.email, args.password, args.username, args.overwrite)
    print(msg)


if __name__ == "__main__":
    main()
