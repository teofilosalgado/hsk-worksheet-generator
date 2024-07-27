#!/bin/bash

if [ -z "$1" ]
    then
        echo "Missing minimum HSK level parameter" >&2
        exit 1
fi

minimum_hsk_level=$1

if [ -z "$2" ]
    then
        maximum_hsk_level=$minimum_hsk_level
else
    maximum_hsk_level=$2
fi

for level in $(eval echo {$1..$2});
do
    # Get HSK words from AllSet Learning
    poetry run python -m scrapy crawl AllSetLearning -L WARNING -a hsk=$level -O ./output/hsk_$level.csv;

    # Compile data to PDF
    typst compile template/main.typ output/hsk_$level.pdf --font-path font --root . --input hsk="$level" --input csv_file_path="../output/hsk_$level.csv";
done

pushd ./output

# Compress .csv files
zip -j -qq hsk.csv.zip *.csv;

# Compress .pdf files
zip -j -qq hsk.pdf.zip *.pdf;

popd