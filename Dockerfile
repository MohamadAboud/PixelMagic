# Use an official Python runtime as a parent image
FROM python:3.10-slim-buster

# Install required system dependencies
RUN apt-get update && apt-get install -y \
    git

# Set the working directory in the container
WORKDIR /app

# Install PyTorch
RUN pip install torch torchvision torchaudio

# Install the diffusers library
RUN pip install git+https://github.com/huggingface/diffusers.git

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of your application code
COPY . /app

# Expose the port that the streamlit app runs on
EXPOSE 8501

# Run the command to start your application
CMD ["streamlit", "run", "ui.py"]
