from bs4 import BeautifulSoup

from Dataproviders.Dataprovider import Dataprovider


class Fantasymassage(Dataprovider):

    baseurl = "https://www.fantasymassage.com"
    newestUrl = "%s/en/videos/" %(baseurl)
    metadataurl = ""

    providerPrefix = 'FantasyMassage'

    containedsites = ["Allgirlmassage", "Nurumassage", "Massageparlor", "Soapymassage", "Milkingtable", "Trickyspa"]
    def getName(self):
        return "Fantasymassage.com"


    def getNewestEntries(self):
        result, content = self.getUrl(self.newestUrl)

        if result:
            soup = BeautifulSoup(content, 'html.parser')
            return self.parseNewestEntries(soup)

    def parseNewestEntries(self, soup):
        Entries = []
        newestScenePreviews = soup.select("div.tlcItem")
        for scene in newestScenePreviews:

            linkElement =scene.select("div.tlcTitle > a")[0]
            caption = linkElement['title']
            url = linkElement['href']

            subsiteElement = scene.select("div.tlcSourceSite > span > a")[0]
            subsite = subsiteElement.text.strip()
            dateElement = scene.select("div.tlcSpecs > span.tlcSpecsDate > span.tlcDetailsValue")
            date = dateElement[0].text
            Entries.append({'title': caption.strip(),
                            'url': "%s%s" % (self.baseurl, url),
                            'rlsdate' : date,
                            'site' : subsite})
        self.Entries = Entries
        return Entries

    def getMetadata(self, url, folder=None, wait=0, subSite=None):
        super(Fantasymassage, self).getMetadata(url=url, folder=folder, wait=3, subSite=subSite)

    def getDescription(self, soup):
        descriptionElement1 = soup.select("div.sceneDesc")
        description = descriptionElement1[0].text
        description = description.replace("Video Description:", "")
        description = description.strip()

        return description

    def getCast(self, soup):
        cast = []
        actorElements = soup.select("a.pornstarName")
        for actor in actorElements:
                cast.append(actor.text)
        return cast

    def getCovers(self, soup):
        covers = []
        frontCoverElement = soup.select("#vjs_video_3_html5_api")
        coverUrl = frontCoverElement[0]['poster']
        covers.append({'url': "%s" % ( coverUrl),
                       'type': 'front'})
        return covers

    def updateProviderprefix(self, soup, subsite=None):
        self.providerPrefix = subsite

        self.providerPrefix = self.providerPrefix.title()
        self.providerPrefix = self.providerPrefix.replace("'", "")
        self.providerPrefix = self.providerPrefix.replace(",", "")
        self.providerPrefix = self.providerPrefix.replace(" ", "")

    def buildTitle(self, soup, cast):
        titleElement = soup.select("h3.title")
        title = titleElement[0].text
        if len(cast) > 0:
            return "[%s] %s: %s" % (self.providerPrefix, cast[0], title)
        else:
            return "[%s] %s" % (self.providerPrefix, title)
