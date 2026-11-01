FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN SECRET_KEY=build-only python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate --noinput && (python manage.py createsuperuser --noinput || true) && gunicorn dataproject.wsgi:application --bind 0.0.0.0:8000"]