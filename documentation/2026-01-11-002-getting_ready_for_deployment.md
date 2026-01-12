```python
# Security settings for production
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
```

these are set in the settings file
here is what my current understanding of them is


SECURE_SSL_REDIRECT
Forces all HTTP requests to redirect to HTTPS.
Ensures all traffic is encrypted in transit.
Prevents credentials, cookies, and data from being sent over plaintext connections.

SESSION_COOKIE_SECURE
Session cookies are sent only over HTTPS.
Prevents session hijacking via insecure HTTP requests.
Guarantees session identifiers are transmitted only on encrypted channels.

CSRF_COOKIE_SECURE
CSRF token cookies are sent only over HTTPS.
Prevents leakage of CSRF tokens over insecure connections.
Protects authenticated actions from request forgery.

SECURE_BROWSER_XSS_FILTER
Enables browser-level XSS protection (primarily for older browsers).
Blocks pages when reflected JavaScript injection is detected.
Defense-in-depth measure; does not fix XSS vulnerabilities.

SECURE_CONTENT_TYPE_NOSNIFF
Prevents browsers from guessing content types.
Forces browsers to respect declared MIME types.
Mitigates script execution through mislabelled or malicious files.


PREPARING DEPLOYMENT 
set up the env vars in your env file
this is dictated by the application youre building

We need to cater for the fact that not everyone uses UV
but you know what everyone uses????
good ol pip

so to be on a safe side
we need to set up the protection by just going with pip

### Generating `requirements.txt` when using `uv`

* `pyproject.toml` is the **single source of truth** for dependencies.
* `requirements.txt` is a **derived compatibility file** for deployment platforms that do not support `uv`.

**Preferred method (using `uv`):**

```bash
uv pip compile pyproject.toml -o requirements.txt
```

* Reads dependencies from `pyproject.toml`
* Resolves and pins versions
* Produces a pip-compatible `requirements.txt`

This keeps development modern while remaining deployment-friendly.

**Fallback method (not preferred):**

```bash
pip freeze > requirements.txt
```

* Captures everything in the active virtual environment
* May include transitive or unintended dependencies
* Use only if the environment is clean

**Principle:**
Do not edit `requirements.txt` manually.
Always regenerate it from `pyproject.toml` to avoid divergence.

**Mental model:**
`pyproject.toml` → canonical dependency definition
`requirements.txt` → deployment adapter for legacy tooling

preparation for deployment

shortcut to generate the secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

check for problems
    checking for problems in development
        uv run python manage.py check 

    checking for problems in production, we add the deploy flag
        uv run python manage.py check --deploy

uv run python manage.py collectstatic
