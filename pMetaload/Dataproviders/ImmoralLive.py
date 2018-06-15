from bs4 import BeautifulSoup

from Dataproviders.Dataprovider import Dataprovider


class ImmoralLive(Dataprovider):

    baseurl = "https://www.ImmoralLive.com"
    newestUrl = "%s/en/videos" %(baseurl)
    metadataurl = ""

    providerPrefix = 'ImmoralLive'

    containedsites = ['Immorallive']

    def getName(self):
        return "ImmoralLive.com"


    def getNewestEntries(self):
        result, content = self.getUrl(self.newestUrl)
        if result:
            soup = BeautifulSoup(content, 'html.parser')
            return self.parseNewestEntries(soup)

    def parseNewestEntries(self, soup):
        Entries = []
        newestScenePreviews = soup.select("ul.sceneList > li.scene")
        for scene in newestScenePreviews:

            linkElement =scene.select("h3.sceneTitle > a")[0]
            caption = linkElement.text
            url = linkElement['href']

            dateElement = scene.select("p.sceneDate")
            date = dateElement[0].text
            Entries.append({'title': caption.strip(),
                            'url': "%s%s" % (self.baseurl, url),
                            'rlsdate' : date,
                            'site': self.getName()})
        self.Entries = Entries
        return Entries

    def getDescription(self, soup):
        descriptionElement1 = soup.select("div.sceneDesc")
        description = descriptionElement1[0].text
        return description.replace("Video Description:", "").strip()

    def getCast(self, soup):
        cast = []
        actorElements = soup.select("span.slide-title")
        for actor in actorElements:
            cast.append(actor.text)
        return cast

    def getCovers(self, soup):
        covers = []
        for line in soup.get_text().split("\n"):
            if '"picPreview"' in line:
                splittedLine = line.split("https")
                splittedLine = splittedLine[1]
                splittedLine = splittedLine.split('"')
                splittedLine = splittedLine[0]
                splittedLine = splittedLine.replace('''\\/''', '''/''')
                splittedLine = "https%s" % (splittedLine)
                break
        covers.append({'url': splittedLine,
                       'type': 'front'})

        return covers

    def updateProviderprefix(self, soup, subsite=None):
        pass

    def buildTitle(self, soup, cast):
        titleElement = soup.select("h3.title")
        title = titleElement[0].text
        if len(cast) > 0:
            return "[%s] %s: %s" % (self.providerPrefix, cast[0], title)
        else:
            return "[%s] %s" % (self.providerPrefix, title)
