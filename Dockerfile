FROM python:3.14-rc as builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools wheel

RUN pip install -r requirements.txt

COPY ./scripts/ .
RUN rm requirements.txt

FROM builder

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.14/site-packages /usr/local/lib/python3.14/site-packages
COPY --from=builder /app/* .

CMD ["python", "main.py"]