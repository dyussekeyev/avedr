FROM ubuntu:latest

WORKDIR /app

COPY scan.py /app

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y xcb python3 python3-pip python3-venv python3-pip wget 
RUN python3 -m venv venv
RUN . venv/bin/activate
RUN pip install flask
RUN wget https://devbuilds.s.kaspersky-labs.com/kvrt_linux/latest/kvrt.run
RUN chmod +x ./kvrt.run

CMD ["venv/bin/python", "/app/scan.py"]
