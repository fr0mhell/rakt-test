FROM python:3.11

WORKDIR /app

### Install GDAL and Python installation tools
RUN apt-get update --fix-missing && \
    apt-get install -y libpq-dev gdal-bin libgdal-dev && \
    pip install pip==23.3.1 pip-tools==7.3.0 setuptools==69.0.2 wheel==0.42.0 && \
    rm -rf /var/lib/apt/lists/* && \
    apt clean

### Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

### Run Django
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
