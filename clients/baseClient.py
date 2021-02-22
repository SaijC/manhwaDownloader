import cfscrape


class Client:
    """
    base client to request and return site content
    """

    def __init__(self, siteUrl):
        self.siteUrl = siteUrl
        self.scraper = cfscrape.create_scraper()

    def getSite(self):
        """
        get site status
        :return: status code
        """
        return self.scraper.get(self.siteUrl)

    def getSiteContent(self):
        """
        get site content
        :return: site Content
        """
        return self.scraper.get(self.siteUrl).content

    def getSiteText(self):
        """
        get site as text
        :return: str
        """
        return self.scraper.get(self.siteUrl).text
