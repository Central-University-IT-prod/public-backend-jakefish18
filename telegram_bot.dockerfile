FROM python:3.12.1-alpine3.19

WORKDIR /src

COPY src/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY src/ /src

CMD ["python3", "main.py"]