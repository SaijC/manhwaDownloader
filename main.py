import re
import logging
import asyncio
import time

from manhwaDownloader.clients import manytoonClient
from manhwaDownloader.core import asyncioDownloader
from manhwaDownloader.core import output
from manhwaDownloader.core import imgToPDF

logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    seriesName = ''
    startUrl = ''
    startChapter = 1
    endChapter = 2

    start = time.time()

    # Gather all site urls
    siteList = manytoonClient.GatherUrls().gatherUrls(siteUrl=startUrl,
                                                      startChapter=startChapter,
                                                      endChapter=endChapter)

    for site in siteList:
        logging.info(site)
        client = manytoonClient.Client(siteUrl=site)
        siteInfoDict = client.gatherSiteInfo()

        ad = asyncioDownloader.AsyncioDownloader(siteInfoDict)
        sites = asyncio.run(ad.createTasks())
        chapterName = [key for key in siteInfoDict.keys()]
        cleanChapterName = re.sub('[^\w\-_\. ]', '', chapterName[0])

        imgNum = 1
        for imgData in sites:
            output.Output(seriesName).toFile(cleanChapterName, imgNum, imgData, saveToProjectFolder=False)
            imgNum += imgNum


    # # Convert image to PDF
    converter = imgToPDF.ImgToPDF(seriesName)
    converter.run(removeStrFromName='', deleteFolders=True)

    end = time.time()
    logging.info((end - start)/60)
