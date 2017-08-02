# -*- coding: utf-8 -*-
import scrapy


class LatestEpisodeSpider(scrapy.Spider):
    name = 'latest_episode'

    def __init__(self, show="", *args, **kwargs):
        super(LatestEpisodeSpider, self).__init__(*args, **kwargs)
        url = "http://www.imdb.com/find?ref_=nv_sr_fn&q="
        url += show + "&s=all"
        self.allowed_domains = ['www.imdb.com']
        self.start_urls = [url]

    def parse(self, response):
        link_to_main_page = response.css(
            'td.result_text a::attr(href)').extract_first()
        link_to_main_page = response.urljoin(link_to_main_page)
        yield scrapy.Request(url=link_to_main_page, callback=self.parse_main_page)

    def parse_main_page(self, response):
        ep_code = response.url[:35]
        ep_url = ep_code + '/episodes'
        yield scrapy.Request(url=ep_url, callback=self.parse_ep_page)

    def parse_ep_page(self, response):
        div_count=0
        for div in response.css('div#episodes_content div.clear div.list.detail.eplist>div'):
        	episode = {
        		'title' : div.css('strong a::text').extract_first(),
        		'air_date' : div.css('div.info div.airdate::text').extract_first().strip(),
        		'description' : div.css('div.item_description::text').extract_first().strip()
        		}
        	print(episode)
        	yield episode
        
        	
        	


        
        
