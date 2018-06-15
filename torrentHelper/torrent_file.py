import os

from dottorrent import Torrent

trackerUrl = os.getenv('ANNOUNCEURL', None)

def createTorrent(videoFile):
    torrent = Torrent(path=str(videoFile), trackers=[trackerUrl], private=True)
    print(torrent.get_info())
    print("Starting Torrent...")
    if torrent.generate(progressCallback) == True:
        print("Torrent generated succesful!")
        with open('%s.torrent'%(videoFile), 'wb') as file:
            torrent.save(file)

def progressCallback(filename, pieces_completed, pieces_total):
    percent = (pieces_completed/pieces_total)*100
    print("\rtorrent %s %d percent done" %(filename, percent), end='', flush=True)
