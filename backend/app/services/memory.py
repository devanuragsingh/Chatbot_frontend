from app.core.database import get_connection

# Save message in DB
def add_message(session_id, role, content):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)",
        (session_id, role, content)
    )

    conn.commit()
    conn.close()


# Get memory from DB
def get_memory(session_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT role, content FROM messages WHERE session_id=? ORDER BY id DESC LIMIT 10",
        (session_id,)
    )

    rows = cursor.fetchall()
    conn.close()

    # Reverse to maintain order
    return [{"role": r[0], "content": r[1]} for r in reversed(rows)]