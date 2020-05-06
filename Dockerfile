  
FROM python:3-alpine

WORKDIR /Users/octo/url-watcher-bot

ENV DOCKER 1

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python3", "./powerbot.py" ]
