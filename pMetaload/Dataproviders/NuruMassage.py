from bs4 import BeautifulSoup

from Dataproviders.Dataprovider import Dataprovider


class NuruMassage(Dataprovider):

    baseurl = "https://www.nurumassage.com"
    newestUrl = "%s/en/videos" %(baseurl)
    metadataurl = ""

    providerPrefix = 'NuruMassage'

    containedsites = ['Nurumassage']

    def getName(self):
        return "NuruMassage.com"


    def getNewestEntries(self):
        Entries = []
        result, content = self.getUrl(self.newestUrl)

        if result:
            soup = BeautifulSoup(content, 'html.parser')
            return self.parseNewestEntries(soup)

    def parseNewestEntries(self, soup):
        Entries = []
        newestScenePreviews = soup.select("div.tlcContentPage  > div.tlcItem")
        for scene in newestScenePreviews:
            linkElement = scene.select("div.tlcTitle > a")[0]
            caption = linkElement['title']
            url = linkElement['href']
            dateElement = scene.select("span.tlcSpecsDate > span.tlcDetailsValue")
            date = dateElement[0].text
            Entries.append({'title': caption,
                            'url': "%s%s" % (self.baseurl, url),
                            'rlsdate': date,
                            'site': self.getName()})
        self.Entries = Entries
        return Entries

    def getDescription(self, soup):
        descriptionElement1 = soup.select("div.sceneDesc")
        description = descriptionElement1[0].text
        return description.replace("Video Description:", "").strip()

    def getCast(self, soup):
        cast = []
        actorElements = soup.select("a.pornstarName")
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
        # they use url with current protocol, build a full link
        # //images.nubiles.net/samples/...jpg
        coverUrl = splittedLine
        covers.append({'url': coverUrl,
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
