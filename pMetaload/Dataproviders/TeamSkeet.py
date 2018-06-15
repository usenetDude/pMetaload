from bs4 import BeautifulSoup

from Dataproviders.Dataprovider import Dataprovider


class TeamSkeet(Dataprovider):

    baseurl = "http://www.teamskeet.com"
    newestUrl = "http://www.teamskeet.com/t1/updates/?site=ts#Newest_Updates"
    metadataurl = ""

    providerPrefix = 'TeamSkeet'

    containedsites = ["Innocenthigh", "Rubateen", "Teenpies", "Exxxxtrasmall", "Badmilfs", "Stepsiblings",
                      "Teencurves", "Therealworkout", "Teensloveanal", "Thisgirlsucks", "Teenyblack", "Shesnew",
                      "Dyked", "Gingerpatch", "Oyeloca", "Tittyattack", "Teensdoporn", "POVLife","Tittyattack", "Lusthd",
                      ""]

    def getName(self):
        return "TeamSkeet.com"


    def getNewestEntries(self):
        result, content = self.getUrl(self.newestUrl, selenium=True, wait=2)

        if result:
            soup = BeautifulSoup(content, 'html.parser')
            return self.parseNewestEntries(soup)

    def parseNewestEntries(self, soup):
        Entries = []
        newestScenePreviews = soup.select("li.white")
        for scene in newestScenePreviews:

            linkElement =scene.select("div.info > div > a")[0]

            caption = linkElement.text.strip()
            url = linkElement['href']

            subsiteElement = scene.select("div.info > div > p > a")[0]
            subsite = subsiteElement.text
            dateElement = scene.select("div.info > div > p > strong")[0]
            date = dateElement.text
            Entries.append({'title': caption.strip(),
                            'url':  url,
                            'rlsdate' : date,
                            'site' : subsite})
        self.Entries = Entries
        return Entries

    def getMetadata(self, url, folder=None, wait=0, subsite=None):
        super(TeamSkeet, self).getMetadata(url=url, folder=folder, wait=3, subSite=subsite)

    def getDescription(self, soup):
        descriptionElement1 = soup.select(" #story-and-tags > table > tbody > tr > td > div.gray")
        return descriptionElement1[0].text

    def getCast(self, soup):
        cast = []
        currentSceneInfo = soup.select(" #story-and-tags > table > tbody > tr > td > div > div h3")[0]
        actorElements = currentSceneInfo.findAll("a")
        for actor in actorElements:
            cast.append(actor.text)
        return cast

    def getCovers(self, soup):
        covers = []
        frontCoverElement = soup.select("#video")
        coverUrl = frontCoverElement[0]['poster']
        covers.append({'url': '%s' % coverUrl,
                       'type': 'front'})
        return covers

    def updateProviderprefix(self, soup, subsite=None):
        siteElement = soup.select("#story-and-tags > table > tbody > tr > td > div > div > div > a")

        self.providerPrefix = siteElement[0].text
        self.providerPrefix = self.providerPrefix.replace(".com", "")

    def buildTitle(self, soup, cast):
        self.updateProviderprefix(soup)
        titleElement = soup.select("title")[0]
        title = titleElement.text.split('|')[1].strip()

        if len(cast) > 0:
            return "[%s] %s: %s" % (self.providerPrefix, cast[0], title)
        else:
            return "[%s] %s" % (self.providerPrefix, title)