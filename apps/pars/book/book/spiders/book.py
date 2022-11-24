from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from book.items import BookItem

from slugify import *


class GenreSpider(CrawlSpider):   # scrapy.Spider
    name = 'genre'
    start_urls = ['https://mybook.ru/']

    # def __init__(self):
    #     self.data = []
    #     self.rules = (
    #     Rule(LinkExtractor(allow='catalog/books')),
    #     Rule(LinkExtractor(allow='author'), callback='parse_books')
    #     )
    #     self.data.extend(self.rules)
    rules = (
            Rule(LinkExtractor(allow='catalog/malaya-forma/books/')),
            Rule(LinkExtractor(allow='author'), callback='parse_genre')
            )

    def parse_genre(self, response):
        # book_item = BookItem()
        # jobs = []

        genres_list = response.css('div.sc-1sg8rha-0.gHinNz div a::text').extract()

        for topic in genres_list:
            # book_item['genre'] = topic.capitalize()
            # book_item['slug'] = slugify(topic)
            global genre
            genre = topic.capitalize()
            # global slug
            # slug = slugify(genre)
            # jobs.append(genres)
            # jobs.append(slug)

        yield {
            'genre': genre
            # 'slug': slug
        }
        # return book_item


class AuthorSpider(CrawlSpider):   # scrapy.Spider
    name = 'author'
    start_urls = ['https://mybook.ru/']

    # def __init__(self):
    #     self.data = []
    #     self.rules = (
    #     Rule(LinkExtractor(allow='catalog/books')),
    #     Rule(LinkExtractor(allow='author'), callback='parse_books')
    #     )
    #     self.data.extend(self.rules)
    rules = (
        Rule(LinkExtractor(allow='catalog/malaya-forma/books/')),
        Rule(LinkExtractor(allow='author'), callback='parse_author')
        )

    def parse_author(self, response):
        name = response.css('div.dey4wx-1.jVKkXg::text').get().replace('&nbsp;', ' ')
        first_name = name.split()[0]
        last_name = name.split()[1]
        avatar = response.xpath('//div/picture/source/@srcset').get().split(',')[0]   
        bio = response.css('div.iszfik-2.gAFRve p::text').get() 
        # slug = slugify(name)

        yield { 
            'first_name': first_name,
            'last_name': last_name,
            'avatar': avatar,
            'bio': bio,
            'name': name 
            # 'slug': slug
        }

        # return author


class BookSpider(CrawlSpider):   # scrapy.Spider
    name = 'book'
    start_urls = ['https://mybook.ru/']

    # def __init__(self):
    #     self.data = []
    #     self.rules = (
    #     Rule(LinkExtractor(allow='catalog/books')),
    #     Rule(LinkExtractor(allow='author'), callback='parse_books')
    #     )
    #     self.data.extend(self.rules)
    rules = (
        Rule(LinkExtractor(allow='catalog/malaya-forma/books/')),
        Rule(LinkExtractor(allow='author'), callback='parse_book')
        )

    def parse_book(self, response):
        # title = response.css('h1.sc-bdfBwQ.lnjchu-0.jzwvLi.gUKDCi.sc-1c0xbiw-11.bzVsYa::text').get().replace('&nbsp;', ' ')
        title = response.xpath('//div/section/div[1]/div[3]/div[1]/div/div/div[3]/div/h1').get().replace('&nbsp;', ' ')
        # slug = slugify(title)
        image_link = response.xpath('//div/picture/source/@srcset').get().split(',')[0]    
        description = response.css('div.iszfik-2.gAFRve p::text').get() 
        genres = response.css('div.sc-1sg8rha-0.gHinNz div a::text').extract()
        author = response.css('div.dey4wx-1.jVKkXg::text').get().replace('&nbsp;', ' ')
        pages = response.css('div.ant-col.sc-1c0xbiw-9.bhxaWx.ant-col-xs-11.ant-col-md-8.ant-col-xl-12 p.lnjchu-1.dPgoNf::text').get().split(' ')[0]
        year = response.xpath('//*[@id="__next"]/div/section/div[1]/div[3]/div[1]/div/div/div[5]/p[2]/text()[1]').get().replace('&nbsp;', ' ').split()[0]
        # "//div[@aria-label='bedrooms']/div[2]/text()"
        # number_of_copies = random.randint(1, 10)
        # number_available = number_of_copies - 1
        status = 'available'

        book = {
            'title': title,
            'image_link': image_link,
            'description': description,
            # 'slug': slug,
            'genre': genres,
            # 'number_of_copies': random.randint(1, 10),
            # 'number_available': number_available,
            'year': year,
            'pages': pages,
            'author': author,
            'status': status 
            }
        