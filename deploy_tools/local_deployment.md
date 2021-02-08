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

Frontend development (server not required, Django settings include `frontend/build/templates` as a tempalte dir):

```
cd frontend
npm run watch
```

Frontend build for production: `npm run build`
