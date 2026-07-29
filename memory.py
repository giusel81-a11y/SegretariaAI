from database import conn


def add_note(text):

    conn.execute(
        "INSERT INTO notes(text) VALUES(?)",
        (text,)
    )

    conn.commit()


def complete_note(note_id):

    conn.execute(
        "UPDATE notes SET completed = 1 WHERE id = ?",
        (note_id,)
    )

    conn.commit()


def delete_note(note_id):

    conn.execute(
        "DELETE FROM notes WHERE id = ?",
        (note_id,)
    )

    conn.commit()


def get_active_notes():

    rows = conn.execute(
        "SELECT id, text FROM notes WHERE completed = 0"
    )

    return rows.fetchall()


def reset_notes():

    conn.execute("DELETE FROM notes")

    conn.execute(
        "DELETE FROM sqlite_sequence WHERE name='notes'"
    )

    conn.commit()
