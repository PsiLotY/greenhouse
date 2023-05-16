FROM python:3 

WORKDIR /src 

COPY calculator.py .

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "calculator.py"]