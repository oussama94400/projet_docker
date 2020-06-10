FROM python:3-alpine
WORKDIR .
MAINTAINER python
COPY envoi_csv.py ./
#RUN apt-get install python-pip3
RUN pip3 install cqlsh
RUN pip3 install cql
#RUN pip3 install python-csv  
RUN pip3 install cassandra-csv  
CMD ["python3", "envoi_csv.py"]
