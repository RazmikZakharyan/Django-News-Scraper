import scrapy


class ReportSpider(scrapy.Spider):
    name = 'report_spider'

    start_urls = [
        'https://news.am/eng/news/allregions/allthemes/',
    ]

    def parse(self, response):
        for article in response.css('article.article-item'):
            data = {
                'text': article.css('div.text::text').get(),
                'image': article.css('img::attr(src)').get(),
                'title': article.css('div.title a::text').get(),
            }

            if not data['image'].startswith('http'):
                data['image'] = ''.join(('https://news.am', data['image']))

            sub_url = article.css('a.photo-link::attr(href)').get()
            yield response.follow(
                url=sub_url,
                callback=self.parse_subpage,
                meta={'main_data': data}
            )

    def parse_subpage(self, response):
        css_path = (
            'div#opennewstext p::text',
            'span.article-body p span::text',
            'span.article-body p::text',
        )
        text_list = ()
        for item in css_path:
            text_list = response.css(item).extract()
            if text_list:
                break

        main_data = response.meta['main_data']

        combined_data = {**main_data, 'sub_text': ''.join(text_list)}

        yield combined_data
