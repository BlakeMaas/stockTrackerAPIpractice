# Use official Python base image
FROM python:3.10-slim

# Accept build-time secret
ARG ALPHA_VANTAGE_API_KEY
ENV ALPHA_VANTAGE_API_KEY=$ALPHA_VANTAGE_API_KEY

# Set workdir
WORKDIR /app

# Copy files
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose default Streamlit port
EXPOSE 8501

# Run Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
