FROM python:3.10

# We copy just the requirements.txt first to leverage Docker cache
COPY requirements.txt /
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /app
WORKDIR /app

ENTRYPOINT gunicorn -b :$PORT run:APP