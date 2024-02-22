FROM python
RUN apt-get update && apt-get install -y openjdk-17-jdk gcc python3-dev
ADD autoeagler.py autoeagler.py
ADD config.json config.json
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
CMD [ "python3", "./autoeagler.py" ]
ENV TERM=xterm