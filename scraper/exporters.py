from scrapy.exporters import CsvItemExporter


class CustomCsvItemExporter(CsvItemExporter):
    def __init__(self, *args, **kwargs):
        kwargs["encoding"] = "utf-8"
        kwargs["delimiter"] = ";"
        super(CustomCsvItemExporter, self).__init__(
            *args, **kwargs, include_headers_line=False
        )
