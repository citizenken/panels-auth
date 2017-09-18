#Panels-auth#
A simple Flask app that forwards Google Oauth requests from Panels-electron. This keeps the Oauth client ID and secret secure on a server, where it can't be unpacked or inspected.

It consists of a few endpoints:
1. `/auth` which starts the Oauth exchange
2. `/callback` which is redirected to after successful exchange, and listened for in the Electron app
3. `/logout` which clears session on the server

To run:
1. Build the virtual env
2. Run `gunicorn panels_oauth:app`

To deploy:
1. Configure a Dokku git remote `git remote add dokku dokku@<machine hostname>:<app name>`
2. Run `git push dokku master`
