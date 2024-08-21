FROM python:3.12.1-alpine3.19

WORKDIR /src

COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/alembic.ini .
COPY src/ .

CMD ["alembic", "upgrade", "head"]
