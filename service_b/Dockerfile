FROM python:3.12.3-slim

ENV USER=service-b-user \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN addgroup --system $USER && adduser --system --group $USER

ENV APP_DIR=/home/$USER/src

WORKDIR $APP_DIR

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . $APP_DIR

RUN chown -R "$USER":"$USER" $APP_DIR
USER $USER

CMD ["fastapi", "run", "main.py"]
