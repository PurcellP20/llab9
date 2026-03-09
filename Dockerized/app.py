from flask import Flask, render_template, request, session, redirect, url_for
from functools import wraps
import psycopg2
import os

app = Flask(__name__)
app.secret_key = 'usaf_sql_challenge_2025'

# Database configuration - support both Docker and local
DB_NAME = os.getenv('DB_NAME', 'intel')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASS = os.getenv('DB_PASS', 'Password1!')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')


def get_db():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT
    )


def check_challenge_completed():
    """Check if challenge has been completed by querying a flag table"""
    try:
        conn = get_db()
        cur = conn.cursor()
        # Ensure table exists first
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS challenge_status
                    (
                        id        INTEGER PRIMARY KEY,
                        completed BOOLEAN DEFAULT FALSE
                    )
                    """)
        # Insert default if not exists
        cur.execute("""
                    INSERT INTO challenge_status (id, completed)
                    VALUES (1, FALSE)
                    ON CONFLICT (id) DO NOTHING
                    """)
        conn.commit()

        # Now check status
        cur.execute("SELECT completed FROM challenge_status WHERE id = 1")
        result = cur.fetchone()
        cur.close()
        conn.close()
        return result[0] if result else False
    except Exception as e:
        print(f"Error checking challenge status: {e}")
        return False


def mark_challenge_completed():
    """Mark challenge as completed in database"""
    try:
        conn = get_db()
        cur = conn.cursor()
        # Ensure table exists
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS challenge_status
                    (
                        id        INTEGER PRIMARY KEY,
                        completed BOOLEAN DEFAULT FALSE
                    )
                    """)
        # Update or insert
        cur.execute("""
                    INSERT INTO challenge_status (id, completed)
                    VALUES (1, TRUE)
                    ON CONFLICT (id) DO UPDATE SET completed = TRUE
                    """)
        conn.commit()
        cur.close()
        conn.close()
        print("Challenge marked as completed!")
    except Exception as e:
        print(f"Error marking challenge complete: {e}")


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    has_future_intel = check_challenge_completed()
    print(f"Login page - Challenge completed status: {has_future_intel}")

    if request.method == 'POST':
        password = request.form.get('password', '')

        # VULNERABLE: SQL Injection in login
        query = f"SELECT * FROM users WHERE password='{password}'"

        try:
            conn = get_db()
            cur = conn.cursor()
            cur.execute(query)
            user = cur.fetchone()
            cur.close()
            conn.close()

            if user:
                session['logged_in'] = True
                session['username'] = user[1]
                return redirect(url_for('dashboard'))
            else:
                error = "INVALID ACCESS CODE - AUTHENTICATION FAILED"
        except Exception as e:
            error = f"SYSTEM ERROR: {str(e)}"

    return render_template('login.html', error=error, has_future_intel=has_future_intel)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    query = ''
    scope = ''
    notes = []

    # Check if challenge was already completed (stored in database)
    has_future_intel = check_challenge_completed()
    print(f"Dashboard - Challenge completed status (before): {has_future_intel}")

    if request.method == 'POST':
        query = request.form.get('query', '')
        scope = request.form.get('scope', '')

        # If scope filter is used (button click)
        if scope and not query:
            sql = f"SELECT * FROM notes WHERE scope = '{scope}' ORDER BY id"
        # If search query is used
        elif query:
            # VULNERABLE: SQL Injection in search
            # Case insensitive search but vulnerable to injection
            # Working exploits:
            # 1. %') OR scope='future'--
            # 2. ') OR scope='future'--
            # 3. ' OR scope='future'--
            # 4. ') OR '1'='1
            sql = f"SELECT * FROM notes WHERE (title ILIKE '%{query}%' OR body ILIKE '%{query}%' OR month ILIKE '%{query}%') AND scope IN ('current', 'historical') ORDER BY id"
        else:
            # No query and no scope, return empty
            return render_template('dashboard.html',
                                   notes=notes,
                                   query=query,
                                   scope=scope,
                                   has_future_intel=has_future_intel,
                                   username=session.get('username', 'Unknown'))

        try:
            conn = get_db()
            cur = conn.cursor()
            cur.execute(sql)
            notes = cur.fetchall()

            # Check if any future intel was retrieved (SQL injection successful)
            if notes and not has_future_intel:
                for note in notes:
                    if note[4] == 'future':  # note[4] is the scope column
                        print(f"Future intel detected! Marking challenge as complete.")
                        has_future_intel = True
                        mark_challenge_completed()
                        break

            print(f"Dashboard - Challenge completed status (after): {has_future_intel}")

            cur.close()
            conn.close()
        except Exception as e:
            notes = []

    return render_template('dashboard.html',
                           notes=notes,
                           query=query,
                           scope=scope,
                           has_future_intel=has_future_intel,
                           username=session.get('username', 'Unknown'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)