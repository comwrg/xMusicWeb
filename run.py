# coding=utf-8
'''
@author: comwrg
@license: MIT
@time : 2017/05/21 20:21
@desc : 
'''
import os
from flask import Flask, render_template, request, make_response, flash, redirect, url_for, send_from_directory
from werkzeug.contrib.fixers import LighttpdCGIRootFix

import NetEaseMusic

app = Flask(__name__)
app.secret_key = 'super secret key'

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

app.wsgi_app = LighttpdCGIRootFix(app.wsgi_app)
@app.route('/')
def main():
    return render_template('convert.html')

@app.route('/', methods=['POST'])
def convert():
    url = request.form['url']
    kwl = NetEaseMusic.getKwl(url)
    if kwl == False:
        return redirect(url_for('convert'))
    res = make_response(kwl)
    res.headers["Content-Disposition"] = "attachment; filename=guys.kwl"
    return res

if __name__ == '__main__':
    app.run(debug=True)
