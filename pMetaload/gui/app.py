from flask import Flask, abort, render_template, session, request
from .blueprints.browse.browse import browsing

from .blueprints.providers.providers import providers
from .blueprints.metadata.metadata import metadataeditor
from .configuration import Config
import pathlib
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'im the secret key key'
app.config.from_object(Config)
app.register_blueprint(browsing, url_prefix='/browse')
app.register_blueprint(providers, url_prefix='/providers')
app.register_blueprint(metadataeditor, url_prefix='/metadata')

@app.route('/')
def home():
    if 'currentdir' in session:
        session.pop('currentdir' , None)
    return render_template('home.html')

if __name__ == '__main__':
    app.run()
