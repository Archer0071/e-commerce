# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Copy all files into the container
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make scripts executable
RUN chmod +x /app/wait-for-it.sh

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run init_database.py with wait-for-it.sh
CMD ["sh", "-c", "ls /app && /app/wait-for-it.sh mysql:3306 -- python init_database.py"]
