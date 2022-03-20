FROM python:3.8-slim-buster

ARG token
ARG db_url

ENV TOKEN=$token
ENV DATABASE_URL=$db_url

RUN pip install --upgrade pip

COPY . /bot

WORKDIR ./bot

RUN groupadd -r bot && useradd -r -g bot bot && su bot

RUN  pip install --no-cache-dir -r requirements.txt

EXPOSE 80

CMD ["python", "bot.py"]