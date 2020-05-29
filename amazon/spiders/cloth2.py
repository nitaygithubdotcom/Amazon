# -*- coding: utf-8 -*-
import scrapy


class ClothSpider(scrapy.Spider):
    name = 'cloth2'
    def start_requests(self):
        urls = [
         'https://www.amazon.in/s?i=apparel&bbn=21474867031&rh=n%3A1571271031%2Cn%3A21474867031%2Cn%3A1968024031%2Cn%3A1968076031&dc&fst=as%3Aoff&pf_rd_i=1968024031&pf_rd_m=A1VBAL9TL5WCBF&pf_rd_p=10f212f8-0f78-4a5b-877b-301f366ced10&pf_rd_r=A649MS3EEJF4QWCW9FBC&pf_rd_s=merchandised-search-6&qid=1588499754&rnid=1968024031&swrs=96BF3E794088A846A0B3BB883E276DB8&ref=sr_nr_n_3/',
         'https://www.amazon.in/s?i=apparel&bbn=21474867031&rh=n%3A1571271031%2Cn%3A21474867031%2Cn%3A1968024031%2Cn%3A1968076031&dc&page=2&fst=as%3Aoff&pf_rd_i=1968024031&pf_rd_m=A1VBAL9TL5WCBF&pf_rd_p=10f212f8-0f78-4a5b-877b-301f366ced10&pf_rd_r=A649MS3EEJF4QWCW9FBC&pf_rd_s=merchandised-search-6&qid=1588765633&rnid=1968024031&swrs=96BF3E794088A846A0B3BB883E276DB8&ref=sr_pg_1'   
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    # start_urls = ['https://www.amazon.in/s?i=apparel&bbn=21474867031&rh=n%3A1571271031%2Cn%3A21474867031%2Cn%3A1968024031%2Cn%3A1968076031&dc&fst=as%3Aoff&pf_rd_i=1968024031&pf_rd_m=A1VBAL9TL5WCBF&pf_rd_p=10f212f8-0f78-4a5b-877b-301f366ced10&pf_rd_r=A649MS3EEJF4QWCW9FBC&pf_rd_s=merchandised-search-6&qid=1588499754&rnid=1968024031&swrs=96BF3E794088A846A0B3BB883E276DB8&ref=sr_nr_n_3/']
    
    def parse(self, response):
        page = response.url.split('/')[-2]
        filename = 'cloths-%s.html' % page
        with open(filename,'wb') as f:
            f.write(response.body)
        self.log('saved file %s' % filename)

        
        xpname = '(//div[@id="mainResults"]/ul/li)[{}]/div/div[last()]/div/a/h2/text()'
        xpprice = '(//div[@id="mainResults"]/ul/li)[{}]/div/div[last()]/div[@class="a-row a-spacing-none"]/a/span/text()'
        xprate = '(//div[@id="mainResults"]/ul/li)[{}]/div/div[last()]/div[@class="a-row a-spacing-top-mini a-spacing-none"]//span[@class="a-icon-alt"]/text()'
        for i in range(len(response.xpath('(//div[@id="mainResults"]/ul/li)'))):
            namexp = xpname.format(i+1)
            pricexp = xpprice.format(i+1)
            ratexp = xprate.format(i+1)
            name = response.xpath(namexp).get()
            price = response.xpath(pricexp).get()
            rating = response.xpath(ratexp).get()
            # yield {"Product Name":name,"Price":price.strip(' -'),"Rating":rating}

        nextpage = response.xpath('//a[@title="Next Page"]/@href').get()
        print(nextpage)
        if nextpage is not None:
            nextpage = response.urljoin(nextpage)
            print(nextpage)
            yield scrapy.Request(nextpage, callback=self.parse)
        