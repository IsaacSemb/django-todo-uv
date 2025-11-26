import os
import sqlite3
import json
from pathlib import Path
from datetime import datetime
import sys
import django
from passlib.context import CryptContext

# the hasher we are using
#  this is the standard that django uses so we needto use it so that unhashing works as expected
#  we are not using this for now because we are using the make_password function from Django
#  but we are keeping it here for reference ALSO IT DOESNT WORK
#  cause the hashing algorithm is different and the unhashing algorithm is different
#  so we are using the make_password function from Django
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], default = "pbkdf2_sha256" )


# Add project root to Python path so Django can find the settings module
# Project root is 2 levels up from this file (scripts/seeding/aa.py -> project root)
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Configure Django settings BEFORE importing anything Django-related
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_todo_fullstack.settings')
django.setup()  # This initializes Django

# NOW you can import Django functions
from django.contrib.auth.hashers import make_password

print('\n file name')
print(__file__)
print()

# our database file name (to avoid repetition and potential mistakes)
# this is the old way of doing it, it is not recommended to use it
# cause for every seeding script we would have to add the database file name
# and if we change the file name, we would have to change it in every script
# DATABASE_FILE = 'db.sqlite3'

# the absolute path to the database file
# this is the old way of doing it, it is not recommended to use it
# DB_PATH = Path(__file__).parent.parent.parent / DATABASE_FILE

# SAFER WAY TO GET THE DATABASE PATH
# Load DB path from Django settings to centralize configuration
from django.conf import settings

# If using the default DB, settings.DATABASES['default']['NAME'] gives the path (could be pathlib.Path or str)
DB_FROM_SETTINGS = settings.DATABASES['default']['NAME']
if isinstance(DB_FROM_SETTINGS, Path):
    DB_PATH = DB_FROM_SETTINGS
else:
    DB_PATH = Path(DB_FROM_SETTINGS)


print('\n DBPATH name')
print(DB_PATH)
print()


# To get column names from a SQLite table using Python:
def get_table_columns(conn, table_name):
    """
    Returns a list of column names for a given SQLite table.
    """
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns_info = cursor.fetchall()
    columns = [col[1] for col in columns_info]
    return columns

# To get all tables from a SQLite database using Python:
def get_all_tables(conn):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    return [table[1] for table in tables]


# this is the function that hashes the password
# we are using the make_password function from Django
def hash_password(password):
    try:
        # hashed_password = pwd_context.hash(password)
        hashed_password = make_password(password)
        return hashed_password
    except ImportError:
        raise RuntimeError("Soemthing went Wrong. Cannot hash password.")




def seed_users(conn, users_data):
    """Insert users into auth_user table"""
    cursor = conn.cursor()
    
    for user in users_data:
        hashed_password = hash_password(user['password'])
        current_time = datetime.now().isoformat()
        
        try:
            cursor.execute("""
                INSERT INTO auth_user (
                username,
                email,
                first_name,
                last_name,
                password,
                is_superuser,
                is_staff,
                is_active,
                date_joined
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                user['username'],
                user['email'],
                user['first_name'],
                user['last_name'],
                hashed_password,
                0,  # is_superuser (false)
                0,  # is_staff (false)
                1,  # is_active (true)
                current_time,
            ))
            print(f"✓ Created user: {user['username']}")
        except sqlite3.IntegrityError as e:
            print(f"✗ SQLITE ERROR: {e}")
    
    conn.commit()


def seed_todos(conn, todos_data):
    """Insert todos into todos table"""
    cursor = conn.cursor()
    
    for user_group in todos_data['todos']:
        user_id = user_group['user_id']
        
        for todo in user_group['todos']:
            current_time = datetime.now().isoformat()
            
            try:
                cursor.execute("""
                    INSERT INTO todos (
                    title,
                    description,
                    status,
                    created_at,
                    updated_at,
                    user_id
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    todo['title'],
                    todo['description'],
                    todo['status'],
                    current_time,
                    current_time,
                    user_id
                ))
                print(f"✓ Created todo: {todo['title']} for user_id {user_id}")
            except sqlite3.IntegrityError as e:
                print(f"✗ SQLITE ERROR: {e}")
    
    conn.commit()





def main():
    """Main seeding function"""
    # Load mock data
    script_dir = Path(__file__).parent
    users_file = script_dir / 'mock_data' / 'users.json'
    todos_file = script_dir / 'mock_data' / 'todos.json'
    
    with open(users_file, 'r') as f:
        users_data = json.load(f)
    
    with open(todos_file, 'r') as f:
        todos_data = json.load(f)
    
    # Connect to database
    print(f"Connecting to database: {DB_PATH}")
    conn = sqlite3.connect(str(DB_PATH))
    
    try:
        print("\n=== Seeding Users ===")
        seed_users(conn, users_data)
        
        print("\n=== Seeding Todos ===")
        seed_todos(conn, todos_data)
        
        print("\n✓ Seeding complete!")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        conn.rollback()
    finally:
        conn.close()


if __name__ == '__main__':
    main()