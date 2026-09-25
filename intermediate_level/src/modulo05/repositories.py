# src/modulo05/repositories.py
import sqlite3

from ..modulo05.contracts import UserDTO


class InMemoryUserRepository:
    """Implementación de persistencia en memoria (para pruebas rápidas)."""

    def __init__(self) -> None:
        self._users: dict[str, UserDTO] = {}

    def save(self, user_id: str, email: str, name: str) -> UserDTO:
        user: UserDTO = {"user_id": user_id, "email": email, "name": name}
        self._users[user_id] = user
        return user

    def find_by_id(self, user_id: str) -> UserDTO | None:
        return self._users.get(user_id)

    def find_by_email(self, email: str) -> UserDTO | None:
        for user in self._users.values():
            if user["email"] == email:
                return user
        return None


class SQLiteUserRepository:
    """Implementación de persistencia real utilizando SQLite."""

    def __init__(
        self, db_path: str = ":memory:", connection: sqlite3.Connection | None = None
    ) -> None:
        self.db_path = db_path
        self._conn = connection or sqlite3.connect(self.db_path)
        self._conn.row_factory = sqlite3.Row
        self._init_db()

    def _init_db(self) -> None:
        with self._conn:
            self._conn.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY,
                    email TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL
                )
                """
            )

    def save(self, user_id: str, email: str, name: str) -> UserDTO:
        with self._conn:
            self._conn.execute(
                "INSERT INTO users (user_id, email, name) VALUES (?, ?, ?)",
                (user_id, email, name),
            )
        return {"user_id": user_id, "email": email, "name": name}

    def find_by_id(self, user_id: str) -> UserDTO | None:
        cursor = self._conn.execute(
            "SELECT user_id, email, name FROM users WHERE user_id = ?",
            (user_id,),
        )
        row = cursor.fetchone()
        if row:
            return {
                "user_id": row["user_id"],
                "email": row["email"],
                "name": row["name"],
            }
        return None

    def find_by_email(self, email: str) -> UserDTO | None:
        cursor = self._conn.execute(
            "SELECT user_id, email, name FROM users WHERE email = ?",
            (email,),
        )
        row = cursor.fetchone()
        if row:
            return {
                "user_id": row["user_id"],
                "email": row["email"],
                "name": row["name"],
            }
        return None
