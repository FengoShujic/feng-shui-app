FROM python:3.9-alpine3.13
LABEL maintainer="Dzonzi"

# Onemogućava buffering outputa
ENV PYTHONUNBUFFERED 1

# Kopiranje potrebnih fajlova
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

# Definisanje ARG za razvojno okruženje
ARG DEV=false

# Instalacija zavisnosti
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client jpeg-dev && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev zlib zlib-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ "$DEV" = "true" ]; then /py/bin/pip install -r /tmp/requirements.dev.txt ; fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser --disabled-password --no-create-home django-user && \
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    chown -R django-user:django-user /vol && \
    chmod -R 755 /vol

# Postavljamo PATH da koristi virtual environment
ENV PATH="/py/bin:$PATH"

# **Dodajemo DATABASE_URL za Render**
ENV DATABASE_URL=${DATABASE_URL}

# Postavljamo korisnika
USER django-user

# Pokrećemo Gunicorn za produkciju
CMD ["gunicorn", "app.wsgi:application", "--bind", "0.0.0.0:8000"]
