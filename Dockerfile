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

# Step 5: Copy the requirements file to the container
COPY requirements.txt .

# Step 6: Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 7: Copy the project code to the container
COPY . .

RUN poetry install

# Step 8: Expose the Django application port
EXPOSE 8000

# Step 9: Run migrations and start the server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
