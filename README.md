# webscraper-popsockets
Scrapes popsocket website for product data using selenium


to get category data have to scrape each product category page, at first tried to make a dictionary of sets containing category types for each product with the key being the url for the product, tried to use a recursive version of this for category pages, possibly with the idea of building a category tree datatype, later decided this was unwieldy for initial crawl and chose to just use a list of urls that I would split the strings of to extract category data.