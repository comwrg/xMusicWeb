FROM debian

WORKDIR /xMusicWeb
ADD . /xMusicWeb

RUN apt-get update && apt-get install -y gunicorn python-pip
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "run:app", "-b", "0.0.0.0:5000"]
# CMD ["python", "run.py"]

# usage
# docker build xMusicWeb -t xmw/1.0
# docker run -d -p 5000:5000 xmw:1.0