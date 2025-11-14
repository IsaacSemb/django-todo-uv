## Application Flow Notes – 10 Nov 2025

### Context
I'm rebuilding my Django muscle memory by walking through a full-stack Todo application.  
The goal is to understand each hop in the request/response cycle—especially around authentication
and templating—before introducing Django REST Framework.

---

### Current Flow (High Level)

1. **Landing Pages**  
   - `home`, `about`, and `contact` are publicly accessible.  
   - They currently serve static/dummy content but establish the basic navigation experience.

2. **Authentication CTA**  
   - The landing page invites the user to “view todos”.  
   - If authenticated, the user is routed to the todos dashboard.  
   - Anonymous users are redirected to the login form.

3. **Auth Experience**  
   - Dedicated modal-style login and signup pages exist.  
   - UI toggles between a “Login” button and “Welcome, <username> / Logout” based on `user.is_authenticated`.  
   - Successful login issues a 302 redirect (confirmed via network inspector) to avoid double form submission.

4. **Next Immediate Goals**  
   - Implement real signup logic (create user, auto-login, or redirect).  
   - Protect todos views with `login_required`.  
   - Filter todos by `request.user`.  
   - Wire Create / Edit / Delete flows (feel the plain-Django pain before reaching for DRF).

---

### Lessons & Mental Models

#### 1. Templates vs. URL Names

| Use Case                              | Correct Input                         | Why                                      |
|--------------------------------------|---------------------------------------|------------------------------------------|
| Rendering a template                 | `'website/home.html'`                 | `render()` needs a real template path.   |
| Linking/Redirecting by URL name      | `'website:home'`                      | Resolved through the URL dispatcher.     |
| Getting the concrete URL string      | `reverse('website:home')  # → '/'`    | Converts `app:view` → URL path.          |

- **Colon (`app:view`) notation is ONLY for URL resolution.**  
  Templates, static files, models, etc. must use filesystem paths.
- **`render()` does _not_ resolve URL names.** Trying `render(request, 'app:view')`
  raises `TemplateDoesNotExist`.
- **`redirect()` accepts URL names because it calls `reverse()` internally.**

#### 2. Redirect Semantics

| Function      | Returns                                    | Typical Use                                           |
|---------------|---------------------------------------------|--------------------------------------------------------|
| `render()`    | `HttpResponse` with HTML                    | Show a page (GET or failed POST).                      |
| `redirect()`  | `HttpResponseRedirect` (302)                | After success (POST/PUT/DELETE) to avoid resubmission. |
| `reverse()`   | URL string (no response by itself)          | Build URLs in Python code; feed into `redirect()` etc. |

- A 302 response instructs the browser to perform a clean GET to the new location.
- Great for post/redirect/get patterns—refreshing won’t resubmit data.

#### 3. Template Context & Navbar Toggle

- Django injects `user` into templates when `django.contrib.auth` context processor is enabled.
- Use `user.is_authenticated` (read-only property) to gate UI:

  ```django
  {% if user.is_authenticated %}
      Welcome, {{ user.username }} | Logout
  {% else %}
      Login
  {% endif %}
  ```

---

### Personal Notes & Observations

**Network Inspector for Understanding Redirects (2025-11-10)**
- Visual confirmation of 302 redirects via browser dev tools clarifies the login/logout flow.
- Seeing the actual HTTP response codes reinforces understanding of the request/response cycle.
- This helps distinguish between `render()` (200) and `redirect()` (302) behaviors.

**Documentation Strategy**
- Keeping clean, timestamped documentation helps "future me" revisit decisions quickly.
- Especially valuable when layering in DRF and comparing pure Django vs. DRF workflows.

---

### Template Learning: URL Variable Assignment (2025-11-14)

**Problem**: Wanted to reuse the same form template for both creating and editing todos, with the form action changing based on context.

**Solution**: Discovered Django template variable assignment using the `as` keyword with `{% url %}`.

**Pattern**:
```django

{% if todo %}
  {% url 'todos:edit_todo' todo.id as form_action %}
{% else %}
  {% url 'todos:add_todo' as form_action %}
{% endif %}

<form action="{{ form_action }}" method="POST">
  <!-- form fields -->
</form>

```

**Key Insight**: The `as form_action` syntax allows us to:
1. Conditionally resolve different URLs based on template context.
2. Store the resolved URL string in a variable.
3. Use that variable in HTML attributes (like `action=`).

This is cleaner than duplicating the entire form or using multiple conditionals throughout the template.

