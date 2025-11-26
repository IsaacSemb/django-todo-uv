# Database Seeding in Django

I'm trying to figure out how to do mock data seeding in Django. There are a bunch of different methods for doing it, and I'm going to try out all of them to get a feel for what each one can do.

Here are the methods I'm exploring:

1. Raw SQL (using SQLite)
2. Raw Python script
3. Django shell script
4. Django fixtures
5. Django management command
6. Django management command with Faker

From these, I think I'll be able to pick out the best one to adopt as my go-to method.

## Quick Reference: Clearing the Database

To clear out the entire database (equivalent of `prisma migrate reset`):

```bash
python manage.py flush
# or with uv
uv run manage.py flush
```

---

## Method Overview & File Locations

### 1. Raw SQL

**Location:** `scripts/seeding/seed_todos.sql`

**How to run:**

```bash
sqlite3 db.sqlite3 < scripts/seeding/seed_todos.sql
```

**Summary:**
This didn't work because of password hashing issues. Django uses PBKDF2 with a complex format that's hard to generate manually in SQL. I think it could work for non-password-related stuff, but for users it's not practical.

**Status:** ⚠️ Skipped due to password hashing complexity

---

### 2. Standalone Python Script

**Location:** `scripts/seeding/seed_script_raw_sqlite.py`

**How to run:**

```bash
python scripts/seeding/seed_script_raw_sqlite.py
```

**Summary:**
It worked, but we still needed to set up Django because the passlib hashing algorithm isn't the same as Django's. Even though it's "standalone," we ended up needing Django setup for password hashing. Uses raw SQL with `sqlite3` module directly.

**Key learning:** Even "standalone" scripts often need Django for password hashing.

**Status:** ✅ Completed

---

### 3. Django Script (Using Django ORM)

**Location:** `scripts/seeding/seed_script_django_script.py`

**How to run:**

```bash
python scripts/seeding/seed_script_django_script.py
```

**Summary:**
Fully Django-powered and way more convenient. You can easily tell how much better it is compared to methods 1 and 2. Uses Django ORM (`User.objects.create_user()`, `Todo.objects.create()`) instead of raw SQL. Password hashing is automatic, foreign keys are simple, and timestamps are handled automatically.

**Key advantages:**

- No password hashing headaches
- No manual SQL
- Foreign keys are just objects
- Automatic validation
- Less code, more readable

**Status:** ✅ Completed

---

### 4. Django Fixtures

**Location:** `todos/fixtures/initial_todos.json` and `todos/fixtures/initial_users.json`

**What are Django fixtures?**

Django fixtures are JSON/YAML files that Django can load into the database. They're Django's built-in way to save and restore data - portable, version-controllable, and reusable across different environments.

**Setup:**

First, create the fixtures directory:

```bash
mkdir -p todos/fixtures/
```

**Two Approaches:**

**Approach A: Export existing data (easiest)**

If you already have seeded data in your database (from any method), export it:

```bash
# Export users
python manage.py dumpdata auth.User --indent 2 > todos/fixtures/initial_users.json

# Export todos
python manage.py dumpdata todos.Todo --indent 2 > todos/fixtures/initial_todos.json
```

This creates fixture files from your existing database automatically.

**Approach B: Create fixtures manually**

Convert your `mock_data` JSON into Django fixture format (different structure). Requires understanding the fixture format.

**How to load fixtures:**

```bash
python manage.py loaddata initial_users
python manage.py loaddata initial_todos
```

**Important Notes:**

1. **Loading order matters:** You must load data in a sensible order. You can't load todos before users because todos depend on users (foreign key integrity). If you try, you'll get:

   ```
   django.db.utils.IntegrityError: Problem installing fixtures
   ```

   Always load parent models before child models.
2. **Fixture naming is strict:** Django looks for fixtures in `<app>/fixtures/<name_of_fixture>`.

   - The fixture name in the command doesn't include the `.json` extension
   - The filename must match exactly what you specify in `loaddata`
   - Example: `loaddata initial_users` looks for `todos/fixtures/initial_users.json`
3. **Django automatically finds fixtures:** The commands above will automatically look in `todos/fixtures/` directory for the files.

