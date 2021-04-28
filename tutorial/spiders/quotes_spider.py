import scrapy
from unidecode import unidecode

class NFSSpider(scrapy.Spider):
    name = 'nfs'
    start_urls = [
        'https://www.sparknotes.com/nofear/shakespeare/antony-and-cleopatra/page_2/',
        'https://www.sparknotes.com/nofear/shakespeare/asyoulikeit/page_2/',
        'https://www.sparknotes.com/nofear/shakespeare/errors/page_2/',
        'https://www.sparknotes.com/nofear/shakespeare/coriolanus/page_2/',
        'https://www.sparknotes.com/nofear/shakespeare/hamlet/page_2/',
        'https://www.sparknotes.com/nofear/shakespeare/henry4pt1/page_3/',
        'https://www.sparknotes.com/nofear/shakespeare/henry4pt2/page_265/',
        'https://www.sparknotes.com/nofear/shakespeare/henryv/page_2/',
        'https://www.sparknotes.com/nofear/shakespeare/juliuscaesar/page_2/',
        'https://www.sparknotes.com/nofear/shakespeare/lear/page_2/',
        'https://www.sparknotes.com/nofear/shakespeare/macbeth/page_2/',
        'https://www.sparknotes.com/nofear/shakespeare/measure-for-measure/page_2/',
        'https://www.sparknotes.com/nofear/shakespeare/merchant/page_2/',
        'https://www.sparknotes.com/nofear/shakespeare/msnd/page_2/',
        'https://www.sparknotes.com/nofear/shakespeare/muchado/page_2/',
        'https://www.sparknotes.com/nofear/shakespeare/othello/page_2/',
        'https://www.sparknotes.com/nofear/shakespeare/richardii/page_2/',
        'https://www.sparknotes.com/nofear/shakespeare/richardiii/page_2/',
        'https://www.sparknotes.com/nofear/shakespeare/romeojuliet/page_2/',
        'https://www.sparknotes.com/nofear/shakespeare/shrew/page_2/',
        'https://www.sparknotes.com/nofear/shakespeare/twelfthnight/page_2/',
        'https://www.sparknotes.com/nofear/shakespeare/twogentlemen/',
        'https://www.sparknotes.com/nofear/shakespeare/winterstale/',
        'https://www.sparknotes.com/nofear/shakespeare/sonnets/sonnet_1/',
    ]

    def parse(self, response):
        original = self.extract_text(response, 'td.noFear__cell--original')
        modern = self.extract_text(response, 'td.noFear__cell--modern')
        for o, m in zip(original, modern):
            yield {
                'original':o,
                'modern':m,
            }

        next_page = self.get_next_page_link(response)
        if next_page is not None:
            yield scrapy.Request(next_page, callback=self.parse)

    def get_next_page_link(self, response):
        next_button = response.css('a.page-turn-nav__link--next')
        try:
            href = next_button.attrib['href']
            return response.urljoin(href)
        except:
            return None

    def extract_text(self, response, css_tag):
        """
        Given a css tag, extract all lines of text. Return lines as list of strings.
        css_tad: 'td.noFear__cell--original' or 'td.noFear__cell--modern'
        """
        assert css_tag in ['td.noFear__cell--original', 'td.noFear__cell--modern']
        rows = response.css(css_tag) # extract all table rows

        lines = []
        for row in rows:
            text = row.css('div.noFear__line::text').getall() # only grab spoken lines
            if len(text) > 0: # if no spoken lines on this row (stage instructions, speaker name, etc)
                # text = row.css('::text').getall() # extract text-only, returns list of strings
                text = (' '.join(text)).split()  # remove whitespace and split into individual strings
                text = ' '.join(text) # combine into single string

                text = unidecode(text) # convert bad unicode to ascii
                text = text.replace("\"", "") # drop internal quotation marks

                # text = ''.join([i for i in text if not i.isdigit()]) # remove line number
                lines.append(text)
        return lines


"""
a.page-turn-nav__link--next
"""
