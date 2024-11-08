import scrapy


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):

         # Selettore per tutti gli articoli dei libri
        books = response.css('article.product_pod')

        # Ingresso nel dettaglio prodotto
        for book in books:
            relative_url = book.css('h3 a::attr(href)').get()
            if 'catalogue/' in relative_url:
              book_url = 'https://books.toscrape.com/' + relative_url
            else:
              book_url = 'https://books.toscrape.com/catalogue/' + relative_url  
            yield response.follow(book_url, callback=self.parse_book_page) 

        next_page = response.css('li.next a::attr(href)').get()

        if next_page is not None:
            if 'catalogue/' in next_page:
              next_page_url = 'https://books.toscrape.com/' + next_page
            else:
              next_page_url = 'https://books.toscrape.com/catalogue/' + next_page  
            yield response.follow(next_page_url, callback=self.parse) 

    # Funzione scraping del dettaglio prodotto
    def parse_book_page(self, response):
       yield{
          'titolo' : response.css('div.product_main h1::text').get(), 
          'prezzo' : response.css('div.product_main p.price_color::text').get(),
          'rating' : response.css('div.product_main p.star-rating::attr(class)').get().split()[-1],
          'tipo_prodotto' : response.css('ul.breadcrumb li:nth-child(2) a::text').get(),
          'categoria_prodotto' : response.css('ul.breadcrumb li:nth-child(3) a::text').get(), 
          'disponibilità' :  response.xpath('.//th[text()="Availability"]/following-sibling::td/text()').get(),
          'recensioni' : response.xpath('.//th[text()="Number of reviews"]/following-sibling::td/text()').get()
       }
