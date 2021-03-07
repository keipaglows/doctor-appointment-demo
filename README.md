# doctor-appointment-demo

## Required

- Python 3.7

## Setting up server app

- Run `make setup` in order to buildout the project;
- Use `make run` to run it;

## Configuring DrChrono

- Make sure to configure at DrChrono `api-management` section your Redirect URIs with `http://127.0.0.1:8010/api/oauth2-authorize`;
- Change `DR_CHRONO_CLIENT_ID` and `DR_CHRONO_CLIENT_SECRET` to your DrChrono app settings through env variables before running the app;
