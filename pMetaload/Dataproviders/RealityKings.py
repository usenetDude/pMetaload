from bs4 import BeautifulSoup

from Dataproviders.Dataprovider import Dataprovider


class RealityKings(Dataprovider):

    baseurl = "https://www.realitykings.com"
    newestUrl = "%s/tour/videos/" %(baseurl)
    metadataurl = ""

    providerPrefix = 'RealityKings'

    containedsites = ["Teenslovehugecocks", "Roundandbrown", "RKPrime", "Milfhunter", "Mikesapartment", "Bignaturals",
                      "Pure18", "Momslickteens", "Momsbangteens", "Streetblowjobs", "Sneakysex","Firsttimeauditions",
                      "8thstreetlatinas", "Steetblowjobs", "Eurosexparties", "Welivetogether", "Monstercurves" ]

    def getName(self):
        return "RealityKings.com"


    def getNewestEntries(self):
        result, content = self.getUrl(self.newestUrl)

        if result:
            soup = BeautifulSoup(content, 'html.parser')
            return self.parseNewestEntries(soup)

    def parseNewestEntries(self, soup):
        Entries = []
        newestScenePreviews = soup.select("article.card")
        for scene in newestScenePreviews:

            linkElement =scene.select("h2.card-info__title > a")[0]
            caption = linkElement.text
            url = linkElement['href']

            subsiteElement = scene.select("div.card-info__meta > a")[0]
            subsite = subsiteElement.text.strip()
            dateElement = scene.select("span.card-info__meta-date")
            date = dateElement[0].text
            Entries.append({'title': caption.strip(),
                            'url': "%s%s" % (self.baseurl, url),
                            'rlsdate' : date,
                            'site' : subsite})
        self.Entries = Entries
        return Entries

    def getDescription(self, soup):
        descriptionElement1 = soup.select("#trailer-desc-txt > p")
        return descriptionElement1[0].text

    def getCast(self, soup):
        cast = []
        actorElements = soup.select("#trailer-desc-txt > h2 > a")
        for actor in actorElements:
            cast.append(actor.text)
        return cast

    def getCovers(self, soup):
        covers = []
        frontCoverElement = soup.select("#video")
        coverUrl = frontCoverElement[0]['poster']
        covers.append({'url': coverUrl,
                       'type': 'front'})
        return covers

    def updateProviderprefix(self, soup, subsite=None):
        siteElement = soup.select("#trailer-desc-txt > h3 > a")

        self.providerPrefix = siteElement[0].text
        self.providerPrefix = self.providerPrefix.title()
        self.providerPrefix = self.providerPrefix.replace(" ", "")

    def buildTitle(self, soup, cast):
        self.updateProviderprefix(soup)
        titleElement = soup.select("h1.section_title")
        title = titleElement[0].text
        if len(cast) > 0:
            return "[%s] %s: %s" % (self.providerPrefix, cast[0], title)
        else:
            return "[%s] %s" % (self.providerPrefix, title)
