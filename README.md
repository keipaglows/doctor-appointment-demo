# doctor-appointment-demo

## Required

- Python 3.7
- NPM

## Setting up server app

- Run `make setup-server` in order to buildout the server app;
- Use `make run-server` to run it;

## Setting up web client app

- Run `make setup-client:` in order to install required npm packages for the client app;
- Use `make run-client` to it;

## Configuring DrChrono

- Make sure to configure at DrChrono `api-management` section your Redirect URIs with `http://127.0.0.1:8010/api/oauth2-authorize`;
- Change `DR_CHRONO_CLIENT_ID` and `DR_CHRONO_CLIENT_SECRET` to your DrChrono app settings through env variables before running the server app;
