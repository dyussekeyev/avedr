FROM ubuntu:latest

WORKDIR /app

COPY scan.py /app
COPY update_av.sh /app
COPY check_av.sh /app

RUN apt-get update && apt-get upgrade -y
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata
RUN apt-get install -y clamav clamav-daemon python3 python3-pip python3-venv cron
RUN mkdir -p /var/run/clamav && chown clamav:clamav /var/run/clamav
RUN freshclam
RUN python3 -m venv venv
RUN /bin/bash -c "source venv/bin/activate && pip install flask"
RUN chmod +x /app/update_av.sh /app/check_av.sh
RUN echo "0 0 * * * /app/update_av.sh" >> /etc/crontab
RUN echo "*/5 * * * * /app/check_av.sh" >> /etc/crontab

# Ensure cron is started
CMD ["sh", "-c", "service clamav-daemon restart && cron && venv/bin/python /app/scan.py"]
