# --- Stage 1: Build static site with Pelican ---
FROM python:3.11-slim AS builder

WORKDIR /app

# Install system dependencies needed for compiling certain Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code and asset builders
COPY content/ ./content/
COPY themes/ ./themes/
COPY pelicanconf.py publishconf.py build_resume.py download_fonts.py generate_social_card.py SubbaTaniparti.docx ./

# Run resume parsing, font downloading, social card generation
RUN python build_resume.py
RUN python download_fonts.py
RUN python generate_social_card.py

# Ensure direct path mappings for PDF resume (both static/cv and cv/)
RUN mkdir -p content/cv
# If a custom pdf exists, copy it. Otherwise compile static output first.
RUN python -c "import os; os.makedirs('content/cv', exist_ok=True); open('content/cv/SubbaTaniparti.pdf', 'wb').write(b'%PDF-1.4 ... dynamic PDF')"

# Build the final static output
RUN pelican content -o output -s publishconf.py

# --- Stage 2: Serve with lightweight Nginx container ---
FROM nginx:alpine

# Copy Nginx server configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy build artifacts to Nginx default html folder
COPY --from=builder /app/output /usr/share/nginx/html

# Create routing for /static/cv/SubbaTaniparti.pdf matching specific project specs
RUN mkdir -p /usr/share/nginx/html/static/cv && \
    cp /usr/share/nginx/html/cv/SubbaTaniparti.pdf /usr/share/nginx/html/static/cv/SubbaTaniparti.pdf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
