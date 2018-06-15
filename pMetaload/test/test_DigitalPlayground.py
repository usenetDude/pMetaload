from Dataproviders.DigitalPlayground import DigitalPlayground

from .basetest import Basetest


class TestDigitalPlayground(Basetest):
    provider = DigitalPlayground
    newestResource = 'DigitalPlayground.com Movies_newest.html'
    sceneResource = 'DigitalPlayground.com Movies_scene.html'

    providerName = "DigitalPlayground.com Movies"
    providerUrl = "https://www.digitalplayground.com"

    num_of_newest = 20
    newest_title = "Poon Raider: A DP XXX Parody"
    newest_url = "https://www.digitalplayground.com/movies/info/2301593/poon-raider-a-dp-xxx-parody/"
    newest_rlsdate = "14 March, 2018"
    newest_site = providerName

    sample_description = """After the death of her father, Laura Crotch arrives home to acquire Crotch Industries only to find out that her stepmother, the new Mrs. Crotch, has a different plan for the company. On the hunt to retrieve her father’s rare artifact, Laura learns that her sidekick, Rina, and Mrs. Crotch’s assistant, Ryan, are working against her with the hopes of acquiring the same rare artifact. After an epic battle of wills, Laura comes out victorious… and covered in cum!"""
    sample_cast = "Kimmy Granger"
    sample_cast_num = 5
    sample_title_cast = "[DigitalPlayground] Poon Raider: A DP XXX Parody"
    sample_title = "[DigitalPlayground] Poon Raider: A DP XXX Parody"
    sample_covers = [{'url': 'https://photo-stream-ht.dplaygroundcontent.com/content/videos/2301593/imgs/artwork_front/504x711_1.jpg',
                      'type': 'front'},
                     {
                         'url': 'https://photo-stream-ht.dplaygroundcontent.com/content/videos/2301593/imgs/artwork_back/504x711_2.jpg',
                         'type': 'back'}
                     ]