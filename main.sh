#!/bin/bash

for level in {1..3}
do
    # Get HSK words from AllSet Learning
    pushd scraper;
    scrapy crawl AllSetLearning -a hsk=$level -O ../output/hsk_$level.csv;
    popd;

    # Compile data to PDF
    typst compile template/main.typ output/hsk_$level.pdf --font-path font --root . --input hsk="$level" --input csv_file_path="../output/hsk_$level.csv";
done


