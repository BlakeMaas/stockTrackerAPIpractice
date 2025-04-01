# Use official slim Python base image
FROM python:3.10-slim

# Set working directory in the container
WORKDIR /app

# Copy everything into the container
COPY . /app

# Install pip dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the port Streamlit runs on
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "main.py", "--server.enableCORS=false"]