**Summary:**
Django's built-in way to save/load data. Uses JSON/YAML files that are portable and version-controllable. The same fixture works across different environments. Great for sharing initial data or test data between team members.

The trick behind this is to know the structure of the fixture files, how fixtures look and how to create them manually if needed, they seem straight forward.

**Status:** ✅ Completed

---

### 5. Django Management Command (Basic)

**Location:** `todos/management/commands/seed_todos.py`

**Directory Structure Required:**

```
todos/
└── management/
    ├── __init__.py          # Empty file (makes it a Python package)
    └── commands/
        ├── __init__.py      # Empty file (makes it a Python package)
        └── seed_todos.py    # Your command file
```

**How to run:**

```bash
python manage.py seed_todos

# With custom file paths
python manage.py seed_todos --users-file path/to/users.json --todos-file path/to/todos.json

# See help
python manage.py seed_todos --help
```

**Key Concepts:**

1. **Command name = filename:** The command name comes from the filename (without `.py`). So `seed_todos.py` becomes `python manage.py seed_todos`.

2. **No manual Django setup:** Unlike standalone scripts, management commands don't need `django.setup()` - Django handles it automatically.

3. **Inherits from BaseCommand:** All management commands inherit from `BaseCommand` which provides structure and utilities.

4. **Shared utilities:** We created `seeding_utils.py` to avoid code duplication. Both `seed_todos` and `seed_all` use the same functions.

**Additional Command: `seed_all`**

We also created `seed_all.py` which acts as an orchestrator that can call different seeding methods:

```bash
# Use script method (default)
python manage.py seed_all

# Use fixtures
python manage.py seed_all --method fixtures

# Use another command
python manage.py seed_all --method command

# Try all methods
python manage.py seed_all --method all
```

**Summary:**
Django's recommended way to create reusable seeding commands. Follows Django conventions, can accept command-line arguments, and is discoverable via `python manage.py help`. No manual setup needed - Django handles everything. We've also created shared utilities (`seeding_utils.py`) to avoid code duplication across different commands.

**Key advantages:**
- No Django setup code needed
- Discoverable via `python manage.py help`
- Can accept command-line arguments
- Uses Django's output styling (`self.style.SUCCESS`, `self.style.ERROR`)
- Reusable and testable
- Can call other commands using `call_command()`

**Status:** ✅ Completed

---

### 6. Django Management Command with Faker

**Location:** `todos/management/commands/seed_todos_faker.py`

**How to run:**

```bash
python manage.py seed_todos_faker --count 50
```

**Summary:**
Same as method 5, but uses the Faker library to generate realistic fake data. Great for creating varied test data.

**Status:** ⏳ Not started yet

---

## Project Structure

Here's where all the seeding files are organized:

```
django-todo-uv/
├── scripts/
│   └── seeding/
│       ├── seed_todos.sql                    # Method #1: Raw SQL
│       ├── seed_script_raw_sqlite.py         # Method #2: Standalone Python
│       ├── seed_script_django_script.py      # Method #3: Django Script
│       └── mock_data/
│           ├── users.json
│           └── todos.json
│
└── todos/
    ├── fixtures/                              # Method #4: Fixtures
    │   ├── initial_users.json
    │   └── initial_todos.json
    │
    └── management/                            # Methods #5 & #6: Commands
        ├── __init__.py
        └── commands/
            ├── __init__.py
            ├── seeding_utils.py               # Shared utilities (no duplication!)
            ├── seed_todos.py                  # Method #5: Basic command
            ├── seed_all.py                    # Orchestrator command
            └── seed_todos_faker.py            # Method #6: Faker command
```

---

## Notes & Learnings

- **Password hashing** is the main reason raw SQL is impractical for Django user seeding
- **Django ORM** is way more convenient than raw SQL - less code, more safety
- **Method 3** (Django Script) is the sweet spot between learning and practicality
- **Method 5** (Management Commands) is the Django-recommended way - no setup needed, discoverable, and follows conventions
- **Shared utilities** (`seeding_utils.py`) help avoid code duplication across different seeding methods
- **Command naming** in Django: the command name comes from the filename (without `.py` extension)
- You can save a seeded database as a snapshot and restore it later (useful for quick resets)
- Management commands can call other commands using `call_command()` from `django.core.management`
