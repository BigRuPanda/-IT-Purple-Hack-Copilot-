FROM python:3.12

WORKDIR /usr/src/bot

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

VOLUME /data

CMD ["/bin/bash", "-c", "python ./bot/main.py"]