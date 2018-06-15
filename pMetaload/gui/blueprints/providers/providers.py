from Dataproviders import *
from Dataproviders.Dataprovider import Dataprovider

from flask import Blueprint, render_template, abort, request, session, url_for, redirect, jsonify

providers = Blueprint('providers', __name__, template_folder='templates')

providerlist = []
for subclass in Dataprovider.__subclasses__():
    instance = subclass()
    providerlist.append(instance)

allsites = []

for idx, provider in enumerate(providerlist):
    for site in provider.containedsites:
        allsites.append({'site':site,
                         'provideridx': idx})

@providers.route('/')
def providerlisting():
    providernames = []
    for idx, entry in enumerate(providerlist):
        providernames.append({'id': idx,
                              'name': entry.getName()})

    return render_template('providerlist.html', providernames=providernames)

@providers.route('/<int:id>')
def provideroverview(id):

    currentprovider = providerlist[id]
    newestscenes = []
    for idx, entry in enumerate(currentprovider.getNewestEntries()):
        newestscenes.append({'id': idx,
                              'scene': entry})

    return render_template('provideroverview.html', newestscenes=newestscenes, providerid=id)

@providers.route('/<int:id>/<path:url>')
def providerDownload(id, url):

    site = request.args.get('subsite')
    currentprovider = providerlist[id]

    path = session['currentdir']

    currentprovider.getMetadata(url=url, folder=path, subSite=site)

    return redirect( url_for('metadataeditor.loadmetadata'))

@providers.route('/search')
def searchprovider():
    #input = request.args.get('input')
    #if input is None:
    #    input = ''
    #result = [x for x in allsites if input in x['site'].lower()]
    #return jsonify(result)
    return render_template('search.html', elements=allsites)