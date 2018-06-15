import argparse
import os
import pathlib
import shutil

from jinja2 import Environment, PackageLoader, select_autoescape

from torrent_file import createTorrent
from upload_img import upload_file_to_jerk
from video_contact_sheet import createSheet
from video_info import getInformation

env = Environment(
    loader=PackageLoader('torrentHelper', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    videoFile = pathlib.Path(args.filename)

    uploadData = []
    ##########################Information about Video##########################
    uploadData = getInformation(videoFile)

    ############################create Torrent File############################
    createTorrent(videoFile)
    ############################create Image Sheet#############################
    contactsheet = createSheet(videoFile)
    ############################upload Image#############################
    uploadData['videosheet'] = upload_file_to_jerk(str(contactsheet), only_url=False)
    frontcoverPath = videoFile.parent / 'front.jpg'
    if not frontcoverPath.is_file():
        frontcoverPath = videoFile.parent / 'front.gif'
    if frontcoverPath.is_file():
        uploadData['frontCover'] = upload_file_to_jerk(str(frontcoverPath), only_url=False)
    backcoverPath = videoFile.parent / 'back.jpg'
    if backcoverPath.is_file():
        uploadData['backCover'] = upload_file_to_jerk(str(backcoverPath), only_url=False)

    ############################get metadata#############################
    castPath = videoFile.parent / 'cast.txt'
    descriptionPath = videoFile.parent / 'description.txt'

    titlePath = videoFile.parent / 'title.txt'

    if castPath.is_file():
        with open(str(castPath), 'r') as file:
            uploadData['cast'] = file.read()
    if descriptionPath.is_file():
        with open(str(descriptionPath), 'r') as file:
            uploadData['description'] = file.read()
    if titlePath.is_file():
        with open(str(titlePath), 'r') as file:
            uploadData['title'] = file.read()
    ############################create Description#############################

    template = env.get_template('movie.txt')
    outputFile = videoFile.parent / 'output.txt'
    with open(str(outputFile), 'w') as file:
        template.stream(uploadData).dump(file)
    torrentDir = os.getenv('TORRENTPATH')
    if torrentDir is not None:
        torrentDir = pathlib.Path(torrentDir)
        shutil.copy(str(videoFile), str(torrentDir))
        print("Successfully copied file %s to torrentDir!" %(str(videoFile)))