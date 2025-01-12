FROM ubuntu:latest

WORKDIR /app

COPY app.py /app

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y python3 python3-pip python3-venv 
RUN python3 -m venv venv
RUN /bin/bash -c "source venv/bin/activate && pip install flask requests"

CMD ["venv/bin/python", "/app.py"]
