import re
import asyncio
import time

from manhwaDownloader.clients import webtoonXYZClient as client
from manhwaDownloader.core import asyncioDownloader
from manhwaDownloader.core import output
from manhwaDownloader.core import imgToPDF

if __name__ == '__main__':
    startUrl = 'https://www.webtoon.xyz/read/worn-and-torn-newbie/chapter-0/'
    seriesName = 'worn-and-torn-newbie'
    startClient = client.Client(siteUrl=startUrl)

    start = time.time()
    siteList = list(startClient.gatherUrls())

    for site in siteList[:1]:
        print(site)
        siteClient = client.Client(siteUrl=site)
        siteInfoDict = siteClient.gatherSiteInfo()

        ad = asyncioDownloader.AsyncioDownloader(siteInfoDict)
        sites = asyncio.run(ad.createTasks())
        chapterName = [key for key in siteInfoDict.keys()]
        cleanChapterName = re.sub('[^\w\-_\. ]', '', chapterName[0])

        imgNum = 1
        for imgData in sites:
            output.Output(seriesName).toFile(cleanChapterName, imgNum, imgData, saveToProjectFolder=False)
            imgNum += 1

    # Convert image to PDF
    converter = imgToPDF.ImgToPDF(seriesName)
    converter.run(removeStrFromName='- WEBTOON XYZ', deleteFolders=False)

    end = time.time()
    print((end - start) / 60)
