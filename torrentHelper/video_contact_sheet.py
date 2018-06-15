import subprocess
from pathlib import Path
import platform

path_to_amt = """C:\Program Files (x86)\AMT\AMT.exe"""
vcs_command = """vcs"""

def createSheet(videoFile):

    if platform.system() == 'win32':
        subprocess.call([path_to_amt, str(videoFile)])

    elif platform.system() == 'Linux':
        subprocess.call([vcs_command, '-p', 'pbay', '-o', '%s.jpg'%(str(videoFile)), str(videoFile)])
    else:
        print("what is this system?")
        return None

    contactsheet = Path("%s.jpg" % (videoFile))
    if contactsheet.is_file():
        return contactsheet.absolute()
    else:
        return None