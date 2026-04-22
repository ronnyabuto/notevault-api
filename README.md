# NoteVault API

A secure RESTful Flask API backend for a personal notes productivity app. Users can register, log in, and manage their own notes. Session-based authentication ensures each user can only access and modify their own data.

---

## Project Description

NoteVault lets authenticated users create, read, update, and delete personal notes. All resource endpoints are protected — unauthenticated requests are rejected, and users cannot view or modify notes belonging to other users. The notes index endpoint supports pagination.

---

## Installation

1. **Clone the repository and navigate into the project folder:**

   ```bash
   git clone https://github.com/ronnyabuto/notevault-api.git
   cd notevault-api
   ```

2. **Create and activate a virtual environment, then install dependencies:**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install flask flask-sqlalchemy flask-migrate flask-bcrypt flask-restful faker marshmallow
   ```

   Or if you have Pipenv installed:

   ```bash
   pipenv install
   pipenv shell
   ```

3. **Navigate into the server directory:**

   ```bash
   cd server
   ```

4. **Apply database migrations:**

   ```bash
   flask db upgrade
   ```

5. **Seed the database with example data:**

   ```bash
   python seed.py
   ```

---

## Running the App

```bash
cd server
flask run --port 5555
```

Or:

```bash
python app.py
```

The API will be available at `http://localhost:5555`.

---

## Testing with the Frontend Client

The assignment provides a session-based React client for testing all auth and resource endpoints:

```bash
git clone https://github.com/learn-co-curriculum/flask-c10-summative-lab-sessions-and-jwt-clients.git
cd flask-c10-summative-lab-sessions-and-jwt-clients/client-with-sessions
npm install
npm start   # runs on http://localhost:4000
```

Ensure the Flask API is running on port 5555 before starting the client. The React app proxies all requests to `http://localhost:5555` automatically.

---

## API Endpoints

### Auth

| Method | Endpoint        | Description                                              |
|--------|-----------------|----------------------------------------------------------|
| POST   | `/signup`       | Register a new user. Returns user data and starts a session. Body: `{ "username", "password" }` |
| POST   | `/login`        | Log in with existing credentials. Returns user data and starts a session. Body: `{ "username", "password" }` |
| DELETE | `/logout`       | End the current session. Requires an active session.     |
| GET    | `/check_session`| Returns the currently logged-in user. Used to persist login state on page refresh. |

### Notes (all require an active session)

| Method | Endpoint        | Description                                                                                      |
|--------|-----------------|--------------------------------------------------------------------------------------------------|
| GET    | `/notes`        | Returns a paginated list of the logged-in user's notes. Query params: `page` (default 1), `per_page` (default 10). |
| POST   | `/notes`        | Create a new note. Body: `{ "title", "content" }`                                               |
| PATCH  | `/notes/<id>`   | Update a note by ID. Only the owner can update. Body: `{ "title"?, "content"? }`                |
| DELETE | `/notes/<id>`   | Delete a note by ID. Only the owner can delete.                                                  |

### Response Codes

| Code | Meaning                              |
|------|--------------------------------------|
| 200  | OK                                   |
| 201  | Created                              |
| 204  | No Content (successful delete/logout)|
| 401  | Unauthorized — not logged in         |
| 403  | Forbidden — does not own resource    |
| 404  | Not Found                            |
| 422  | Unprocessable — validation failed    |
