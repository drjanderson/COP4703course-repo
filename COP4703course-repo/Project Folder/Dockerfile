# Use the official Python image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy dependency list
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Run the Session #2 Python program
CMD ["python", "session2_correct_syntax.py"]