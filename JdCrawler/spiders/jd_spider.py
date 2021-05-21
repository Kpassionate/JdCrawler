# -*- coding: utf-8 -*-

import scrapy
from JdCrawler.items import JdItem


class JdSpider(scrapy.Spider):
    name = 'jd'
    # 允许的域名
    allowed_domains = ['jd.com']  # 有的时候写个www.jd.com会导致search.jd.com无法爬取
    keyword = "射雕英雄传"
    page = 1
    # 解析jd搜索url，除了keyword和page都是干扰项，故只需拼接keyword和page即可
    url = 'https://search.jd.com/Search?keyword=%s&page=%d'

    def start_requests(self):
        yield scrapy.Request(self.url % (self.keyword, self.page), callback=self.parse, meta={'middleware': 'Selenium'})

    def parse(self, response, **kwargs):
        """
        分析
        jd的page是1、3、5...基数型，首次打开时展示第一页数据，下滑展示第二页数据，即每页展示N（基数）和N+1两页的总数据
        为获得完整数据，使用selenium模拟下滑操作，获取完整数据
        """

        for li in response.xpath('//li[@class="gl-item"]'):
            item = JdItem()
            # 京东商品ID
            _id = li.xpath('@data-sku').extract_first()
            # 商品图片
            _img = li.xpath('div/div[@class="p-img"]//img/@data-lazy-img').extract_first()
            # 商品名称
            _name = li.xpath('div//font[@class="skcolor_ljg"]/text()').extract_first()
            # 价格
            _price = li.xpath('div/div[@class="p-price"]//i/text()').extract_first()
            # 店铺名称
            _shop = li.xpath('div//a[@class="curr-shop hd-shopname"]/text()').extract_first()
            # 商品详情页url
            _url = li.xpath('div/div[@class="p-img"]/a/@href').extract_first()

            item['id'] = _id
            item['img'] = 'https:' + _img
            item['name'] = _name
            item['price'] = _price
            item['shop'] = _shop

            if _url.startswith('//'):
                item['url'] = 'https:' + _url

            elif not item['url'].startswith('https:'):
                item['info'] = None
                yield item
                continue
            # 获取详情页信息（详情页数据不需要使用selenium,那丫的太慢了）
            yield scrapy.Request(item['url'], callback=self.info_parse, meta={"item": item})

        if self.page < 20:
            self.page += 2
            yield scrapy.Request(self.url % (self.keyword, self.page), callback=self.parse,
                                 meta={'middleware': 'Selenium'})

    @staticmethod
    def info_parse(response):
        """
        获取详情页信息
        """
        item = response.meta['item']
        item['info'] = {}
        # 累计评价
        _comment_num = response.xpath('//div[@id="comment-count"]/a/text()').extract_first()
        # 书籍信息
        book = response.xpath('//div[@class="p-parameter"]//text()').extract()
        book_info = []
        # 去掉空格和换行符\n
        for i in book:
            i.replace('\n', '')
            b = i.strip()
            if len(b):
                book_info.append(b)
        item['info']['book_info'] = '·'.join(book_info)
        item['info']['comment_num'] = _comment_num

        yield item
