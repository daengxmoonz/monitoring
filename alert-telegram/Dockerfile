FROM python:3.10-slim
WORKDIR /app
COPY app.py /app/app.py
RUN pip install --no-cache-dir flask requests
CMD ["python3", "app.py"]
