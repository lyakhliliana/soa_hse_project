FROM python:3.10

WORKDIR /content_service

COPY .  content_service

RUN pip install --no-cache-dir --upgrade -r content_service/requirements.txt

ENV PYTHONPATH /content_service

EXPOSE 50051

CMD [ "python", "content_service/src/api.py" ]