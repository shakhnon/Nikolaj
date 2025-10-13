# Stage 1: Build the application with Poetry and install dependencies
FROM python:3.10-slim as builder

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y curl build-essential

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Copy Poetry config and project files
COPY pyproject.toml poetry.lock ./

# Install project dependencies (no-root to avoid unnecessary installs)
RUN poetry install --no-root --no-interaction --no-ansi

# List installed packages for debugging
RUN poetry show

# Copy application source code to the build container
COPY bot_telega_nikolaj ./bot_telega_nikolaj

# Stage 2: Create a smaller runtime container
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy only the installed dependencies from the builder stage
COPY --from=builder /root/.local /root/.local
COPY --from=builder /app /app

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Run the bot
CMD ["poetry", "run", "python", "bot_telega_nikolaj/bot_core.py"]


