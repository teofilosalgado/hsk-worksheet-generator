import os
from random import choice
from string import ascii_lowercase, ascii_uppercase, digits
from zipfile import ZipFile

from scrapy.exporters import BaseItemExporter, CsvItemExporter
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
                    {comma}{{
                        "~:pos": "{position}",
                        "~:id": "~:{id}",
                        "~:template-id": "~:JyNTqOWw",
                        "~:content": "",
                        "~:name": "{chinese}",
                        "~:fields": {{
                            "~:name": {{
                                "~:id": "~:name",
                                "~:value": "{chinese}"
                            }},
                            "~:mBQDvQJd": {{
                                "~:id": "~:mBQDvQJd",
                                "~:value": "{english}"
                            }},
                            "~:HVbfyxAT": {{
                                "~:id": "~:HVbfyxAT",
                                "~:value": "{pinyin}"
                            }},
                            "~:CvHut85d": {{
                                "~:id": "~:CvHut85d",
                                "~:value": "{category}"
                            }}
                        }}
                    }}"""

    def _generate_id(self) -> str:
        return "".join(
            choice(ascii_uppercase + ascii_lowercase + digits) for i in range(8)
        )

    def _read_file(self, file_name: str) -> str:
        file_path = os.path.join(
            os.path.abspath(os.getcwd()), "input", "mochi", file_name
        )
        with open(file_path, encoding="utf-8") as file:
            return file.read()

    def start_exporting(self):
        self.json_file.write(to_bytes(self._read_file("start_exporting.json")))

    def finish_exporting(self):
        self.json_file.write(to_bytes(self._read_file("finish_exporting.json")))
        self.json_file.flush()
        self.json_file.close()

        temporary_data_file_path = os.path.join(
            self.output_folder_path, f"{self._generate_id()}.json"
        )
        os.rename(self.json_file_path, temporary_data_file_path)
        with ZipFile(self.json_file_path, "w") as zip_file:
            zip_file.write(temporary_data_file_path, arcname="data.json")
        os.remove(temporary_data_file_path)

    def export_item(self, item):
        fields = dict(self._get_serialized_fields(item))
        self.json_file.write(
            to_bytes(
                self.template.format(
                    comma="" if self.is_first_item else ",",
                    position=self.position,
                    id=self._generate_id(),
                    chinese=fields["chinese"],
                    english=fields["english"],
                    pinyin=fields["pinyin"],
                    category=fields["category"],
                )
            )
        )
        self.is_first_item = False
        self.position = self.position + 1
