from bs4 import BeautifulSoup
from manhwaDownloader.core import output
from manhwaDownloader.core import asyncioDownloader
from manhwaDownloader.constants import CONSTANTS as CONST

import re
import asyncio
import cfscrape


class Client:
    """
    subclass of baseClient, specific to manytoons.com
    """

    def __init__(self, useTemplate, seriesName):
        self.seriesName = seriesName
        self.siteTemplateDict = CONST.SITETEMPLATEDICT[useTemplate]
        self.scraper = cfscrape.create_scraper()

    def gatherSiteInfo(self, response):
        """
        gather information from given site chapterName, imgNum and imgLink
        :return: dict {chapterName: [(imgNum, imgUrl), ...)]}
        """
        imgInfoDict = dict()
        siteContent = response.content
        soup = BeautifulSoup(siteContent, 'html.parser')
        chapterTitle = soup.title.string
        gatherImgTags = soup.find_all(self.siteTemplateDict['gatherImgTags'][0],
                                      self.siteTemplateDict['gatherImgTags'][1])
        for tag in gatherImgTags:
            gatherRawLink = tag[self.siteTemplateDict['gatherRawLink']]
            cleanLink = gatherRawLink.strip()

            if not imgInfoDict:
                imgInfoDict.update({chapterTitle: [cleanLink]})
            else:
                imgInfoDict[chapterTitle].append(cleanLink)
        return imgInfoDict

    def getNext(self, response):
        """
        get next chapter url
        :return: set
        """
        siteUrlList = set()
        siteContent = response.content
        soup = BeautifulSoup(siteContent, 'html.parser')
        imgTags = soup.find_all(self.siteTemplateDict['nextImgTags'][0],
                                self.siteTemplateDict['nextImgTags'][1])
        for tag in imgTags:
            rawLink = tag[self.siteTemplateDict['nextRawLink']]
            cleanLink = rawLink.strip()
            siteUrlList.add(cleanLink)
        return siteUrlList

    def run(self, url):
        """
        recursive get wesite
        :param url: url link
        :return: None
        """
        print(f'Downloading: {url}...')
        response = self.scraper.get(url)
        if not response.status_code == 200:
            return
        else:
            siteInfoDict = self.gatherSiteInfo(response)

            ad = asyncioDownloader.AsyncioDownloader(siteInfoDict)
            sites = asyncio.run(ad.createTasks())

            chapterName = [key for key in siteInfoDict.keys()]
            cleanChapterName = re.sub(CONST.REMOVEILLEGALCHARS, '', chapterName[0])

            imgNum = 1
            for imgData in sites:
                output.Output(self.seriesName).toFile(cleanChapterName, imgNum, imgData, saveToProjectFolder=False)
                imgNum += 1
            nextUrl = list(self.getNext(response))
            self.run(nextUrl[0])