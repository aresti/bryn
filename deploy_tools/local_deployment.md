# Local development environment setup

- clone the repo
- setup venv and install requirements
- obtain credentials for auth_settings.py and a copy of locals.py
- pre-commit install (to install hooks)

If outside of the climb network, use:

- sshuttle --dns -H -r user@someVMwithinCLIMB 0/0

Backend test server:

```
python brynweb/manage.py runserver
```

Frontend development:

```
cd frontend
npm run serve
```

Then access at http://localhost:8080/, via webpack devserver to get HMR (non webpack routes are proxied to Django at 8000)

Frontend build for production: `npm run build`, then simply serve from Django (webpack outputs templates & bundles to dirs accessible to Django)
Whitenoise is used for static files so no need to setup static routing in nginx config.
