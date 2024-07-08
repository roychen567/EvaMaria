FROM python:3.10.8-slim-buster

# Update and install dependencies
RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y git

# Copy requirements file and install dependencies
COPY requirements.txt /requirements.txt
RUN pip install -U pip && pip install -U -r /requirements.txt

# Set working directory
WORKDIR /leo

# Copy the entire project
COPY . .

# Default command to run when the container starts
CMD ["python3", "bot.py"]
