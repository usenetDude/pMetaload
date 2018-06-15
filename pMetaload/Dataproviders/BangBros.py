from bs4 import BeautifulSoup

from Dataproviders.Dataprovider import Dataprovider


class BangBros(Dataprovider):

    baseurl = "https://bangbros.com"
    newestUrl = "%s/videos/" %(baseurl)
    metadataurl = ""

    providerPrefix = 'BangBros'

    containedsites = ["Bangbus", "Monstersofcock", "Assparade", "Bigmouthfuls", "Bigtitsroundasses", "Tugjobs",
                      "Bigtitcreampie", "Milflessons", "Milfsoup", "Brownbunnies", "Facialfest", "Blowjobfridays",
                      "Magicalfeet", "Ballhoneys", "Mranal", "Backroomfacials", "Pawg", "Fuckteamfive", "Bangbros18",
                      "Pornstarspa", "Partyof3", "Latinarampage", "Backroommilf", "Canhescore", "Colombiafuckfest",
                      "Bangpov", "Newbieblack", "Gloryholeloads", "Bangcasting", "Blowjobninjas", "Publicbang",
                      "Streetranger", "Chongas", "Mydirtymaid", "Stepmomvideos", "Mrcameltoe", "Powermunch", "Boobsquad",
                      "Dorminvasion", "Dirtyworldtour", "livingwithanna", "Mylifeinbrazil", "Workinglatinas", "MomisHorny",
                      "Casting", "Bangbrosangels", "Pennyshow", "Bangtryouts", "Sluttywhitegirls", "Avaspice"]
    def getName(self):
        return "Bangbros.com"


    def getNewestEntries(self):
        result, content = self.getUrl(self.newestUrl)

        if result:
            soup = BeautifulSoup(content, 'html.parser')
            return self.parseNewestEntries(soup)

    def parseNewestEntries(self, soup):
        Entries = []
        newestScenePreviews = soup.select("div.echThumb")
        for scene in newestScenePreviews:

            linkElement =scene.select("a.thmb_lnk")[0]
            caption = linkElement['title']
            url = linkElement['href']

            subsiteElement = scene.select("span.thmb_mr_1 > a.thmb_mr_lnk > span.faTxt")[0]
            subsite = subsiteElement.text.strip()
            dateElement = scene.select("span.thmb_mr_2 > span.faTxt")
            date = dateElement[0].text
            Entries.append({'title': caption.strip(),
                            'url': "%s%s" % (self.baseurl, url),
                            'rlsdate' : date,
                            'site' : subsite})
        self.Entries = Entries
        return Entries

    def getDescription(self, soup):
        descriptionElement1 = soup.select("div.vdoDesc")
        return descriptionElement1[0].text.strip()

    def getCast(self, soup):
        cast = []
        actorElements = soup.select("div.vdoCast a")
        for actor in actorElements:
            if actor['href'].startswith('/model'):
                cast.append(actor.text)
        return cast

    def getCovers(self, soup):
        covers = []
        frontCoverElement = soup.select("#player-overlay-image")
        coverUrl = frontCoverElement[0]['src']
        covers.append({'url': "https:%s" % ( coverUrl),
                       'type': 'front'})
        return covers

    def updateProviderprefix(self, soup, subsite=None):
        siteElement = soup.select("div.vdoCast > a")

        self.providerPrefix = siteElement[0].text
        self.providerPrefix = self.providerPrefix.title()
        self.providerPrefix = self.providerPrefix.replace("'", "")
        self.providerPrefix = self.providerPrefix.replace(",", "")
        self.providerPrefix = self.providerPrefix.replace(" ", "")

    def buildTitle(self, soup, cast):
        self.updateProviderprefix(soup)
        titleElement = soup.select("div.ps-vdoHdd > h1")
        title = titleElement[0].text
        if len(cast) > 0:
            return "[%s] %s: %s" % (self.providerPrefix, cast[0], title)
        else:
            return "[%s] %s" % (self.providerPrefix, title)
