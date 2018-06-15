from bs4 import BeautifulSoup

from Dataproviders.Dataprovider import Dataprovider


class FamilyStrokes(Dataprovider):

    baseurl = "https://www.familystrokes.com"
    newestUrl = "%s/scenes" %(baseurl)
    metadataurl = ""
    providerPrefix = "FamilyStrokes"

    containedsites = ['Familystrokes']

    def getName(self):
        return "FamilyStrokes.com"


    def getNewestEntries(self):
        result, content = self.getUrl(self.newestUrl)

        if result:
            soup = BeautifulSoup(content, 'html.parser')
            return self.parseNewestEntries(soup)

    def parseNewestEntries(self, soup):
        Entries = []
        newestScenePreviews = soup.select("table.scenes  > tbody > tr")
        for scene in newestScenePreviews:

            linkElement =scene.select("td > a")[0]
            url = linkElement['href']
            captionElement = scene.select("div.title > div.left-info > span")
            caption = captionElement[0].text

            dateElement = scene.select("div.scene-date")
            date = dateElement[0].text.strip()
            Entries.append({'title': caption,
                            'url': "%s" % (url),
                            'rlsdate' : date,
                            'site': self.getName()})
        self.Entries = Entries
        return Entries

    def getDescription(self, soup):
        descriptionElement = soup.select("div.scene-description > div.scene-story")
        return descriptionElement[0].text.strip()

    def getCast(self, soup):
        cast = []
        actorElements = soup.select("div.starring > span")
        for actor in actorElements:
            cast.append(actor.text)
        return cast

    def getCovers(self, soup):
        covers = []
        frontCoverElement = soup.select("#preview")
        coverUrl = frontCoverElement[0]['poster']
        covers.append({'url': coverUrl,
                       'type': 'front'})
        return covers

    def updateProviderprefix(self, soup, subsite=None):
        pass

    def buildTitle(self, soup, cast):
        titleElement = soup.select("span.d-inline-block")
        title = titleElement[0].text
        if len(cast) > 0:
            return "[%s] %s: %s" % (self.providerPrefix, cast[0], title)
        else:
            return "[%s] %s" % (self.providerPrefix, title)
