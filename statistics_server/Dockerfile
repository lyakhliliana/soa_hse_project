FROM python:3.10

WORKDIR /statistics_server

COPY .  statistics_server

RUN pip install --no-cache-dir --upgrade -r statistics_server/requirements.txt

EXPOSE 8040

CMD ["uvicorn", "statistics_server.src.api:app", "--host", "0.0.0.0", "--port", "8040"]