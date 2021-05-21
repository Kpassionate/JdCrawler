# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JdItem(scrapy.Item):
    id = scrapy.Field()  # 商品id
    name = scrapy.Field()  # 商品名称
    price = scrapy.Field()  # 商品价格
    shop = scrapy.Field()  # 店铺名称
    img = scrapy.Field()  # 图片url
    url = scrapy.Field()  # 商品详情页链接
    info = scrapy.Field()  # 详细信息
