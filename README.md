Dental Space One Test Flask OAuth2 Client
=========================================

Running in docker:

```bash
docker build -t dso-test-flask:latest .
docker run --rm -p 4000:4000 \
    -e OAUTH2_SERVER=https://testlab.ondso.dev \
    -e OAUTH2_CLIENT_ID=<your client id> \
    -e OAUTH2_CLIENT_SECRET=<your client secret> \
      dso-test-flask:latest
```