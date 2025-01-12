FROM python:3.8-slim
WORKDIR /app
COPY app.py /app
RUN pip install flask requests
CMD ["python", "app.py"]
