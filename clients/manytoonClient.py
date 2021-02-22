import re
from bs4 import BeautifulSoup
from manhwaDownloader.clients import baseClient

import logging
logging.basicConfig(level=logging.DEBUG)

class GatherUrls:
    @staticmethod
    def gatherUrls(siteUrl, startChapter, endChapter):
        """
        gathers urls from given startUrl and n number of chapter to get
        :param endChapter: int
        :return: list of tupels
        """
        siteUrlList = list()
        for chapterNum in range(startChapter, endChapter + 1):
            urlSplit = siteUrl.split('/')
            oldChapterName = urlSplit[-2]
            newChapterName = re.sub('\d+', str(chapterNum), oldChapterName)
            url = siteUrl.replace(oldChapterName, newChapterName)
            siteUrlList.append(url)
        return siteUrlList


class Client(baseClient.Client):
    """
    subclass of baseClient, specific to manytoons.com
    """

    def __init__(self, siteUrl):
        super().__init__(siteUrl=siteUrl)

    def gatherSiteInfo(self):
        """
        gather information from given site chapterName, imgNum and imgLink
        :return: dict {chapterName: [(imgNum, imgUrl), ...)]}
        """
        imgInfoDict = dict()
        site = self.getSite()
        if site.status_code == 200:
            siteContent = site.content
            soup = BeautifulSoup(siteContent, 'html.parser')
            chapterTitle = soup.title.string

            imgTags = soup.find_all("img", {"class": "wp-manga-chapter-img"})
            for tag in imgTags:
                rawLink = tag['src']
                cleanLink = rawLink.strip()

                if not imgInfoDict:
                    imgInfoDict.update({chapterTitle: [cleanLink]})
                else:
                    imgInfoDict[chapterTitle].append(cleanLink)
            return imgInfoDict
