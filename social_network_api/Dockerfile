FROM python:3.10

WORKDIR /social_network_api

COPY .  social_network_api

RUN pip install --no-cache-dir --upgrade -r social_network_api/requirements.txt

EXPOSE 30

CMD ["uvicorn", "social_network_api.src.api:app", "--host", "0.0.0.0", "--port", "30"]