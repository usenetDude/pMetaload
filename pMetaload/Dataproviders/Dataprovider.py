import time
from abc import ABC, abstractmethod
import pathlib
import requests
from bs4 import BeautifulSoup
from flask import current_app
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class Dataprovider(ABC):
    providerPrefix = ''

    Entries = []

    @abstractmethod
    def getName(self):
        pass

    @abstractmethod
    def getNewestEntries(self):
        pass

    @abstractmethod
    def getDescription(self, soup):
        pass

    @abstractmethod
    def getCast(self, soup):
        pass

    @abstractmethod
    def getCovers(self, soup):
        pass

    @abstractmethod
    def updateProviderprefix(self, soup, subSite=None):
        pass

    @abstractmethod
    def buildTitle(self, soup, cast):
        pass

    def getMetadata(self, url, folder=None, wait=0, subSite=None):
        if wait > 0:
            result, content = self.getUrl(url, selenium=True, wait=wait)
        else:
            result, content = self.getUrl(url, selenium=False, wait=wait)
        if result:
            soup = BeautifulSoup(content, 'html.parser')

            description = self.getDescription(soup)
            if description is not None:
                self.saveTextfile(description, "description", folder=folder)

            ##Cast
            cast = self.getCast(soup)
            self.saveCast(cast, folder=folder)

            ##Covers
            covers = self.getCovers(soup)
            for cover in covers:
                self.downloadCover(cover['url'], cover['type'], folder=folder)

            ##ProviderPrefix
            ##We build a new Prefix per Scene as this has multiple Sites
            self.updateProviderprefix(soup, subSite)

            ##Title
            title = self.buildTitle(soup, cast)
            self.saveTextfile(title, "title", folder=folder)

    def getUrl(self, url, selenium=False, wait=0):
        if selenium:
            driver = webdriver.Remote(command_executor=current_app.config['SELENIUMURL'],
                                      desired_capabilities=DesiredCapabilities.CHROME)
            driver.get(url)
            time.sleep(wait)
            html = driver.page_source
            driver.quit()
            return True, html
        else:
            r = requests.get(url)

            if r.status_code == 200:
               return True, r.text
            else:
                return False, r.status_code

    def downloadCover(self, url, type, folder=None):
        response = requests.get(url)
        if response.status_code == 200:
            if folder is not None:
                path = pathlib.Path(folder) / pathlib.Path("%s.jpg" %(type))
                with open("%s" % str(path.absolute()), 'wb') as f:
                    f.write(response.content)
            else:
                with open("%s.jpg" % type, 'wb') as f:
                    f.write(response.content)

    def saveTextfile(self, text, file, folder=None):
        if folder is not None:
            path = pathlib.Path(folder) / pathlib.Path("%s.txt" % (file))
            with open("%s" % str(path.absolute()), "w") as f:
                f.write(text)
        else:
            with open("%s.txt" % file, "w") as f:
                f.write(text)

    def saveCast(self, cast, folder=None):
        self.saveTextfile(", ".join(cast), "cast", folder)
