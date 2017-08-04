apt-get install gunicorn
pip install -r requirements.txt
gunicorn run:app -p run.pid -b 0.0.0.0:5000 -D