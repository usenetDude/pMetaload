from bs4 import BeautifulSoup

from Dataproviders.Dataprovider import Dataprovider


class Kinkyfamily(Dataprovider):

    baseurl = "http://kinkyfamily.com"
    newestUrl = "%s" % baseurl

    providerPrefix = "KinkyFamily"

    containedsites = ['Kinkyfamily']

    def getName(self):
        return "KinkyFamily.com"

    def getNewestEntries(self):
        result, content = self.getUrl(self.newestUrl)

        if result:
            soup = BeautifulSoup(content, 'html.parser')
            return self.parseNewestEntries(soup)

    def parseNewestEntries(self, soup):
        Entries = []
        newestScenePreviews = soup.select(".holder > div.th")
        for scene in newestScenePreviews:
            caption = scene.find("span", {"class": "caption"})

            #from html-source: window.location.href = "/index.php/main/view_movie/"+tmp_id+"/"+tmp_title;
            link = scene.find("a", {"class": "thumb_wrap"})

            clickCode = link['onclick'] #looks like re_add_click('11', 'this-is-caption');
            splittedCode = clickCode.split("'")
            tmp_id = splittedCode[1]
            tmp_title = splittedCode[len(splittedCode)-2]

            Entries.append({ 'title': caption.text,
                             'url': "%s/index.php/main/view_movie/%s/%s"%(self.baseurl, tmp_id,tmp_title),
                             'rlsdate': "",
                             'site': self.getName()})
        self.Entries = Entries
        return Entries

    def getDescription(self, soup):
        descriptionElement = soup.select(".description")
        description = descriptionElement[0].text
        return description.replace("Description:", "").strip()

    def getCast(self, soup):
        return []

    def getCovers(self, soup):
        covers = []
        for line in soup.get_text().split("\n"):
            if '/content/thumbs/' in line:
                splittedLine = line.split("'")
                imageLink = splittedLine[len(splittedLine) - 2]
                break
        coverUrl = "%s%s" % (self.baseurl, imageLink)
        covers.append({'url': coverUrl,
                       'type': 'front'})
        return covers

    def updateProviderprefix(self, soup, subsite=None):
        pass

    def buildTitle(self, soup, cast):
        titleElement = soup.select("h2.title_heading")
        title = titleElement[0].text
        if len(cast) > 0:
            return "[%s] %s: %s" % (self.providerPrefix, cast[0], title)
        else:
            return "[%s] %s" % (self.providerPrefix, title)
