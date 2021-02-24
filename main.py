import time

from manhwaDownloader.clients import client as client
from manhwaDownloader.core import imgToPDF

if __name__ == '__main__':
    start = time.time()
    startUrl = 'https://www.tappytoon.com/en/chapters/751940412?'
    seriesName = 'beauty-beast'

    myClient = client.Client(useTemplate='webtoonXYZ', seriesName=seriesName)
    myClient.run(url=startUrl, numChapters=1)

    # Convert image to PDF
    converter = imgToPDF.ImgToPDF(seriesName)
    converter.run(removeStrFromName='', deleteFolders=False)

    end = time.time()
    print((end - start) / 60)
