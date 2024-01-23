import mysql.connector
import os


def create_db_connection():
    return mysql.connector.connect(
        host = os.getenv("DB_HOST"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD"),
        database = os.getenv("DB_NAME") ,
        port = os.getenv("DB_PORT")
    )


def close_db_connection(db_connection, cursor):
    cursor.close()
    db_connection.close()


def clicks_check_is_fastest(time_to_check):
    try:
        db_connection = create_db_connection()
        cursor = db_connection.cursor()
        cursor.execute("""
            SELECT MIN(time_taken)
            FROM leaderboard
            WHERE time_taken IS NOT NULL
        """)
        fastest_time_taken_data = cursor.fetchone()
        close_db_connection(db_connection, cursor)

        fastest_time_taken = fastest_time_taken_data[0] if fastest_time_taken_data else None
        if fastest_time_taken is None:
            return True
        elif isinstance(time_to_check, (int, float)) and isinstance(fastest_time_taken, (int, float)):
            if time_to_check < fastest_time_taken:
                return True
            else:
                return False
        else:
            return False
    except mysql.connector.Error:
        return False


def clicks_check_highest_streak():
    db_connection = create_db_connection()
    cursor = db_connection.cursor()

    cursor.execute("""
        SELECT name, streak
        FROM leaderboard
        WHERE streak = (SELECT MAX(streak) FROM leaderboard WHERE streak > 1)
        LIMIT 1
    """)
    user_with_highest_streak = cursor.fetchone()

    close_db_connection(db_connection, cursor)

    return user_with_highest_streak if user_with_highest_streak else None


def clicks_fastest_time():
    try:
        db_connection = create_db_connection()
        cursor = db_connection.cursor()
        cursor.execute("""
            SELECT name, MIN(time_taken)
            FROM leaderboard
            WHERE time_taken = (SELECT MIN(time_taken) FROM leaderboard WHERE time_taken IS NOT NULL)
        """)
        fastest_time_taken_data = cursor.fetchone()
        close_db_connection(db_connection, cursor)
        return fastest_time_taken_data if fastest_time_taken_data else ("No user", 0)
    except mysql.connector.Error:
        return ("No user", 0)
    

def clicks_slowest_time():
    try:
        db_connection = create_db_connection()
        cursor = db_connection.cursor()
        cursor.execute("""
            SELECT name, MAX(time_taken)
            FROM leaderboard
            WHERE time_taken = (SELECT MAX(time_taken) FROM leaderboard WHERE time_taken IS NOT NULL)
        """)
        slowest_time_taken_data = cursor.fetchone()
        close_db_connection(db_connection, cursor)
        return slowest_time_taken_data if slowest_time_taken_data else ("No user", 0)
    except mysql.connector.Error:
        return ("No user", 0)


def clicks_get_by_name(name):
    try:
        db_connection = create_db_connection()
        cursor = db_connection.cursor()
        cursor.execute("""
            SELECT clicks, time_taken, streak
            FROM leaderboard
            WHERE name = %s
        """, (name,))
        user_data = cursor.fetchone()
        close_db_connection(db_connection, cursor)
        return user_data if user_data else (0, 0, 0)
    except mysql.connector.Error:
        return (0, 0, 0)


def clicks_get_leaderboard(limit=10):
    try:
        db_connection = create_db_connection()
        cursor = db_connection.cursor()
        cursor.execute("""
            SELECT name, clicks
            FROM leaderboard
            ORDER BY clicks DESC
            LIMIT %s
        """, (limit,))
        leaderboard_data = cursor.fetchall()
        leaderboard_text = ""
        for rank, (name, clicks) in enumerate(leaderboard_data, start=1):
            leaderboard_text += f"{rank} {name}: {clicks}\n"
        close_db_connection(db_connection, cursor)
        return leaderboard_text
    except mysql.connector.Error:
        return "Error retrieving leaderboard data"


def clicks_get_total():
    try:
        db_connection = create_db_connection()
        cursor = db_connection.cursor()
        cursor.execute("""
            SELECT SUM(clicks)
            FROM leaderboard
        """)
        total_clicks = cursor.fetchone()
        close_db_connection(db_connection, cursor)
        return total_clicks[0] if total_clicks else 0
    except mysql.connector.Error:
        return 0


def clicks_reset():
    try:
        db_connection = create_db_connection()
        cursor = db_connection.cursor()
        cursor.execute("DELETE FROM leaderboard")
        db_connection.commit()
        close_db_connection(db_connection, cursor)
        return "Leaderboard cleared successfully"
    except mysql.connector.Error:
        return "Error clearing leaderboard"


async def clicks_update(name, time_taken):
    db_connection = create_db_connection()
    cursor = db_connection.cursor()

    cursor.execute("""
        SELECT clicks, time_taken, streak
        FROM leaderboard
        WHERE name = %s
    """, (name,))
    user_data = cursor.fetchone()

    if user_data is None:
        cursor.execute("""
            INSERT INTO leaderboard (name, clicks, time_taken, streak)
            VALUES (%s, 1, %s, 1)
        """, (name, time_taken))
    else:
        clicks, current_time_taken, current_streak = user_data

        if current_time_taken is None or time_taken < current_time_taken:
            new_time = time_taken
        else:
            new_time = current_time_taken

        cursor.execute("""
            UPDATE leaderboard
            SET clicks = %s, time_taken = %s, streak = %s
            WHERE name = %s
        """, (clicks + 1, new_time, current_streak + 1, name))

    cursor.execute("""
            UPDATE leaderboard
            SET streak = 0
            WHERE name <> %s
        """, (name,))
        
    db_connection.commit()
    close_db_connection(db_connection, cursor)


def token_add(ticker, pair, ca, chain, image_url):
    db_connection = create_db_connection()
    cursor = db_connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tokens (
            ticker VARCHAR(255) PRIMARY KEY,
            pair VARCHAR(255),
            ca VARCHAR(255),
            chain VARCHAR(255),
            image_url VARCHAR(255)
        )
    """)
    db_connection.commit()

    cursor.execute("SELECT ticker FROM tokens WHERE ticker = %s", (ticker,))
    existing_token = cursor.fetchone()

    if existing_token:
        cursor.execute("""
            UPDATE tokens 
            SET pair = %s, ca = %s, chain = %s, image_url = %s
            WHERE ticker = %s
        """, (pair, ca, chain, image_url, ticker))
        db_connection.commit()
    else:
        cursor.execute("""
            INSERT INTO tokens (ticker, pair, ca, chain, image_url)
            VALUES (%s, %s, %s, %s, %s)
        """, (ticker, pair, ca, chain, image_url))
        db_connection.commit()
    close_db_connection(db_connection, cursor)



def token_get(ticker):
    db_connection = create_db_connection()
    cursor = db_connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tokens WHERE ticker = %s", (ticker.lower(),))
    matching_data = cursor.fetchall()
    close_db_connection(db_connection, cursor)

    return matching_data