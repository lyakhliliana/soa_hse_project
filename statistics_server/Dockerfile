FROM python:3.10

WORKDIR /statistics_server

COPY .  statistics_server

RUN pip install --no-cache-dir --upgrade -r statistics_server/requirements.txt

ENV PYTHONPATH /statistics_server

EXPOSE 50052

CMD [ "python", "statistics_server/src/api.py" ]