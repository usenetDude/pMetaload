from bs4 import BeautifulSoup

from Dataproviders.Dataprovider import Dataprovider


class DigitalPlayground(Dataprovider):

    baseurl = "https://www.digitalplayground.com"
    newestUrl = "%s/movies/" %(baseurl)
    metadataurl = ""

    providerPrefix = 'DigitalPlayground'

    containedsites = ['Digitalplayground']

    def getName(self):
        return "DigitalPlayground.com Movies"


    def getNewestEntries(self):
        Entries = []
        result, content = self.getUrl(self.newestUrl)

        if result:
            soup = BeautifulSoup(content, 'html.parser')
            return self.parseNewestEntries(soup)

    def parseNewestEntries(self, soup):
        Entries = []
        newestScenePreviews = soup.select("article")
        for scene in newestScenePreviews:
            linkElement = scene.select("h4 > a")[0]
            caption = linkElement.text
            url = linkElement['href']

            dateElement = scene.select("div.info-left > span")
            date = dateElement[1].text
            Entries.append({'title': caption.strip(),
                            'url': "%s%s" % (self.baseurl, url),
                            'rlsdate': date,
                            'site': self.getName()})

        self.Entries = Entries
        return Entries

    def getDescription(self, soup):
        descriptionElement1 = soup.select("div.overview > p")
        return descriptionElement1[0].text.strip()

    def getCast(self, soup):
        cast = []
        actorElements = soup.select("div.model > div.title-bar > div.title-text > div > h4 a")
        for actor in actorElements:
            cast.append(actor.text)
        return cast

    def getCovers(self, soup):
        covers = []
        coverUrlElement = soup.select("#front-cover-hd")
        coverUrl = coverUrlElement[0]['src']
        coverUrl = "https:%s" % (coverUrl)
        covers.append({'url': coverUrl,
                       'type': 'front'})
        coverUrlElement = soup.select("#back-cover-hd")
        coverUrl = coverUrlElement[0]['src']
        coverUrl = "https:%s" % (coverUrl)
        covers.append({'url': coverUrl,
                       'type': 'back'})
        return covers

    def updateProviderprefix(self, soup, subsite=None):
        pass

    def buildTitle(self, soup, cast):
        titleElement = soup.select("header > h1")
        title = titleElement[0].text
        return "[%s] %s" % (self.providerPrefix, title)
