FROM python:3.8

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY api .
WORKDIR ./api
CMD [ "python", "endpoint.py" ]

HEALTHCHECK --timeout=5s CMD curl --silent --fail http://127.0.0.1:5001/
