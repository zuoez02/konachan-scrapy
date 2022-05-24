#!/bin/bash
if [ -z "$@" ]; then
    echo "no tags"
    exit 1
fi
scrapy crawl post -a tag="$@"