FROM mvertes/alpine-mongo:latest

RUN apk add --no-cache py-pip
ADD requirements.txt  /requirements.txt
RUN pip install -r requirements.txt
ADD run.py /run.py
VOLUME ["/data"]
EXPOSE 5000
ENTRYPOINT [ "/usr/bin/python", "run.py" ]
