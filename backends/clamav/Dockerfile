FROM ubuntu:latest

WORKDIR /app

COPY scan.py /app

RUN apt-get update && apt-get upgrade -y
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata
RUN apt-get install -y clamav clamav-daemon python3 python3-pip python3-venv
RUN mkdir -p /var/run/clamav && chown clamav:clamav /var/run/clamav
RUN freshclam
RUN clamd
RUN python3 -m venv venv
RUN /bin/bash -c "source venv/bin/activate && pip install flask"

CMD ["venv/bin/python", "/app/scan.py"]
