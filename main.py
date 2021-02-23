import re
import asyncio
import time

from manhwaDownloader.clients import manytoonClient as client
from manhwaDownloader.core import asyncioDownloader
from manhwaDownloader.core import output
from manhwaDownloader.core import imgToPDF

if __name__ == '__main__':
    startUrl = 'https://manytoon.com/comic/tales-of-demons-and-gods/chapter-2-viewing-the-sky-from-the-bottom-of-the-well/'
    seriesName = 'worn-and-torn-newbie'
    startClient = client.Client(siteUrl=startUrl)

    start = time.time()


    # Convert image to PDF
    # converter = imgToPDF.ImgToPDF(seriesName)
    # converter.run(removeStrFromName='', deleteFolders=False)

    end = time.time()
    print((end - start) / 60)
