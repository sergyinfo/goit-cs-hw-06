# Use the official Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose ports for web and socket servers
EXPOSE 3000
EXPOSE 5000

# Command to run the main script (which starts both web and socket servers)
CMD ["python", "main.py"]
