from bs4 import BeautifulSoup
from manhwaDownloader.core import output
from manhwaDownloader.core import asyncioDownloader
from manhwaDownloader.constants import CONSTANTS as CONST

import re
import asyncio
import cfscrape
import logging


class Client:
    """
    subclass of baseClient, specific to manytoons.com
    """

    def __init__(self, useTemplate, seriesName):
        self.seriesName = seriesName
        self.siteTemplateDict = CONST.SITETEMPLATEDICT[useTemplate]
        self.scraper = cfscrape.create_scraper()

    def gatherSiteInfo(self, soup):
        """
        gather information from given site chapterName, imgNum and imgLink
        :param soup: BeautifulSoup object
        :return: dict {chapterName: [(imgNum, imgUrl), ...)]}
        """
        imgInfoDict = dict()
        chapterTitle = soup.title.string

        # get image tags information from dictionary, to search for images links
        gatherImgTags = soup.find_all(self.siteTemplateDict['gatherImgTags'][0],
                                      self.siteTemplateDict['gatherImgTags'][1])

        # gather site links in a dictionary
        for tag in gatherImgTags:
            gatherRawLink = tag[self.siteTemplateDict['gatherRawLink']]
            cleanLink = gatherRawLink.strip()

            if not imgInfoDict:
                imgInfoDict.update({chapterTitle: [cleanLink]})
            else:
                imgInfoDict[chapterTitle].append(cleanLink)
        return imgInfoDict

    def getNext(self, soup):
        """
        get next chapter url
        :param soup: BeautifulSoup object
        :return: set
        """
        siteUrlList = set()
        imgTags = soup.find_all(self.siteTemplateDict['nextImgTags'][0],
                                self.siteTemplateDict['nextImgTags'][1])
        for tag in imgTags:
            rawLink = tag[self.siteTemplateDict['nextRawLink']]
            cleanLink = rawLink.strip()
            siteUrlList.add(cleanLink)
        return siteUrlList

    def run(self, url, numChapters=None):
        """
        recursive get wesite
        :param url: url link
        :return: None
        """

        print(f'Downloading: {url}...')
        response = self.scraper.get(url)
        if not response.status_code == 200 or numChapters is 0:
            return
        else:
            siteContent = response.content
            soup = BeautifulSoup(siteContent, 'html.parser')
            siteInfoDict = self.gatherSiteInfo(soup)

            # use asyncio to download images
            ad = asyncioDownloader.AsyncioDownloader(siteInfoDict)
            sites = asyncio.run(ad.createTasks())

            # get chapter name from dictionary and remove illegal character for path
            chapterName = [key for key in siteInfoDict.keys()]
            cleanChapterName = re.sub(CONST.REMOVEILLEGALCHARS, '', chapterName[0])

            # save image data
            imgNum = 1
            for imgData in sites:
                output.Output(self.seriesName).toFile(cleanChapterName, imgNum, imgData, saveToProjectFolder=False)
                imgNum += 1

            # get next url
            nextUrl = list(self.getNext(soup))
            chapterName
            self.run(nextUrl[0])
