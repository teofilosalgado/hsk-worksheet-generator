import os

from zipfile import ZipFile
from random import choice
from string import ascii_uppercase, ascii_lowercase, digits

from scrapy.exporters import BaseItemExporter
from scrapy.exporters import CsvItemExporter
from scrapy.utils.python import to_bytes


class CustomCsvItemExporter(CsvItemExporter):
    def __init__(self, *args, **kwargs):
        kwargs["encoding"] = "utf-8"
        kwargs["delimiter"] = ";"
        super(CustomCsvItemExporter, self).__init__(
            *args, **kwargs, include_headers_line=False
        )

class CustomMochiItemExporter(BaseItemExporter):
    def __init__(self, file, **kwargs):
        print(kwargs)
        self._configure(kwargs, dont_fail=True)
        # Keeps reference of the output file path for .zip compression later
        self.json_file_path = os.path.abspath(file.name)
        self.json_file = file
        # Output folder where the compressed .zip/.mochi file will be created
        self.output_folder_path = os.path.dirname(self.json_file_path)
        # Prevents dangling commas
        self.is_first_item = True
        # Keeps cards in order
        self.position = 0
        self.template = """
                    %s{
                        "~:pos": "%s",
                        "~:id": "~:%s",
                        "~:template-id": "~:JyNTqOWw",
                        "~:content": "",
                        "~:name": "打电话",
                        "~:fields": {
                            "~:name": {
                                "~:id": "~:name",
                                "~:value": "%s"
                            },
                            "~:mBQDvQJd": {
                                "~:id": "~:mBQDvQJd",
                                "~:value": "%s"
                            },
                            "~:HVbfyxAT": {
                                "~:id": "~:HVbfyxAT",
                                "~:value": "%s"
                            },
                            "~:CvHut85d": {
                                "~:id": "~:CvHut85d",
                                "~:value": "%s"
                            }
                        }
                    }"""

    def _generate_id(self) -> str:
        return ''.join(choice(ascii_uppercase + ascii_lowercase + digits) for i in range(8))


    def _read_file(self, file_name:str) -> str:
        file_path = os.path.join(
            os.path.abspath(os.getcwd()),
            "input",
            "mochi",
            file_name
        )
        with open(file_path, encoding="utf-8") as file:
            return file.read()


    def start_exporting(self):
        self.json_file.write(to_bytes(self._read_file("start_exporting.json")))

    def finish_exporting(self):
        self.json_file.write(to_bytes(self._read_file("finish_exporting.json")))
        temporary_data_file_path = os.path.join(
             self.output_folder_path, 
             f"{self._generate_id()}.json"
        )
        os.rename(self.json_file_path, temporary_data_file_path)
        with ZipFile(self.json_file_path, "w") as zip_file:
            zip_file.write(temporary_data_file_path, arcname="data.json")
        os.remove(temporary_data_file_path)


    def export_item(self, item):
        fields = dict(self._get_serialized_fields(item))
        self.json_file.write(to_bytes(
            self.template % (
                    "" if self.is_first_item else ",",
                    str(self.position),
                    self._generate_id(),
                    fields["chinese"],
                    fields["english"],
                    fields["pinyin"],
                    fields["category"]
                )
            )
        )
        self.is_first_item = False
        self.position = self.position + 1
