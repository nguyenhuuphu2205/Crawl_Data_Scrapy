# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
import json

script = """
function main(splash)
    splash:init_cookies(splash.args.cookies)
    local url = splash.args.url
    assert(splash:go(url))
    assert(splash:wait(5))
    return {
        cookies = splash:get_cookies(),
        html = splash:html()
    }
end
"""

script2 = """
function main(splash)
    splash:init_cookies(splash.args.cookies)
    local url = splash.args.url
    assert(splash:go(url))
    assert(splash:wait(5))
    return {
        cookies = splash:get_cookies(),
        html = splash:html()
    }
end
"""


class VnexpressSpiderComment(scrapy.Spider):
    name = 'vnexpress_comment'
    start_urls = ["https://vnexpress.net/kinh-doanh"]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, endpoint='execute',
                                args={'lua_source': script2,'wait':2})

    def parse(self, response):
        for text in response.css('.sidebar_1 h4'):
            url = text.css('a::attr(href)').get()
            # yield response.follow(url, self.vnexpress_parse)
            yield SplashRequest(url, self.parse, endpoint='execute',
                                args={'lua_source': script2,'wait':2})
            # for next_page in response.css('.next::attr(href)'):
        # next_page = response.css('.next::attr(href)').get()
        # if next_page is not None:
        #     # next_page = response.urljoin(next_page)
        #     yield SplashRequest(next_page, self.parse, endpoint='execute',
        #                         args={'lua_source': script2})



    # def parse_item(self, response):
    #     def get_id_user(comment):
    #         url = str(comment.css('a.nickname.txt_666::attr(href)').get())
    #         if url is  None:
    #             url = str(comment.css('a.nickname.txt_666.hover::attr(href)').get())
    #         if "users" in url:
    #             return url.split('/')[-1]
    #         else:
    #             return None
    #     def extract_comment():
    #         a = []
    #         list_comment = response.css('div.comment_item.width_common')
    #         for comment in list_comment:
    #             tmp1 = {
    #                 'name': comment.css('b::text').get(),
    #                 'id':get_id_user(comment),
    #                 'comment': comment.css('p.full_content::text').get(),
    #                 'like': comment.css('span.txt_666.txt_11.total_like::text').get()
    #             }
    #             a.append(tmp1)
    #         sub_comment = response.css('div.sub_comment_item.width_common')
    #         for sub_comment_item in sub_comment:
    #             tmp2 = {
    #                 'name': sub_comment_item.css('b::text').get(),
    #                 'id':get_id_user(sub_comment_item),
    #                 'comment': sub_comment_item.css('p.full_content::text').get(),
    #                 'like': sub_comment_item.css('span.txt_666.txt_11.total_like::text').get()
    #             }
    #             a.append(tmp2)
    #         tmp3 = {'title': response.css('h1.title_news_detail.mb10::text').get(),
    #                 'subtitle': response.css('p.description::text').get(),
    #                 'subject': response.css('li.start a::text').get(),
    #                 'time': response.css('header span.time.left::text').get(),
    #                 'total_comment': response.css('label::text').get(),
    #                 'comment':a
    #                 }
    #
    #         return tmp3
    #
    #     return extract_comment()
    def parse_item(self, response):
        def extract_data(query):
            data = response.css(query).get()
            if data is not None:
                return data.replace("\n", "").replace("\t", "")
            else:
                return data
        def get_id_user(comment):
            url = str(comment.css('a.nickname.txt_666::attr(href)').get())
            if url is  None:
                url = str(comment.css('a.nickname.txt_666.hover::attr(href)').get())
            if "users" in url:
                return url.split('/')[-1]
            else:
                return None
        def extract_comment():
            a=[]
            list_comment = response.css('div.comment_item.width_common')
            for comment in list_comment:
                tmp1= {
                    'name':comment.css('b::text').get(),
                    'id':str(comment.css('a.nickname.txt_666::attr(href)').get()).split('/')[-1],
                    'comment':comment.css('p.full_content::text').get(),
                    'like' : comment.css('span.txt_666.txt_11.total_like::text').get()
                }
                print get_id_user(comment)
                # tmp1=comment.css('p.full_content::text').get()
                a.append(tmp1)
            sub_comment = response.css('div.sub_comment_item.width_common')
            for sub_comment_item in sub_comment:
                tmp2 = {
                    'name': sub_comment_item.css('b::text').get(),
                    'id': str(comment.css('a.nickname.txt_666.hover::attr(href)').get()).split('/')[-1],
                    'comment':sub_comment_item.css('p.full_content::text').get(),
                    'like': sub_comment_item.css('span.txt_666.txt_11.total_like::text').get()
                }
                print get_id_user(sub_comment_item)
                # tmp2= sub_comment_item.css('span.txt_666.txt_11.total_like::text').get()
                a.append(tmp2)
            tmp3 = {'title': response.css('h1.title_news_detail.mb10::text').get(),
                    'subtitle': response.css('p.description::text').get(),
                    'subject':response.css('li.start a::text').get(),
                    'time':response.css('header span.time.left::text').get(),
                    'total_comment':response.css('label::text').get(),
                    'comment':a
                    }
            # a.append(tmp3)

            return tmp3
        return extract_comment()

