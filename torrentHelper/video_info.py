from pymediainfo import MediaInfo

def getInformation(videoPath):
    videoInformation = {}
    media_info = MediaInfo.parse(videoPath)
    for track in media_info.tracks:
        if track.track_type == 'General':
            videoInformation['filesize'] = track.other_file_size[0]
            videoInformation['duration'] = track.other_duration[0]
        if track.track_type == 'Video':
            videoInformation['resolution'] = '%sx%s'%(track.width,track.height)

    return videoInformation