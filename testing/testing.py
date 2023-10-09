import sqlite3
from api import index as api

db_connection = sqlite3.connect("testdb.db")

def init_db():
    cursor = db_connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leaderboard (
            name TEXT PRIMARY KEY,
            clicks INTEGER
        )
    """)
    db_connection.commit()


def clicks_get_by_name(name):
    try:
        cursor = db_connection.cursor()
        
        cursor.execute("""
            SELECT clicks
            FROM leaderboard
            WHERE name = ?
        """, (name,))
        
        user_data = cursor.fetchone()
        
        return user_data[0] if user_data else 0
    
    except sqlite3.Error:
        return 0


def clicks_get_leaderboard(limit=20):
    try:
        cursor = db_connection.cursor()
        
        cursor.execute("""
            SELECT name, clicks
            FROM leaderboard
            ORDER BY clicks DESC
            LIMIT ?
        """, (limit,))
        
        leaderboard_data = cursor.fetchall()
        
        leaderboard_text = ""
        
        for rank, (name, clicks) in enumerate(leaderboard_data, start=1):
            leaderboard_text += f"{rank} {api.escape_markdown(name)}: {clicks}\n"
        
        return leaderboard_text
    
    except sqlite3.Error:
        return "Error retrieving leaderboard data"


def clicks_get_user_total(user_id):
    try:
        cursor = db_connection.cursor()
        
        cursor.execute("""
            SELECT SUM(clicks)
            FROM leaderboard
            WHERE name = ?
        """, (user_id,))
        
        total_clicks = cursor.fetchone()
        
        return total_clicks[0] if total_clicks else 0
    
    except sqlite3.Error:
        return 0 


def clicks_get_total():
    try:
        cursor = db_connection.cursor()
        
        cursor.execute("""
            SELECT SUM(clicks)
            FROM leaderboard
        """)
        
        total_clicks = cursor.fetchone()
        
        return total_clicks[0] if total_clicks else 0
    
    except sqlite3.Error:
        return 0


async def clicks_update(name):
    cursor = db_connection.cursor()
    
    cursor.execute("""
        SELECT clicks
        FROM leaderboard
        WHERE name = ?
    """, (name,))
    
    user_data = cursor.fetchone()
    
    if user_data is None:
        cursor.execute("""
            INSERT INTO leaderboard (name, clicks)
            VALUES (?, 1)
        """, (name,))
    else:
        cursor.execute("""
            UPDATE leaderboard
            SET clicks = ?
            WHERE name = ?
        """, (user_data[0] + 1, name))
    
    db_connection.commit()
