# Use the official Python image from Docker Hub with Python 3.10
FROM python:3.10

# Update package lists and install ffmpeg
RUN apt update && apt install -y ffmpeg

# Set the working directory in the container
WORKDIR /code

# Copy the file with the requirements to the container
COPY ./requirements.txt /code/

COPY ./app/ /code/app/

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port 8501
EXPOSE 8501

# Define the command to run the Streamlit app
CMD ["streamlit", "run", "./app/main.py"]
