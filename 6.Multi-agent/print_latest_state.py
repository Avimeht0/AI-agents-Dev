#!/usr/bin/env python3
import argparse
import json
import sqlite3
import sys
from typing import Optional


def fetch_latest_state(
    conn: sqlite3.Connection,
    source: str = "sessions",
    app_name: Optional[str] = None,
    user_id: Optional[str] = None,
    session_id: Optional[str] = None,
):
    if source not in {"sessions", "user_states"}:
        raise ValueError("source must be 'sessions' or 'user_states'")

    cur = conn.cursor()

    if source == "sessions":
        base = "SELECT app_name, user_id, id as session_id, state, update_time FROM sessions"
        where = []
        params = []
        if app_name:
            where.append("app_name = ?")
            params.append(app_name)
        if user_id:
            where.append("user_id = ?")
            params.append(user_id)
        if session_id:
            where.append("id = ?")
            params.append(session_id)
        sql = base + (" WHERE " + " AND ".join(where) if where else "") + " ORDER BY update_time DESC LIMIT 1"
    else:
        base = "SELECT app_name, user_id, state, update_time FROM user_states"
        where = []
        params = []
        if app_name:
            where.append("app_name = ?")
            params.append(app_name)
        if user_id:
            where.append("user_id = ?")
            params.append(user_id)
        sql = base + (" WHERE " + " AND ".join(where) if where else "") + " ORDER BY update_time DESC LIMIT 1"

    cur.execute(sql, params)
    row = cur.fetchone()
    return row


def main():
    parser = argparse.ArgumentParser(description="Print latest persisted state from SQLite DB")
    parser.add_argument(
        "--db",
        default="/home/arvind/AI-agents-Dev/7.Multi-agent/multi_agent_data.db",
        help="Path to SQLite DB (default: 7.Multi-agent/multi_agent_data.db)",
    )
    parser.add_argument(
        "--source",
        choices=["sessions", "user_states"],
        default="sessions",
        help="Table to read from (default: sessions)",
    )
    parser.add_argument("--app", dest="app_name", help="Filter by app_name")
    parser.add_argument("--user", dest="user_id", help="Filter by user_id")
    parser.add_argument("--session", dest="session_id", help="Filter by session id (sessions only)")

    args = parser.parse_args()

    try:
        conn = sqlite3.connect(args.db)
    except sqlite3.Error as e:
        print(f"Error opening DB {args.db}: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        row = fetch_latest_state(
            conn,
            source=args.source,
            app_name=args.app_name,
            user_id=args.user_id,
            session_id=args.session_id,
        )
        if not row:
            print("No rows found.")
            return

        if args.source == "sessions":
            app_name, user_id, session_id, state, update_time = row
            meta = {
                "source": args.source,
                "app_name": app_name,
                "user_id": user_id,
                "session_id": session_id,
                "update_time": update_time,
            }
        else:
            app_name, user_id, state, update_time = row
            meta = {
                "source": args.source,
                "app_name": app_name,
                "user_id": user_id,
                "update_time": update_time,
            }

        try:
            state_json = json.loads(state)
        except Exception:
            # Not JSON? print raw
            print(json.dumps({"meta": meta, "state_raw": state}, indent=2))
            return

        print(json.dumps({"meta": meta, "state": state_json}, indent=2))
    finally:
        conn.close()


if __name__ == "__main__":
    main()


