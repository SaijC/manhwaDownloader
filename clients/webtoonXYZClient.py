from bs4 import BeautifulSoup
from manhwaDownloader.clients import baseClient


class Client(baseClient.Client):
    """
    subclass of baseClient, specific to manytoons.com
    """

    def __init__(self, siteUrl):
        super().__init__(siteUrl=siteUrl)
        self.site = self.getSite()

    def gatherUrls(self):
        """
        gathers urls from given startUrl and n number of chapter to get
        :param endChapter: int
        :return: list of tupels
        """
        siteUrlList = set()
        if self.site.status_code == 200:
            siteContent = self.site.content
            soup = BeautifulSoup(siteContent, 'html.parser')
            imgTags = soup.find_all('option', {'class': 'short'})
            for tag in imgTags:
                rawLink = tag['data-redirect']
                cleanLink = rawLink.strip()
                siteUrlList.add(cleanLink)
        return siteUrlList

    def gatherSiteInfo(self):
        """
        gather information from given site chapterName, imgNum and imgLink
        :return: dict {chapterName: [(imgNum, imgUrl), ...)]}
        """
        imgInfoDict = dict()
        if self.site.status_code == 200:
            siteContent = self.site.content
            soup = BeautifulSoup(siteContent, 'html.parser')
            chapterTitle = soup.title.string
            imgTags = soup.find_all('img', {'class': 'wp-manga-chapter-img'})
            for tag in imgTags:
                rawLink = tag['data-src']
                cleanLink = rawLink.strip()

                if not imgInfoDict:
                    imgInfoDict.update({chapterTitle: [cleanLink]})
                else:
                    imgInfoDict[chapterTitle].append(cleanLink)
            return imgInfoDict
