# webscraper-popsockets
Scrapes popsocket website for product data using selenium.

I chose the popsocket website for this project as I am quite interested in the surprising amount of product innovation in this fairly niche market.

In this case I am dealing with the UK website but attempting to maintain compatibility with other regional sites, though this may take some testing at a later time.

## Dealing with cookies and offer popups
Initially the trigger for a offer popup seemed complex, but eventually realised implementing a long enough wait for the element to appear was sufficient, another solution would be to inject css to set the element to display:none!important.

## Getting product category data
Unfortunately this site does not expose full product type/category on each product page, so to get this data have to scrape each product category page for a list of all products under this category, which then can be compiled into a list of category types for each product.

At first I tried to make a dictionary of sets containing category types for each product with the key being the product url, and thought to use a recursive implementation for category pages, possibly building some sort of tree datatype, but decided this was unwieldy for the initial crawl and chose to just use a list of urls that I can split the strings of to extract category data, though this implementation could still be added later.

The choice of product URL over another value for a unique identifier was made because, although there is a pid exposed in the DOM that appears to be conserved, I will be working with query-stripped URLs primarily anyway. I will scrape pid and may choose to switch to pid as identifier at a later time if this does appear to be well conserved. From what I can see of pid naming schemes, there does not seem a consistent or logical enough naming scheme to bother relying on anyway.

## Getting product data
Aside from category data, the product data I can see consistently scraping are price, pid, name, description text (including hidden copy I discovered that is not displayed on the product page), review score, available colours and other options such as phone compatibility where available.
