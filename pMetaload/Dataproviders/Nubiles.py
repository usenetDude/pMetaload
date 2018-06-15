from bs4 import BeautifulSoup

from Dataproviders.Dataprovider import Dataprovider


class Nubiles(Dataprovider):

    baseurl = "http://nubiles.net"
    newestUrl = "%s/video/gallery" %(baseurl)
    metadataurl = ""

    providerPrefix = 'Nubiles'

    containedsites = ['Nubiles.com']
    def getName(self):
        return "Nubiles.com"


    def getNewestEntries(self):
        result, content = self.getUrl(self.newestUrl)

        if result:
            soup = BeautifulSoup(content, 'html.parser')
            return  self.parseNewestEntries(soup)

    def parseNewestEntries(self, soup):
        Entries =  []
        newestScenePreviews = soup.select("div.thumbnail-grid")
        for scene in newestScenePreviews:

            linkElement =scene.select("figcaption > a.title")[0]
            caption = linkElement.text
            url = linkElement['href']

            dateElement = scene.select("span.date")
            date = dateElement[0].text
            Entries.append({'title': caption.strip(),
                            'url': "%s%s" % (self.baseurl, url),
                            'rlsdate' : date,
                            'site': self.getName()})
        self.Entries = Entries
        return Entries

    def getDescription(self, soup):
        descriptionElement1 = soup.select("div.video-description > article")
        return descriptionElement1[0].text.strip()

    def getCast(self, soup):
        cast = []
        actorElements = soup.select(".featuring-modelname > a")
        for actor in actorElements:
            cast.append(actor.text)
        return cast

    def getCovers(self, soup):
        covers = []
        frontCoverElement = soup.select(".video-js")
        # they use url with current protocol, build a full link
        # //images.nubiles.net/samples/...jpg
        coverUrl = "http:%s" % (frontCoverElement[0]['poster'])
        covers.append({'url': coverUrl,
                       'type': 'front'})
        return covers

    def updateProviderprefix(self, soup, subsite=None):
        pass

    def buildTitle(self, soup, cast):
        titleElement = soup.select("span.videotitle")
        title = titleElement[0].text
        if len(cast) > 0:
            return "[%s] %s: %s" % (self.providerPrefix, cast[0], title)
        else:
            return "[%s] %s" % (self.providerPrefix, title)
