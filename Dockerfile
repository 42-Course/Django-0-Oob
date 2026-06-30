FROM python:3.12-alpine

WORKDIR /app

COPY . /app

# Pure-Python OOP day: standard library only.
CMD ["sh"]
