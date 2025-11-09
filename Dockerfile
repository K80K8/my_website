# Use official Python image
FROM python:3.11-slim

# Set working directory in container
WORKDIR /app

# Copy only requirements first for caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your project
COPY . .

# Expose the port the app will run on
EXPOSE 10000

# Command to run your app
CMD ["python", "app.py"]
