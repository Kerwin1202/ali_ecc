FROM python:3.11
LABEL maintainer="Kerwin"

WORKDIR /app

COPY . /app/

RUN pip install -r requirements.txt

EXPOSE 19951

ENTRYPOINT [ "python", "main.py", "80" ]