import scrapy
from scrapy.http import Request
from utils import common


class PagesSpider(scrapy.Spider):
    name = "pages"

    def __init__(self, **kw):
        """Receives the URL to page through.

        Raises:
            Exception: If no URL was passed.
        """        
        super(PagesSpider, self).__init__(**kw)
        self.start_urls = kw.get('urls') or 'dummy'
        if self.start_urls == 'dummy':
            raise Exception('No URL was passed to the pages spider, only: {}'.format(kw))
        elif not isinstance(self.start_urls, list):
            raise Exception('URLs should be in a list object, we received: {}'.format(kw))
        
        self.page_type = kw.get('page_type')
        self.section = kw.get('section')


    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, callback=self.parse, cb_kwargs={'section': self.section, 'page_type': self.page_type, 'visited': []})


    def parse(self, response, **cb_kwargs):
        href = response.css('.rgPagerCell').xpath('.//a')
        kwargs = cb_kwargs
        event_target = None

        for link in href:
            js_function = link.xpath('./@href').get()
            if not js_function:
                break

            if js_function not in kwargs['visited']:
                if link.xpath('./@class'):
                    kwargs['visited'].append(js_function)
                    continue
                else:
                    event_target = js_function.replace(
                        "javascript:__doPostBack('", "").replace("','')", "")
                    kwargs['visited'].append(js_function)
                    break

        event_argument = response.css(
            '#__EVENTARGUMENT::attr(value)').extract()
        last_focus = response.css('#__LASTFOCUS::attr(value)').extract()
        view_state = response.css('#__VIEWSTATE::attr(value)').extract()
        view_state_generator = response.css(
            '#__VIEWSTATEGENERATOR::attr(value)').extract()
        view_state_encrypted = response.css(
            '#__VIEWSTATEENCRYPTED::attr(value)').extract()

        page_type = kwargs['page_type']
        if page_type == 'index':
            rows = response.css('.rgMasterTable').xpath('./tbody/tr')
            metadata = None
        elif page_type == 'series':
            rows = response.css('.rgMasterTable').xpath('./tbody/tr')
            metadata = response.xpath("//table[@id='MainContent_SeriesPane_tableStatus']")
        else:
            rows = None
            metadata = None

        yield {
            'link': response.url,
            'section': kwargs['section'],
            'rows': rows,
            'metadata': metadata,
            'page_type': page_type
        }

        if event_target:
            yield scrapy.FormRequest(
                response.url,
                formdata={
                    '__EVENTTARGET': event_target,
                    '__EVENTARGUMENT': event_argument,
                    '__LASTFOCUS': last_focus,
                    '__VIEWSTATE': view_state,
                    '__VIEWSTATEGENERATOR': view_state_generator,
                    '__VIEWSTATEENCRYPTED': view_state_encrypted
                },
                callback=self.parse,
                cb_kwargs=kwargs
            )
