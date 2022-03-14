# About my dockerfile
# directive=value
FROM python:latest
RUN mkdir /data
VOLUME ["/data"]

RUN mkdir /workingdir

# Cron stuff from https://stackoverflow.com/questions/37458287/how-to-run-a-cron-job-inside-a-docker-container
RUN apt-get update && apt-get -y install cron
COPY Docker/crontab /etc/cron.d/crawl_tab
RUN chmod 0644 /etc/cron.d/crawl_tab
RUN crontab /etc/cron.d/crawl_tab
RUN touch /etc/cron.d/crawl_tab

COPY configuration.py /workingdir/
COPY crawl.py /workingdir/
COPY notenliste.py /workingdir/
COPY notifier.py /workingdir/
COPY requirements.txt /workingdir/
COPY test.py /workingdir/
COPY Docker/run.sh /workingdir/




RUN pip install -r /workingdir/requirements.txt

ENTRYPOINT ["/workingdir/run.sh"]


