# Step 1: Use an official Python runtime as a parent image
FROM python:3.11-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    libpq-dev \
    gcc \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Step 4: Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Step 5: Copy project files to the container
COPY . .

# Step 6: Install dependencies using Poetry (without creating a virtual environment)
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

# Step 7: Expose the Django application port
EXPOSE 8000

# Step 8: Run migrations and start the server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
