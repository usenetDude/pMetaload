from Dataproviders.Dataprovider import Dataprovider
from Dataproviders.MassageRooms import MassageRooms

newest = "https://www.fantasymassage.com/en/videos"
scene = "https://www.fantasymassage.com/en/video/Two-for-One-Special-Scene-01/131002"
name = "FantasyMassage.com"

dummyProvider = MassageRooms()

result, content = dummyProvider.getUrl(newest, selenium=False, wait=0)
if result:
    with open('%s_newest.html'%name, "w") as f:
        f.write(str(content))

result, content = dummyProvider.getUrl(scene, selenium=False, wait=0)
if result:
    with open('%s_scene.html'%name, "w") as f:
        f.write(str(content))