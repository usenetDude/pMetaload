from bs4 import BeautifulSoup

from Dataproviders.Dataprovider import Dataprovider


class SimplyAnal(Dataprovider):

    baseurl = "https://www.simplyanal.com"
    newestUrl = "%s/videos/?nats=" %(baseurl)
    metadataurl = ""

    providerPrefix = 'Simplyanal'

    containedsites = ['Simplyanal']

    def getName(self):
        return "Simplyanal.com"


    def getNewestEntries(self):
        result, content = self.getUrl(self.newestUrl)

        if result:
            soup = BeautifulSoup(content, 'html.parser')
            return self.parseNewestEntries(soup)

    def parseNewestEntries(self, soup):
        Entries = []
        newestScenePreviews = soup.select("div.updates-content > div.video-frame")
        for scene in newestScenePreviews:
            linkElement = scene.select("div.info-box-new > span.title-movie > a")[0]
            caption = linkElement.text
            url = linkElement['href']


            date = ""
            Entries.append({'title': caption.strip(),
                            'url': "%s" % url,
                            'rlsdate': date,
                            'site': self.getName()})
        self.Entries = Entries
        return Entries

    def getDescription(self, soup):
        ##Description
        descriptionElement1 = soup.select("div.movie-description")
        return descriptionElement1[0].text.strip()

    def getCast(self, soup):
        ##Cast
        cast = []
        actorElements = soup.select("div.movie-data > span.model-movie > b > a")
        for actor in actorElements:
            cast.append(actor.text)
        return cast

    def getCovers(self, soup):
        covers = []
        ##Covers
        frontCoverElement = soup.select("#video")

        coverUrl = frontCoverElement[0]['poster']
        covers.append({'url': coverUrl,
                       'type': 'front'})
        return covers

    def updateProviderprefix(self, soup, subsite=None):
        pass

    def buildTitle(self, soup, cast):
        titleElement = soup.select("div.header-title > h2")
        title = titleElement[0].text
        title = title.split(' in ')[1]
        if len(cast) > 0:
            return "[%s] %s: %s" % (self.providerPrefix, cast[0], title)
        else:
            return "[%s] %s" % (self.providerPrefix, title)
