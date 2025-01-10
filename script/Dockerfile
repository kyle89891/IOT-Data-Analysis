# Step 1: Use an official Python runtime as the base image
FROM python:3.9-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy the current directory contents into the container at /app
COPY . /app

# Step 4: Install any needed dependencies (use requirements.txt if needed)
RUN pip install --no-cache-dir -r requirements.txt


# Step 5: Run the Python script
CMD ["python", "Explore_Data.py"]
