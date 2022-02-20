# docker run --rm -it -p 8000:8000 $(docker build -q .)

FROM python:3.9.9-buster
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD uvicorn app:app --host=0.0.0.0 --port=8000
