FROM python:3.11-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && apk add --no-cache bash gcc musl-dev libffi-dev python3-dev && rm -rf /var/cache/apk/*
RUN python -m pip install --upgrade pip
RUN pip install poetry

COPY pyproject.toml .
COPY poetry.lock .
RUN POETRY_VIRTUALENVS_CREATE=false poetry install 

COPY HW_4 HW_4

EXPOSE 8000
CMD ["uvicorn", "HW_4.demo_service.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
