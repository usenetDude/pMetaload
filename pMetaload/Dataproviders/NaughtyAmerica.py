from bs4 import BeautifulSoup

from Dataproviders.Dataprovider import Dataprovider


class NaughtyAmerica(Dataprovider):

    baseurl = "https://www.naughtyamerica.com"
    newestUrl = "https://tour.naughtyamerica.com/new-porn-videos"
    metadataurl = ""

    providerPrefix = 'NaughtyAmerica'

    containedsites = ["NaughtyAmerica", "Myfriendshotmom", "Assmasterpiece", "Ihaveawife", "Mywifeisapornstar",
                      "Naughtybookworms", "Mygirlfriendsbustyfriend", "Mysistershotfriend", "Myfriendshotgirl",
                      "Neighboraffair","Mydaughtershotfriend", "Dirtywivesclub", "Naughtyoffice", "Diaryofananny",
                      "Seducedbyacougar"]

    def getName(self):
        return "NaughtyAmerica.com"


    def getNewestEntries(self):
        result, content = self.getUrl(self.newestUrl)

        if result:
            soup = BeautifulSoup(content, 'html.parser')
            return self.parseNewestEntries(soup)

    def parseNewestEntries(self, soup):
        Entries = []
        newestScenePreviews = soup.select("div.grid-item-large")
        for scene in newestScenePreviews:

            linkElement =scene.select("a.model-name")[0]

            caption = linkElement.text.rsplit('in', 1)[0].strip()
            url = linkElement['href']

            subsite = linkElement.text.split('in')[-1].strip()
            dateElement = scene.select("p.entry-date")
            date = dateElement[0].text
            Entries.append({'title': caption.strip(),
                            'url':  url,
                            'rlsdate' : date,
                            'site' : subsite})
        self.Entries = Entries
        return Entries

    def getDescription(self, soup):
        descriptionElement1 = soup.select("p.synopsis_txt")
        return descriptionElement1[0].text

    def getCast(self, soup):
        cast = []
        currentSceneInfo = soup.select("#scene-info > p.scenepage")[0]
        actorElements = currentSceneInfo.findAll("a")
        for actor in actorElements:
            cast.append(actor.text)
        return cast

    def getCovers(self, soup):
        covers = []
        frontCoverElement = soup.select("#trailer_card")
        coverUrl = frontCoverElement[0]['src']
        covers.append({'url': 'https:%s' % coverUrl,
                       'type': 'front'})
        return covers

    def updateProviderprefix(self, soup, subsite=None):
        siteElement = soup.select("#photo-set > #synopsis > p > a")

        self.providerPrefix = siteElement[0].text
        self.providerPrefix = self.providerPrefix.replace("'s", "s")
        self.providerPrefix = self.providerPrefix.title()
        self.providerPrefix = self.providerPrefix.replace(" ", "")
        self.providerPrefix = self.providerPrefix.replace("'", "")

    def buildTitle(self, soup, cast):
        self.updateProviderprefix(soup)
        titleElement = soup.find("div", attrs={"itemprop": "name"})
        title = titleElement.text.replace("\n", "").replace("  ","").strip().replace("&", " & ")
        return "[%s] %s" % (self.providerPrefix, title)
