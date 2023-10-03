import scrapy
from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = "pep"
    allowed_domains = ["peps.python.org"]
    start_urls = ["https://peps.python.org/"]

    def parse(self, response):
        table = response.css("section#numerical-index")
        tbody = table.css("tbody")
        for row in tbody.css("tr"):
            href = row.css("a").attrib["href"]
            pep_link = response.urljoin(href) + "/"
            yield response.follow(pep_link, callback=self.parse_pep)

    def parse_pep(self, response):
        section = response.css("section#pep-content")
        name = section.css("h1::text").get()
        number = int(name.split(" ")[1])
        status = section.css('dt:contains("Status") + dd abbr::text').get()
        data = {"number": number, "name": name, "status": status}
        yield PepParseItem(data)
