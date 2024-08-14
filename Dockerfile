FROM python:3.12-alpine
RUN pip install --no-cache-dir flask requests pkce
ADD . /app
WORKDIR /app
ENTRYPOINT ["flask", "run", "--port", "4000", "--host", "0"]