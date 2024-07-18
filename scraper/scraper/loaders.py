from itemloaders.processors import TakeFirst
from scrapy.loader import ItemLoader


class WordLoader(ItemLoader):
    default_output_processor = TakeFirst()
