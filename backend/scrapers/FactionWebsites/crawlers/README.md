Scrapers depend on:
 - scrapy
 - html2text
 - beautifulsoup4

Run a scraper with:
`scrapy runspider --set FEED_EXPORT_ENCODING=utf-8 --set LOG_LEVEL=INFO <scraperfile>.py -o output.json`
