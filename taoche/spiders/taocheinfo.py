# -*- coding: utf-8 -*-
import scrapy
from taoche.items import TaocheItem
from taoche.spiders.city import CITY_CODE, CAR_CODE_LIST
import re


class TaocheinfoSpider(scrapy.Spider):
    name = 'taocheinfo'
    allowed_domains = ['taoche.com']
    start_urls = ['https://quanguo.taoche.com/audi/']
    for city in CITY_CODE:
        for car in CAR_CODE_LIST:
            # https://beijing.taoche.com/bmw/
            # beijing就是地区 bmw就是车辆品牌
            url = f"https://{city}.taoche.com/{car}/"
            start_urls.append(url)

    def parse(self, response):
        # [last()-1] 倒数第二项
        max_page = response.xpath("//div[@class='paging-box the-pages']/div/a[last()-1]/text()").extract()
        max_page = self.get_value(max_page)  # 数据为空的处理方式
        for page in range(int(max_page)):
            url = response.url + f'?page={page + 1}#pagetag'
            yield scrapy.Request(url=url, callback=self.parse_1)

    def parse_1(self, response):
        car_info_list = response.xpath("//div[@id='container_base']//ul/li")
        for car_info in car_info_list:
            title = car_info.xpath(".//div[@class='gongge_main']/a/span/text()").extract()[0]

            mileage = car_info.xpath(".//p/i[2]/text()").extract()[0]

            city = car_info.xpath(".//i[@class='city_i']/a/text()").extract()[0]

            price = car_info.xpath(".//i[@class='original']/text()").extract()
            price = price[0] if price else ''  # 有些没有原价 则输入一个空

            new_price = car_info.xpath(".//i[@class='Total brand_col']/text()").extract()[0]

            # 详情页url
            detail_url = car_info.xpath(".//div[@class='gongge_main']/a/@href").extract()[0]
            detail_url = "https:" + detail_url

            item = TaocheItem()

            item["title"] = title
            item["mileage"] = mileage
            item["city"] = city
            item["price"] = price
            item["new_price"] = new_price
            item["detail_url"] = detail_url

            # 将detail_url以参数形式传入到parse_detail 传入参数是meta={'data': item}
            yield scrapy.Request(url=detail_url, callback=self.parse_detail, meta={'data': item}, encoding='utf-8',
                                 dont_filter=True)

    # 进入详情页
    def parse_detail(self, response):

        tax = response.xpath("//div[@class='price-ratio clearfix']/span/text()").extract()[0]
        if '含税' in tax:
            tax = re.findall("(\d+.\d+)", tax)[1]
        else:
            tax = ''

        # 详情页数据

        # 参考价
        refer_price = response.xpath("//div[@class='price-ratio clearfix']/text()[2]").extract()[0]
        if '不详' in refer_price:
            refer_price = ""
        else:
            # strip()输出时 不会输出空格
            refer_price = re.findall(r"参考价:(.*)", refer_price)[0].strip()

        # 排量/变速箱
        info = response.xpath("//div[@class='summary-attrs']/dl[3]/dd/text()").extract()[0]
        info = re.findall(r"(.*?)/(.*)", info)[0]
        displacement = info[0]
        transmission = info[1]
        if "-" in displacement:
            displacement = ''
        if "-" in transmission:
            transmission = ''

            # 品牌型号
        brand_type = response.xpath("//div[@class='hide-box']/div[2]/div[1]/ul/li[1]/span//text()").extract()
        brand_type = "".join(brand_type)
        # print(brand_type)
        # 牌照所在地
        loc_of_lic = response.xpath("//div[@class='hide-box']/div[2]/div[1]/ul/li[2]/span/a/text()").extract()[0]

        loc_of_lic = loc_of_lic.strip()
        # print(loc_of_lic)
        # 油耗
        oil_wear = response.xpath("//div[@class='hide-box']/div[2]/div[2]/ul/li[2]/span/text()").extract()[0]
        # print(oil_wear)
        # 发动机
        engine = response.xpath("//div[@class='hide-box']/div[2]/div[1]/ul/li[3]/span/text()").extract()[0]
        # print(engine)
        if "-" in engine:
            engine = ""
        # 长宽高
        three_high = response.xpath("//div[@class='hide-box']/div[2]/div[2]/ul/li[3]/span/text()").extract()[0]
        if "-" in three_high:
            three_high = ''
        # print(three_high)
        # 驱动方式
        drive_way = response.xpath("//div[@class='hide-box']/div[2]/div[1]/ul/li[4]/span/text()").extract()[0]
        # print(drive_way)
        # 车身类型
        body_type = response.xpath("//div[@class='hide-box']/div[2]/div[2]/ul/li[4]/span/text()").extract()[0]
        if "-" in body_type:
            body_type = ""
        # print(body_type)
        # 车辆级别
        che_level = response.xpath("//div[@class='hide-box']/div[2]/div[1]/ul/li[5]/span/a/text()").extract()[0]
        che_level = che_level.strip()
        # print(che_level)
        # 后备箱容量
        trunk_cip = response.xpath("//div[@class='col-xs-6 parameter-configure-list']/ul/li[5]/span/text()").extract()[0]
        if "-" in trunk_cip:
            trunk_cip = ''

        item = response.meta['data']
        item["tax"] = tax
        item["refer_price"] = refer_price
        item["displacement"] = displacement
        item["transmission"] = transmission
        item["brand_type"] = brand_type
        item["loc_of_lic"] = loc_of_lic
        item["oil_wear"] = oil_wear
        item["engine"] = engine
        item["three_high"] = three_high
        item["drive_way"] = drive_way
        item["body_type"] = body_type
        item["che_level"] = che_level
        item["trunk_cap"] = trunk_cip
        # print(item)
        yield item

    def get_value(self, value):  # 数据为空的处理方法
        value = value[0] if value else 1
        return value
