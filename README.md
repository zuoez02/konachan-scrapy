# Konachan scrapy

Konachan.com is a wallpaper image websit. To scrap pictures, I write this spider.

## Install

You should install python3, pip, scrapy.

## Usage

Run `scrapy crawl post -a tag="TAGS"`, where TAGS are tag you want to search like it is in website.

## Arguments

```

scrapy crawl post
    -a clear=true   # clear current search cache
    -a stop=false   # not stop download when match cache
    -a tag='TAGS'   # search tags

```

## Configuration

To config where the pictures are downloaded, edit the config in konachan/settings.py `FILES_STORE`

## License

MIT