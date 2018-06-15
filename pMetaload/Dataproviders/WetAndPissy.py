from bs4 import BeautifulSoup

from Dataproviders.Dataprovider import Dataprovider


class WetAndPissy(Dataprovider):

    baseurl = "https://www.wetandpissy.com"
    newestUrl = "%s/videos/?nats=" %(baseurl)
    metadataurl = ""

    providerPrefix = 'WetAndPissy'

    containedsites = ["Wetandpissy"]
    def getName(self):
        return "WetAndPissy.com"


    def getNewestEntries(self):
        result, content = self.getUrl(self.newestUrl)

        if result:
            soup = BeautifulSoup(content, 'html.parser')
            return self.parseNewestEntries(soup)

    def parseNewestEntries(self, soup):
        Entries = []
        newestScenePreviews = soup.select("div.updates-content > div.video-frame")
        for scene in newestScenePreviews:

            linkElement =scene.select("span.title-movie > a")[0]
            caption = linkElement.text
            url = linkElement['href']

            dateElement = scene.select("span.date")
            date = dateElement[0].text
            Entries.append({'title': caption,
                            'url': url,
                            'rlsdate' : date,
                            'site': self.getName()})
        self.Entries = Entries
        return Entries

    def getDescription(self, soup):
        descriptionElement1 = soup.select("div.movie-description")
        return descriptionElement1[0].text.strip()

    def getCast(self, soup):
        cast = []
        actorElements = soup.select("span.model-movie > b > a")
        for actor in actorElements:
            cast.append(actor.text)
        return cast

    def getCovers(self, soup):
        covers = []
        frontCoverElement = soup.select("#video")
        coverUrl = frontCoverElement[0]['poster']
        covers.append({'url': coverUrl,
                       'type': 'front'})
        return covers

    def updateProviderprefix(self, soup, subsite=None):
        pass

    def buildTitle(self, soup, cast):
        titleElement = soup.select("div.header-title > h2")
        title = titleElement[0].text.split('in')[-1].strip()
        if len(cast) > 0:
            return "[%s] %s: %s" % (self.providerPrefix, cast[0], title)
        else:
            return "[%s] %s" % (self.providerPrefix, title)
