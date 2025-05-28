FROM python:3.10-slim

ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /usr/app

# System dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    git \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

# Install dbt and plugins
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy DBT project into image (not best practice, optional)
# COPY . /usr/app

CMD ["tail", "-f", "/dev/null"]
