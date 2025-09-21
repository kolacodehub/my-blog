# 1. Use Python 3.13 (since your pyproject requires >=3.13)
FROM python:3.13-bullseye

# 2. Don’t buffer logs (important for Docker logs)
ENV PYTHONUNBUFFERED=1

# 3. Set working directory inside container
WORKDIR /code

# 4. Install Poetry
RUN pip install --no-cache-dir poetry

# 5. Copy only dependency files first (better caching)
COPY pyproject.toml poetry.lock ./

# 6. Install dependencies (no-root since this is not a library)
RUN poetry install --no-root

# 7. Copy the rest of your code
COPY . .

# Make sure entrypoint script is executable
RUN chmod +x /code/start-django.sh

# 8. Expose Django’s port
EXPOSE 8000

# 9. Run Django with Poetry
ENTRYPOINT ["/code/start-django.sh"]
