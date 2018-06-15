from bs4 import BeautifulSoup

from Dataproviders.Dataprovider import Dataprovider


class MassageRooms(Dataprovider):

    baseurl = "https://www.massagerooms.com"
    newestUrl = "%s/tour/videos/" %(baseurl)
    metadataurl = ""

    providerPrefix = 'MassageRooms'

    containedsites = ['MassageRooms']

    def getName(self):
        return "MassageRooms.com"


    def getNewestEntries(self):
        Entries = []
        result, content = self.getUrl(self.newestUrl)

        if result:
            soup = BeautifulSoup(content, 'html.parser')
            return self.parseNewestEntries(soup)

    def parseNewestEntries(self, soup):
        Entries = []
        newestScenePreviews = soup.select("article.release-card.scene")
        for scene in newestScenePreviews:
            linkElement = scene.select("div.card-title > a")[0]
            caption = linkElement['title']
            url = linkElement['href']
            dateElement = scene.select("div.release-date")[0]
            date = dateElement.text
            Entries.append({'title': caption,
                            'url': "%s%s" % (self.baseurl, url),
                            'rlsdate': date,
                            'site': self.getName()})
        self.Entries = Entries
        return Entries

    def getDescription(self, soup):
        descriptionElement1 = soup.select("div.expandable > p")
        description = descriptionElement1[0].text
        return description.strip()

    def getCast(self, soup):
        cast = []
        actorElements = soup.select("div.paper-tiles > article.tag-card > a[href^=/tour/model]")
        for actor in actorElements:
            cast.append(actor.text.strip())
        return cast

    def getCovers(self, soup):
        covers = []
        playerElement = soup.select("#player")[0]
        splittedLine = playerElement['style'].split('url(')[1]
        splittedLine = splittedLine.split(');')[0]

        # they use url with current protocol, build a full link
        # //images.nubiles.net/samples/...jpg
        coverUrl = "https:%s"%splittedLine
        covers.append({'url': coverUrl,
                       'type': 'front'})
        return covers

    def updateProviderprefix(self, soup, subsite=None):
        pass

    def buildTitle(self, soup, cast):
        titleElement = soup.select("header.release-title > h1")
        title = titleElement[0].text
        if len(cast) > 0:
            return "[%s] %s: %s" % (self.providerPrefix, cast[0], title)
        else:
            return "[%s] %s" % (self.providerPrefix, title)
