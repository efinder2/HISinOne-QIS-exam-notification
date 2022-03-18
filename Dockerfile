# About my dockerfile
# directive=value
FROM python:latest
RUN mkdir /data
VOLUME ["/data"]

RUN mkdir /workingdir

RUN apt-get update

COPY configuration.py /workingdir/
COPY crawl.py /workingdir/
COPY notenliste.py /workingdir/
COPY notifier.py /workingdir/
COPY requirements.txt /workingdir/
COPY test.py /workingdir/
COPY Docker/run.sh /workingdir/




RUN pip install -r /workingdir/requirements.txt

ENTRYPOINT ["/workingdir/run.sh"]


