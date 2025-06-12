#!/bin/bash

echo "Starting periodic scraper..."

while true; do
    echo "Running scraper at $(date)..."
    cd /app/scraper && scrapy crawl menu -O output/products.json

    if [ $? -eq 0 ]; then
        echo "Scraping completed successfully!"
    else
        echo "Scraping failed!"
    fi

    echo "Next scrape in 24 hours..."
    sleep 86400
done
