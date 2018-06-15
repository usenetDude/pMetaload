import io
import pathlib
from datetime import datetime
import subprocess

from flask import Blueprint, render_template, abort, request, session, send_file, redirect, url_for

metadataeditor = Blueprint('metadataeditor', __name__, template_folder='templates')


@metadataeditor.route('/update', methods=['POST'] )
def saveTitle():
    if 'titleInput' in request.form:
        title = request.form['titleInput']
        saveFile(title, "title")
    if 'castInput' in request.form:
        cast = request.form['castInput']
        saveFile(cast, "cast")
    if 'descriptionInput' in request.form:
        description = request.form['descriptionInput']
        saveFile(description, "description")
    return redirect(url_for('metadataeditor.loadmetadata'))

@metadataeditor.route('/torrent', methods=['POST'] )
def saveTorrent():

    path = pathlib.Path(session['currentdir'])
    for file in path.glob("*.mp4"):
        subprocess.Popen("torrentHelper %s &>log.txt" %(str(file)), shell=True).wait()
    for file in path.glob("*.avi"):
        subprocess.Popen("torrentHelper %s &>log.txt" %(str(file)), shell=True).wait()

    return redirect(url_for('metadataeditor.loadmetadata'))


@metadataeditor.route('/')
def loadmetadata():
    path = pathlib.Path(session['currentdir'])

    title = openFile('title')
    description = openFile('description')
    cast = openFile('cast')
    output = openFile('output')

    log = openFile('log')

    covers = []
    if (path / pathlib.Path("front.jpg")).exists():
        covers.append('front')
    if (path / pathlib.Path("back.jpg")).exists():
        covers.append('back')
    return render_template('metadataeditor.html', title=title, description=description, cast=cast,
                           covers=covers, output=output, log=log)

@metadataeditor.route('/img<string:type>')
def loadCover(type):
    path = pathlib.Path(session['currentdir']) / pathlib.Path('%s.jpg' % type)

    with open("%s"%str(path), 'rb') as f:
        filedata = f.read()
        return send_file(io.BytesIO(filedata), mimetype='image/jpg')

def openFile(filename):
    path = pathlib.Path(session['currentdir'])

    path = path / pathlib.Path("%s.txt" % filename)
    if path.exists():
        with open(str(path), 'r') as f:
            return f.read()
    else:
        return ''

def saveFile(text, file):
    path = pathlib.Path(session['currentdir'])
    path = path / pathlib.Path("%s.txt" % file)
    with open(str(path), "w") as f:
            f.write(text)