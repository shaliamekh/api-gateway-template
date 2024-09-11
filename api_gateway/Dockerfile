FROM python:3.12.5-slim

ENV USER=api-gateway-user \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install --no-install-recommends -y \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && addgroup --system $USER && adduser --system --group $USER

ENV APP_DIR=/home/$USER/src

WORKDIR $APP_DIR

COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src $APP_DIR

ENV PYTHONPATH=$APP_DIR

RUN chown -R "$USER":"$USER" $APP_DIR
USER $USER

CMD ["fastapi", "run", "./drivers/rest/main.py", "--proxy-headers"]
