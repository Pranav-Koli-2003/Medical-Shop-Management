# Docker + CI/CD Setup — Medical Shop Management System

These 5 files turn your Docker/CI-CD resume line from a claim into something real you can demonstrate and discuss confidently.

## Files in this package
```
Dockerfile                      # Containerizes the Django app with Gunicorn
docker-compose.yml              # Runs Django + a real Postgres database together
.dockerignore                   # Keeps the image clean (no db.sqlite3, __pycache__, etc.)
requirements.txt                # Django + Gunicorn
.github/workflows/ci.yml        # Runs Django checks + tests automatically on every push
```

---

## How to Add These to Your Real Project

1. Copy all 5 files/folders into the **root of your Medical Shop project** (same level as `manage.py`).
2. If you already have a `requirements.txt`, merge the two rather than overwriting.
3. Commit and push:
   ```bash
   git add Dockerfile docker-compose.yml .dockerignore requirements.txt .github
   git commit -m "chore: add Docker and CI/CD pipeline"
   git push
   ```
4. Once pushed, go to your GitHub repo's **"Actions"** tab — you'll see the workflow run automatically. That green checkmark is now real, verifiable proof of a working CI pipeline.

---

## Try It Locally (do this before any interview)

```bash
docker compose up --build
```

This builds your Django app into a container and starts it alongside a real PostgreSQL database — visit `http://localhost:8000` to confirm it works.

**Important:** your `settings.py` currently hardcodes SQLite. To actually use the Postgres container, you'll need to update the `DATABASES` setting to read from the `DATABASE_URL` environment variable (using a package like `dj-database-url`). This step is intentionally left for you to do — walking through *why* and *how* you made this change is exactly the kind of detail an interviewer might ask about, and doing it yourself means you'll actually be able to explain it.

---

## What to Say in an Interview Now

With these files in your repo, you can honestly say:

> "I containerized my Medical Shop project with Docker, running Django with Gunicorn instead of the dev server, and set up a docker-compose file to run it alongside a Postgres database locally. I also added a GitHub Actions workflow that runs Django's checks and test suite automatically on every push."

This is now **true**, specific, and backed by a real commit in your repo — exactly the difference between a resume line that survives scrutiny and one that doesn't.

## One More Thing Worth Doing
Your `tests.py` file is currently empty (standard Django boilerplate). The CI workflow will technically pass either way, but "0 tests" is a noticeable gap if an interviewer opens the file. Adding even 5-10 real tests for your models (Purchase, Sell, Inventory) would make this pipeline demonstrate something meaningful, not just run successfully on nothing.
