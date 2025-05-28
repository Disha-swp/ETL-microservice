# Use Python base image
FROM python:3.13

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port and run app
ENV PORT=8080
CMD ["python", "main.py"]
