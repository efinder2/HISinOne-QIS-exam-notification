FROM python:latest

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y cron
RUN mkdir /workingdir /data
COPY requirements.txt /workingdir/
COPY *.py /workingdir/
RUN pip install --no-input -r /workingdir/requirements.txt

COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
