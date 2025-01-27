FROM python:3.10-slim
RUN mkdir /app
COPY requirements.txt /app
COPY demo.py /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "demo.py"]