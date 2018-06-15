import sys
import pathlib
import git
import os
from gui.app import app


def updateScripts():
    scriptPath = pathlib.Path(__file__)
    scriptFolder = scriptPath.absolute().parent
    print("Checking for updates... running from %s"%(str(scriptFolder)))
    #try to "pull" repo
    repository = git.Repo(path=str(scriptFolder))
    origin = repository.remotes.origin
    result = origin.pull()
    if result[0].flags == 64:
        print("Pull ok, fast forward!")
        os.execl(sys.executable, *([sys.executable] + sys.argv))
    elif result[0].flags == 4:
        print("We are up to date!")
    else:
        print(result[0].flags)


if __name__ == '__main__':
    #dont run updates in docker
    #updateScripts()
    app.run(host='0.0.0.0', debug=True)
    #myApp = pMetaLoadApplication()
    #myApp.run()