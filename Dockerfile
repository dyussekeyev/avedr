FROM python:3.8-slim
WORKDIR /app
COPY app.py /app
RUN pip install flask
RUN pip install requests
RUN pip install mwdblib
CMD ["python", "app.py"]
