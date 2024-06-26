FROM python:3.9-slim
WORKDIR /
COPY . .
RUN pip install -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "$PORT"]