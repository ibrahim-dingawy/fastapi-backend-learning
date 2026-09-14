import sqlite3


connection = sqlite3.connect("video_app.db")
cursor = connection.cursor()




cursor.execute(
    """
    INSERT INTO videos (title, description, status)
    VALUES (?, ?, ?)
    """,
    ("Python Basics", "Python tutorial", "indexed")
)

cursor.execute(
    """
    INSERT INTO videos (title, description, status)
    VALUES (?, ?, ?)
    """,
    ("FastAPI Upload", "File upload tutorial", "processing")
)

cursor.execute(
    """
    INSERT INTO videos (title, description, status)
    VALUES (?, ?, ?)
    """,
    ("Database Intro", "Learning SQLite", "failed")
)

connection.commit()


cursor.execute("""
SELECT COUNT(*)
FROM videos
WHERE status = 'indexed'
""")

print(cursor.fetchone()[0])




