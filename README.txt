To run the Crawler Successfully follow the instructions -

1. First install all the dependencies using requirements.txt by command pip install -r requirements.txt

2. After that open cmd and go to the folder where scrapy.cfg file is present

3. After that write this command to run the crawler
	scrapy crawl scraper -a tag=dentist -L WARN

 where you can define any tag you want

4. Once scraping start it will automatically start storing data in Database. (Its a sqlite3 databse)

5. If you want to store data in any other file as well like csv or json etc. you can run this command
	scrapy crawl scraper -a tag=dentist -L WARN -o Output.csv

6. Proxies and useragents are handled by middlewares already. Proxies takes time to authenticate, so it might decrease speed a lil, in case if you dont want to use proxy you can go to settings.py file and comment PROXY_POOL_ENABLED line.

7. We are also using text converter in order to to convert any other language to english, so it might be also decrease limit, and you dont want conversion to increase speed which will be very quick , you can go to spider folder and then scraper.py file and under function convert , comment first three line and uncomment fourth line.


8. That's it




I already scraped for dentist in toronto and data is stored in the db. YOu can check or delete it to scrap again and store from start.

Thanks