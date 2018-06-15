from bs4 import BeautifulSoup

from Dataproviders.Dataprovider import Dataprovider


class Teenfidelity(Dataprovider):

    baseurl = "https://www.teenfidelity.com"
    newestUrl = "%s" %(baseurl)
    metadataurl = ""

    providerPrefix = 'Teenfidelity'

    containedsites = ["Teenfidelity"]
    def getName(self):
        return "Teenfidelity.com"


    def getNewestEntries(self):
        result, content = self.getUrl(self.newestUrl)

        if result:
            soup = BeautifulSoup(content, 'html.parser')
            return self.parseNewestEntries(soup)

    def parseNewestEntries(self, soup):
        Entries = []
        newestScenePreviews = soup.select("#video-updates-videos > li.top-level")
        for scene in newestScenePreviews:

            linkElement =scene.select("h5")[0]
            caption = linkElement.text.rsplit('#', 1)[0]
            urlElement = scene.select("div.inner-level > a.trigger")
            url = urlElement[0]['href']

            dateElement = scene.select("div.video-data > p.video-update-row3")
            date = dateElement[0].text.split("\nEpisode")[0].strip().replace("Date: ", "")
            Entries.append({'title': caption,
                            'url': "%s%s" %(self.baseurl, url),
                            'rlsdate' : date,
                            'site': self.getName()})
        self.Entries = Entries
        return Entries

    def getDescription(self, soup):
        descriptionElement1 = soup.select("p.trailer-excerpt")
        description =descriptionElement1[0].text.strip()
        description = description.replace("Description: ", "")
        return description

    def getCast(self, soup):
        cast = []
        actorElements = soup.select("#inner-block > p > a")
        for actor in actorElements:
            cast.append(actor.text)
        return cast

    def getCovers(self, soup):
        covers = []
        frontCoverElement = soup.select("#video_content > video")
        coverUrl = frontCoverElement[0]['poster']
        covers.append({'url': 'https:%s' % coverUrl,
                       'type': 'front'})
        return covers

    def updateProviderprefix(self, soup, subsite=None):
        pass

    def buildTitle(self, soup, cast):
        titleElement = soup.select("div.trailer-header > h1.lt")
        title = titleElement[0].text
        episodeElement = soup.select("div.trailer-header > div.rt")
        episode = episodeElement[0].text.split(' ')[0].replace('#', '')
        if len(cast) > 0:
            return "[%s] Episode %s: %s" % (self.providerPrefix, episode, title)
        else:
            return "[%s] %s" % (self.providerPrefix, title)
