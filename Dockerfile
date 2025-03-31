FROM python:3.9-slim

WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Simple test import
RUN python -c "from utils.formatters import format_story"

EXPOSE 7860

# Command to run the application
CMD ["python", "app.py", "--listen", "--port", "7860"]
