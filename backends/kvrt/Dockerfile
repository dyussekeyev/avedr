FROM ubuntu:latest
WORKDIR /app
COPY scan.py /app
RUN apt-get update && apt-get install -y python3 python3-pip python3-venv
RUN python3 -m venv venv
RUN . venv/bin/activate && pip install flask
CMD ["venv/bin/python", "/app/scan.py"]
