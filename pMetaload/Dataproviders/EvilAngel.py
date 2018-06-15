from bs4 import BeautifulSoup

from Dataproviders.Dataprovider import Dataprovider


class EvilAngelMovies(Dataprovider):

    baseurl = "https://www.evilangel.com"
    newestUrl = "%s/en/movies" %(baseurl)
    metadataurl = ""
    providerPrefix = "EvilAngel"

    containedsites = ['Evilangel']

    def getName(self):
        return "EvilAngel.com Movies"


    def getNewestEntries(self):
        result, content = self.getUrl(self.newestUrl)

        if result:
            soup = BeautifulSoup(content, 'html.parser')
            return self.parseNewestEntries(soup)

    def parseNewestEntries(self, soup):
        Entries = []
        newestScenePreviews = soup.select("div.tlcContentPage  > div.tlcItem")
        for scene in newestScenePreviews:

            linkElement =scene.select("div.tlcTitle > a")[0]
            caption = linkElement['title']
            url = linkElement['href']
            dateElement = scene.select(".tlcDetailsValue")
            date = dateElement[0].text
            Entries.append({'title': caption,
                            'url': "%s%s" % (self.baseurl, url),
                            'rlsdate' : date,
                            'site': self.getName()})
        self.Entries = Entries
        return Entries

    def getDescription(self, soup):
        descriptionElement = soup.select("p.descriptionText")
        return descriptionElement[0].text

    def getCast(self, soup):
        cast = []
        actorElements = soup.select("ul.actorList > li.pornstar")
        for actor in actorElements:
            nameElement = actor.select("div.pornstarNameBox > a.pornstarName")
            cast.append(nameElement[0].text)
        return cast

    def getCovers(self, soup):
        covers = []
        frontCoverElement = soup.select("a.frontCoverImg")
        frontCoverUrl = frontCoverElement[0]['href']
        covers.append({'url': frontCoverUrl,
                       'type': 'front'})

        backCoverElement = soup.select("a.backCoverImg")
        backCoverUrl = backCoverElement[0]['href']
        covers.append({'url': backCoverUrl,
                       'type': 'back'})

        return covers

    def updateProviderprefix(self, soup, subsite=None):
        pass

    def buildTitle(self, soup, cast):
        titleElement = soup.select("h3.dvdTitle")
        title = titleElement[0].text
        return "[%s] %s" % (self.providerPrefix, title)
