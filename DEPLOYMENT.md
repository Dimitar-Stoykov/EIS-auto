# Deploying eis_project (Railway + Postgres + Cloudflare R2)

Plan: Railway hosts the Django app + Postgres database. Cloudflare R2 hosts
static files (CSS) and media (uploaded images/videos), so Railway itself
never has to serve that traffic.

You said you want to test this on your own Railway/Cloudflare account first,
then redo it for real on the owner's accounts once it works. Everything
below works the same either time — just repeat the same steps under the
new accounts later. Nothing here is owner-specific.

## 0. What changed in the code (already done)

- `settings.py` reads `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`,
  `CSRF_TRUSTED_ORIGINS`, database credentials, and R2 credentials from
  environment variables — all fall back to safe local-dev defaults if unset,
  so nothing changes for your day-to-day local work.
- `DATABASES` uses `DB_ENGINE`/`DB_NAME`/`DB_USER`/`DB_PASSWORD`/`DB_HOST`/
  `DB_PORT` if set (Postgres in production), otherwise falls back to
  `db.sqlite3` (unchanged for local dev).
- Static files (`staticfiles/`) and media (`mediafiles/`) are served from
  Cloudflare R2 in production, via `django-storages` — see
  `eis_project/storage_backends.py`. Locally, with no R2 env vars set,
  everything keeps working exactly as it does today (local folders).
- `.gitignore` fixed — it was excluding `staticfiles/` (the real CSS source
  folder), so it had never actually been committed to GitHub. Also now
  ignores `mediafiles/` (your uploaded images/videos live in R2 + the
  database in production, not in git) and `staticfiles_collected/` (a
  build artifact).
- Added `Procfile` (`release`: migrate + collectstatic, `web`: gunicorn) and
  `.python-version` (3.12 — Django 6.0 requires it) for Railway's builder.
- Added `requirements.txt` entries: `gunicorn`, `psycopg[binary]` (Postgres
  driver), `django-storages[s3]` (R2 support, R2 speaks the S3 API).

## 1. Create the Cloudflare R2 bucket

1. Cloudflare dashboard → **R2 Object Storage** → **Create bucket**. Name it
   e.g. `eisauto-media`.
2. Bucket → **Settings** → **Public Access**: enable it (or connect a custom
   domain — see step 1b). Without this, images won't load on the site.
3. Bucket → **Settings** → copy the **S3 API endpoint** — looks like
   `https://<account_id>.r2.cloudflarestorage.com`. This is `R2_ENDPOINT_URL`.
4. Cloudflare dashboard → **R2** → **Manage API Tokens** → create a token
   with **Object Read & Write** permission, scoped to this bucket. You get
   an **Access Key ID** and **Secret Access Key** — these are
   `R2_ACCESS_KEY_ID` / `R2_SECRET_ACCESS_KEY`. Shown once — save them.

### 1b. Public URL

Two options for `R2_PUBLIC_DOMAIN` (no `https://`, no trailing slash):

- **Quick test (what you'll use first):** Bucket → Settings → Public
  Access → enable the `r2.dev` subdomain. You'll get something like
  `pub-xxxxxxxxxxxx.r2.dev`. Use that.
- **Real domain (for the owner's account later):** connect a subdomain you
  control, e.g. `cdn.eisauto.com`, via Bucket → Settings → Custom Domains.
  Cleaner for production, and doesn't change if you ever move providers.

## 2. Commit and push

```bash
git add .
git commit -m "Add Postgres/Railway/R2 production config"
git push origin main
```

## 3. Create the Railway project

1. railway.app → sign in with GitHub → **New Project → Deploy from GitHub
   repo** → select your repo.
2. Railway detects Python and builds using your `Procfile` and
   `.python-version` automatically.
3. **Add Postgres**: in the project, **+ New → Database → PostgreSQL**.
   Railway creates it as a separate service in the same project.
4. **Set environment variables** on the *web* service (Settings →
   Variables):
   - `SECRET_KEY` — generate one: `python -c "import secrets; print(secrets.token_urlsafe(50))"`
   - `DEBUG` = `False`
   - `ALLOWED_HOSTS` = `<your-app>.up.railway.app` (add your real domain
     later once you have one)
   - `CSRF_TRUSTED_ORIGINS` = `https://<your-app>.up.railway.app`
   - `DB_ENGINE` = `django.db.backends.postgresql`
   - `DB_NAME` = `${{Postgres.PGDATABASE}}`
   - `DB_USER` = `${{Postgres.PGUSER}}`
   - `DB_PASSWORD` = `${{Postgres.PGPASSWORD}}`
   - `DB_HOST` = `${{Postgres.PGHOST}}`
   - `DB_PORT` = `${{Postgres.PGPORT}}`
     (Railway lets you reference another service's variables with
     `${{ServiceName.VAR}}` — click the variable field, it autocompletes.)
   - `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_BUCKET_NAME`,
     `R2_ENDPOINT_URL`, `R2_PUBLIC_DOMAIN` — from step 1.
   - `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_HOST`, `EMAIL_PORT`,
     `EMAIL_USE_TLS` — same values as your local `.env`.
5. Confirm **Settings → Source → Deploy on push** is on for `main`.
6. Wait for the deploy. The `release` command runs `migrate` +
   `collectstatic` before the app starts — your Postgres schema and R2
   static files will already be in place.

## 4. Move your existing data in

Your real content (services, gallery, prices, site settings) currently only
exists in your local `db.sqlite3`. Export it locally:

```bash
python manage.py dumpdata --natural-foreign --natural-primary \
  -e contenttypes -e auth.permission -e admin.logentry -e sessions.session \
  --indent 2 -o data.json
```

Don't commit `data.json` — it contains your admin user's hashed password.

Install the Railway CLI, then load it into the live Postgres:

```bash
railway login
railway link          # pick your project
railway run python manage.py loaddata data.json
```

Your gallery/price images referenced in that data need to physically exist
in the R2 bucket too — upload the contents of your local `mediafiles/`
folder into the bucket under the `media/` prefix (matches
`MediaStorage.location` in `storage_backends.py`), keeping the same
sub-paths (e.g. `media/gallery/images/...`). The R2 dashboard supports
drag-and-drop upload, or use `rclone`/the `aws` CLI pointed at the R2
endpoint for bulk upload.

Then create a fresh admin user on production (safer than the loaded one):

```bash
railway run python manage.py createsuperuser
```

## 5. Test it

Visit `https://<your-app>.up.railway.app` — check the homepage loads with
CSS, images load from the R2 public domain (check an `<img>` src in
DevTools — it should point at your `r2.dev`/custom domain, not `/media/`),
the contact form sends email, and `/admin/` login + password reset work.

## 6. Once it works: redo it for real

Repeat sections 1–4 under the owner's Railway and Cloudflare accounts (new
bucket, new Railway project, same env var names). Nothing in the codebase
needs to change — it's the same repo, just pointed at different
credentials. When ready, point the real domain at Railway and swap
`R2_PUBLIC_DOMAIN` to the owner's real custom domain instead of the test
`r2.dev` one.

## Ongoing workflow

From now on: edit code locally → `git push origin main` → Railway rebuilds
and redeploys automatically (runs migrations + collectstatic first) → data
lives in Postgres, uploads live in R2 — neither is touched by a redeploy.
