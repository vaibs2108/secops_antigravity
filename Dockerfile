FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
COPY app/ ./app/
COPY .streamlit/ ./.streamlit/

RUN pip3 install -r requirements.txt

EXPOSE 8501

# HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENV PYTHONPATH=/app
ENV STREAMLIT_THEME_BASE="dark"
ENV STREAMLIT_THEME_PRIMARY_COLOR="#3B82F6"
ENV STREAMLIT_THEME_BACKGROUND_COLOR="#0F172A"
ENV STREAMLIT_THEME_SECONDARY_BACKGROUND_COLOR="#1E293B"
ENV STREAMLIT_THEME_TEXT_COLOR="#F8FAFC"

ENTRYPOINT ["streamlit", "run", "app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
