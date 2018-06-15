import pathlib

import pytest


class Basetest(object):
    provider = ""
    newestResource = ''
    sceneResource = ''

    providerName = "BrattySis.com"
    providerUrl = "http://brattysis.com"

    num_of_newest = 16
    newest_title = "Slip It In - S5:E2"
    newest_url = "http://brattysis.com/video/watch/56984/slip-it-in-s5e2"
    newest_rlsdate = "Apr 20, 2018"
    newest_site = providerName

    sample_description = """Lana Rhoades is annoyed that her stepbrother Tony pissed all over the toilet seat. She demands that he clean the pee up, including what's on her big ass. He is totally turned on by his stepsister's bottom. While Lana's back is turned, he starts jacking off. Pulling her closer, he gets his stepsister close enough to slip it into her greedy twat. Lana can't help but ride her stepbrother's stiffie once she realizes how good it feels.
Turning around, Lana whips out her big tits for Tony to enjoy. Soon she's on her knees sucking him off with her puffy lips before she climbs aboard once again. Her trimmed snatch is nice and creamy as she keeps her hips in motion bouncing up and down while her knockers jiggle. Tony can't get enough, especially once Lana flips over and lets him be in control.
Bringing her knees up to her chin, Lana opens herself wide for Tony to pound her pussy while rubbing her clit. Then she gets on her knees so he can bring her home with a big climax. Shoving her giant boobs together, she gives her stepbrother the perfect landing spot for his cum shot as Tony jacks himself off to the enticing sight of his stepsister's breasts."""
    sample_cast = "Lana Rhoades"
    sample_cast_num = 1
    sample_title_cast = "[BrattySis] Lana Rhoades: Slip It In - S5:E2"
    sample_title = "[BrattySis] Slip It In - S5:E2"
    sample_covers = [{'url': '',
                      'type': 'front'}]

    @pytest.fixture()
    def providerObject(self):
        dataproviderObject = self.provider()
        return dataproviderObject

    @pytest.fixture(scope="class")
    def soupnewest(self):
        from bs4 import BeautifulSoup
        resourcefolder = pathlib.Path(__file__).parent / 'resources'
        with open(str(resourcefolder / self.newestResource), 'r') as file:
            htmlSource = file.read()
        soup = BeautifulSoup(htmlSource, 'html.parser')
        return soup

    @pytest.fixture(scope="class")
    def soupscene(self):
        from bs4 import BeautifulSoup
        resourcefolder = pathlib.Path(__file__).parent / 'resources'
        with open(str(resourcefolder / self.sceneResource), 'r') as file:
            htmlSource = file.read()
        soup = BeautifulSoup(htmlSource, 'html.parser')
        yield soup
        soup = ""

    def test_Name(self, providerObject):
        assert providerObject.getName() == self.providerName

    def test_url(self, providerObject):
        assert providerObject.baseurl == self.providerUrl

    def test_parseNewest(self, providerObject, soupnewest):
        NewestEntries = providerObject.parseNewestEntries(soupnewest)
        assert len(NewestEntries) == self.num_of_newest
        assert NewestEntries[0]['title'] == self.newest_title
        assert NewestEntries[0]['url'] == self.newest_url
        assert NewestEntries[0]['rlsdate'] == self.newest_rlsdate
        assert NewestEntries[0]['site'] == self.newest_site

    def test_getDescription(self, providerObject, soupscene):
        description = providerObject.getDescription(soupscene)
        assert description == self.sample_description

    def test_getCast(self, providerObject, soupscene):
        cast = providerObject.getCast(soupscene)
        assert len(cast) == self.sample_cast_num
        if len(cast) > 0:
            assert cast[0] == self.sample_cast

    def test_buildTitlewithCast(self, providerObject, soupscene):
        cast = [self.sample_cast, ]
        title = providerObject.buildTitle(soupscene, cast)
        assert title == self.sample_title_cast

    def test_buildTitlewithoutCast(self, providerObject, soupscene):
        cast = []
        title = providerObject.buildTitle(soupscene, cast)
        assert title == self.sample_title

    def test_getCovers(self, providerObject, soupscene):
        covers = providerObject.getCovers(soupscene)
        assert len(covers) == len(self.sample_covers)
        assert covers == self.sample_covers

    def test_liveVersion(self, providerObject):
        NewestEntries = providerObject.getNewestEntries()
        assert len(NewestEntries) == self.num_of_newest

    def test_liveCover(self, providerObject):
        response, content = providerObject.getUrl(providerObject.getNewestEntries()[0]['url'])
        if response:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(content, 'html.parser')

            covers = providerObject.getCovers(soup)
            assert len(covers) == len(self.sample_covers)