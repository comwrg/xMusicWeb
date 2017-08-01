# coding=utf-8
'''
@author: comwrg
@license: MIT
@time : 2017/05/21 20:21
@desc : 
'''
import os, json
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
@app.route('/convert.html')
def main():
    return render_template('convert.html')


@app.route('/convert', methods=['POST'])
def convert():
    url = request.form['url']
    kwl = NetEaseMusic.getKwl(url)
    if not kwl:
        return redirect(url_for('convert'))
    res = make_response(kwl)
    res.headers["Content-Disposition"] = "attachment; filename=guys.kwl"
    return res


@app.route('/diff.html')
def diff_html():
    return render_template('diff.html')


@app.route('/diff', methods=['POST'])
def diff():
    url1 = request.form['url1']
    url2 = request.form['url2']
    diff1, diff2 = NetEaseMusic.diff(url1, url2)

    def pack(diff):
        l = []
        i = 0
        for data in diff:
            i += 1
            l.append({
                'id'    : i,
                'song'  : data[0],
                'singer': data[1],
                'album' : data[2]
            })
        return l

    # onlysamesongname: only same song name but diff album or singer
    onlysamesongname = []
    i = 0
    for data1 in diff1[:]:
        lista = []
        listb = []
        songname = ''
        for data2 in diff2[:]:
            # if song name equal, add to list
            if data1[0] == data2[0]:
                songname = data1[0]
                lista.append(data1)
                listb.append(data2)
                # remove song of the same song
                # why use try because data1 will be deleted in first cycle
                try:
                    diff1.remove(data1)
                    diff2.remove(data2)
                except:
                    pass
        if songname:
            i += 1
            onlysamesongname.append({
                'id'       : i,
                'songname' : songname,
                'songlista': lista,
                'songlistb': listb
            })

    return json.dumps([pack(diff1), pack(diff2), onlysamesongname])


if __name__ == '__main__':
    app.run(debug=True)
