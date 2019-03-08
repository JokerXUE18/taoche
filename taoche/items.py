# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TaocheItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    table = "taoche"  # 数据库表名 可有可无
    title = scrapy.Field()  # 标题
    resistered_date = scrapy.Field()  # 上牌时间
    mileage = scrapy.Field()  # 车程
    city = scrapy.Field()  # 销售城市
    price = scrapy.Field()  # 原价
    new_price = scrapy.Field()  # 出售价
    tax = scrapy.Field()  # 含税
    refer_price = scrapy.Field()  # 参考价
    displacement = scrapy.Field()  # 排量
    transmission = scrapy.Field()  # 变速箱
    brand_type = scrapy.Field()  # 品牌型号
    loc_of_lic = scrapy.Field()  # 牌照所在地
    oil_wear = scrapy.Field()  # 油耗
    engine = scrapy.Field()  # 发动机
    three_high = scrapy.Field()  # 长宽高
    drive_way = scrapy.Field()  # 驱动方式
    body_type = scrapy.Field()  # 车身类型
    che_level = scrapy.Field()  # 车辆级别
    trunk_cap = scrapy.Field()  # 后备箱容量
    detail_url = scrapy.Field()
