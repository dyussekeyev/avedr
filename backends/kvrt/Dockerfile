FROM ubuntu:latest
WORKDIR /app
COPY scan.py /app
RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y xcb python3 python3-pip python3-venv wget \
    && python3 -m venv venv \
    && /bin/bash -c "source venv/bin/activate && pip install flask" \
    && wget https://devbuilds.s.kaspersky-labs.com/kvrt_linux/latest/kvrt.run \
    && chmod +x ./kvrt.run
CMD ["venv/bin/python", "/app/scan.py"]
