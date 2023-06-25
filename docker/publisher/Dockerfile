FROM python:3 

WORKDIR /src 

COPY ./client ./client

COPY requirements.txt .

RUN pip install --no-cache-dir -r ./requirements.txt

CMD ["python", "client/publisher.py"]
# ENTRYPOINT ["tail"]
# CMD ["-f","/dev/null"]
