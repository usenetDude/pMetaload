import pathlib
from datetime import datetime

from flask import Blueprint, render_template, abort, request, session, current_app

browsing = Blueprint('browsing', __name__, template_folder='templates')

@browsing.route('/', defaults = {'req_path': ''})
@browsing.route('/<path:req_path>')
def dir_browse(req_path, special=None):
    special= request.args.get('special')
    BASE_DIR = pathlib.Path(current_app.config['BROWSEROOT'])

    if 'currentdir' in session:
        path = pathlib.Path(session['currentdir']) / pathlib.Path(req_path)
    else:
        path = BASE_DIR / pathlib.Path(req_path)

    if 'currentdir' in session and special == 'up':
        if pathlib.Path(session['currentdir']) != BASE_DIR:
            path = pathlib.Path(session['currentdir']).parent

    if not path.exists():
        return abort(404)

    session['currentdir'] = str(path)

    dircontents = []
    for direntry in path.iterdir():
        if direntry.is_file():
            dircontents.append({'entry': direntry,
                                'type': 'file',
                                'date': datetime.fromtimestamp(direntry.stat().st_mtime)})
        elif direntry.is_dir():
            dircontents.append({'entry': direntry.parts[-1],
                                'type': 'directory',
                                'date': datetime.fromtimestamp(direntry.stat().st_mtime)})

    dircontents.sort(key=lambda x:x['date'], reverse=True)
    return render_template('browse.html', dircontent=dircontents)