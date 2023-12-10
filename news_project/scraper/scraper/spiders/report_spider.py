import scrapy


class ReportSpider(scrapy.Spider):
    name = 'report_spider'

    start_urls = [
        'https://news.am/eng/news/allregions/allthemes/2023/12/09/',
    ]

    def parse(self, response):
        for article in response.css('article.article-item'):
            image_url = article.css('img::attr(src)').get()
            if not image_url.startswith('http'):
                image_url = ''.join(('https://news.am', image_url))

            data = {
                'text': article.css('div.text::text').get(),
                'image_url': image_url,
                'title': article.css('div.title a::text').get(),
            }

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
        image_url = main_data['image_url']

        combined_data = {**main_data, 'sub_text': ''.join(text_list)}

        yield scrapy.Request(image_url, callback=self.parse_image,
                             meta={'combined_data': combined_data})

    def parse_image(self, response):
        image_bytes = response.body
        combined_data = response.meta['combined_data']

        # Include the image_bytes in the final output
        combined_data['image_bytes'] = image_bytes

        yield combined_data
