import scrapy
from scrapy import Selector, Request

from JdCrawler.items import JdcrawlerItem


class JdSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['search.jd.com']
    start_urls = ['http://search.jd.com/Search?keyword=射雕英雄传']
    searchword = "射雕英雄传"
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36"
    }

    def parse(self, response, **kwargs):
        selector = Selector(response)
        node_list = selector.xpath("//ul[@class='gl-warp clearfix']/li")
        for node in node_list:
            good = JdcrawlerItem()
            try:
                good['name'] = node.xpath("div/div[@class='p-name p-name-type-2']/a/em/text()").extract()[0]. \
                    replace("\n", "-").replace("\t", "-")
                good['title'] = node.xpath("div/div[@class='p-img']/a/@title").extract()[0]
                good['url'] = node.xpath("div/div[@class='p-img']/a/@href").extract()[0].replace("//", "")
                good['price'] = node.xpath("div/div[@class='p-price']/strong/i/text()").extract()[0]
                good['shop'] = node.xpath("div/div[@class='p-shop']//a/text()").extract()[0]

            except:
                print('解析异常...')
            good['searchword'] = JdSpider.searchword
            yield good

        for page in range(1, 11):
            url = JdSpider.start_urls[0] + "&page=" + str(1 + 2 * page)
            print(url)
            yield Request(url, callback=self.parse,
                          headers=self.headers,
                          # cookies=self.cookies,
                          # meta=self.meta
                          )
