FROM python:3
WORKDIR /usr/src/app
RUN pip install pika redis simplejson
COPY code.py .
CMD ["python","-u","./code.py"]