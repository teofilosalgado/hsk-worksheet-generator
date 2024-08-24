from typing import List, Union

from scrapy import Selector
from scrapy.http import Response
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from hsk_worksheet_generator.items import Word
from hsk_worksheet_generator.loaders import WordLoader

VOCAULARY_XPATH = "//p/span/a[contains(@href, '/chinese/vocabulary/HSK')]"


class AllSetLearningSpider(CrawlSpider):
    name = "AllSetLearning"
    allowed_domains = ["resources.allsetlearning.com"]

    def _build_regex_url(self, hsk: str):
        match hsk:
            case "1":
                return rf"/chinese/vocabulary/HSK_{hsk}_Vocabulary$"
            case _:
                return rf"/chinese/vocabulary/HSK_{hsk}_Vocabulary_\(exclusive\)$"

    def __init__(self, hsk: Union[str, None] = None, *args, **kwargs):
        if hsk is None:
            raise RuntimeError('Missing "hsk" argument')

        self.start_urls = ["https://resources.allsetlearning.com/chinese/vocabulary"]
        self.rules = [
            Rule(
                LinkExtractor(
                    allow=(self._build_regex_url(hsk),),
                    unique=True,
                ),
                follow=False,
                callback="parse_item",
            )
        ]

        super(AllSetLearningSpider, self).__init__(*args, **kwargs)

    def parse_item(self, response: Response):
        tables: List[Selector] = response.xpath(
            "//table[contains(@class, 'table')]/tbody"
        )
        categories: List[str] = [
            selector.get()
            for selector in response.xpath(
                "//h2/span[contains(@class, 'mw-headline')]/a/text()"
            )  # type: ignore
        ]
        for category, table in zip(categories, tables):
            rows = table.xpath("./tr[td]")
            for index, row in enumerate(rows):
                word = WordLoader(item=Word(), selector=row)
                word.add_value("id", index)
                word.add_value("category", category)
                word.add_xpath("chinese", "td[1]/text()")
                word.add_xpath("pinyin", "td[2]/text()")
                word.add_xpath("english", "td[3]/text()")
                yield word.load_item()
