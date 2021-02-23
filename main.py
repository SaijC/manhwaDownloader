import time

from manhwaDownloader.clients import client as client
from manhwaDownloader.core import imgToPDF

if __name__ == '__main__':
    start = time.time()
    startUrl = 'https://manytoon.com/comic/tales-of-demons-and-gods/chapter-2-viewing-the-sky-from-the-bottom-of-the-well/'
    seriesName = 'tales-of-demons-and-gods'

    myClient = client.Client(useTemplate='manytoon', seriesName=seriesName)
    myClient.run(url=startUrl)

    # Convert image to PDF
    converter = imgToPDF.ImgToPDF(seriesName)
    converter.run(removeStrFromName='', deleteFolders=False)

    end = time.time()
    print((end - start) / 60)
