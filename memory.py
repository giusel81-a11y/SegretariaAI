from database import conn

def add_note(text):

    conn.execute(
        "INSERT INTO notes(text) VALUES(?)",
        (text,)
    )

    conn.commit()


def get_notes():

    rows = conn.execute(
        "SELECT text FROM notes"
    )

    return [r[0] for r in rows]
