from bs4 import BeautifulSoup

from Dataproviders.Dataprovider import Dataprovider


class Tushy(Dataprovider):

    baseurl = "https://www.tushy.com"
    newestUrl = "%s/videos" %(baseurl)
    metadataurl = ""

    providerPrefix = 'Tushy'

    containedsites = ["Tushy"]

    def getName(self):
        return "Tushy.com"


    def getNewestEntries(self):
        result, content = self.getUrl(self.newestUrl)

        if result:
            soup = BeautifulSoup(content, 'html.parser')
            return self.parseNewestEntries(soup)

    def parseNewestEntries(self, soup):
        Entries = []
        newestScenePreviews = soup.select("article")
        for scene in newestScenePreviews:

            linkElement =scene.select("h3.videolist-panel-caption-title > a")[0]
            caption = linkElement.text
            url = linkElement['href']

            dateElement = scene.select("div.videolist-panel-caption-video-info > ul > li.videolist-panel-caption-video-info-item > span.videolist-panel-caption-video-info-data")
            date = dateElement[0].text
            Entries.append({'title': caption,
                            'url': "%s%s" % (self.baseurl, url),
                            'rlsdate' : date,
                            'site': self.getName()})
        self.Entries = Entries
        return Entries

    def getDescription(self, soup):
        descriptionElement1 = soup.select("span.moreless")
        return descriptionElement1[0].text

    def getCast(self, soup):
        cast = []
        actorElements = soup.select("#castme-subtitle > a")
        for actor in actorElements:
            cast.append(actor.text)
        return cast

    def getCovers(self, soup):
        covers = []
        frontCoverElement = soup.select("img.player-img")
        coverUrl = frontCoverElement[0]['src']
        covers.append({'url': coverUrl,
                       'type': 'front'})
        return covers

    def updateProviderprefix(self, soup, subsite=None):
        pass

    def buildTitle(self, soup, cast):
        titleElement = soup.select("h1.caption-title > a")
        title = titleElement[0].text
        if len(cast) > 0:
            return "[%s] %s: %s" % (self.providerPrefix, cast[0], title)
        else:
            return "[%s] %s" % (self.providerPrefix, title)
