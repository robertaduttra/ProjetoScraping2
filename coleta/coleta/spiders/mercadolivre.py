#scrapy startproject coleta - cria pasta coleta
#scrapy genspider mercadolivre https://lista.mercadolivre.com.br/tenis-corrida-masculino dentro da coleta cria spider
#scrapy shell - dentro terminal
#fetch('https://lista.mercadolivre.com.br/tenis-corrida-masculino')
# pega user agente my no google - Seu user-agent USER_AGENT NA PASTA SETTING.PY e tanta novamente o scrapy shell
#response.css('div.ui-search-result__content')
#len(response.css('div.ui-search-result__content')) - quantidade itens da pagina
#criar variavel products = response.css('div.ui-search-result__content')
#products.css('span.ui-search-item__brand-discoverability.ui-search-item__group__element') - tiver espaco poe ponto
#products.css('span.ui-search-item__brand-discoverability.ui-search-item__group__element').get() retorna 1
#products.css('span.ui-search-item__brand-discoverability.ui-search-item__group__element::text').get() - traz somente o texto do elemento.
# salva nem um json * scrapy crawl mercadolivre -o data.jsonl
#prices = products[0] .css('span.andes-money-amount__fraction::text').getall() - lista com os 3 e categorizar
#pedi p ele nao obdecer o robot txt ROBOTSTXT_OBEY = False DEBUG: Forbidden by robots.txt:
# scrapy crawl mercadolivre -o data1.jsonl para rodar na pasta coleta/coleta
import scrapy


class MercadolivreSpider(scrapy.Spider):
    name = "mercadolivre"
    allowed_domains = ["lista.mercadolivre.com.br"]
    start_urls = ["https://lista.mercadolivre.com.br/tenis-corrida-masculino"]
    page_count = 1
    max_pages = 10

    def parse(self, response):
        
        products = response.css('div.ui-search-result__content')
        
        for product in products: #54 itens
            
            prices = product.css('span.andes-money-amount__fraction::text').getall()
            cents = product.css('span.andes-money-amount__cents::text').getall()            
            
            yield {
                 'brand': product.css('span.ui-search-item__brand-discoverability.ui-search-item__group__element::text').get(),
                 'name': product.css('h2.ui-search-item__title::text').get(),
                 'old_price_reais': prices[0] if len(prices) > 0 else None,
                 'old_price_centavos': cents[0] if len(cents) > 0 else None,
                 'new_price_reais': prices[1] if len(prices) > 1 else None,
                 'new_price_centavos': cents[1] if len(cents) > 1 else None,
                 'reviews_rating_number':product.css('span.ui-search-reviews__rating-number::text').get(),
                 'reviews_amount':product.css('span.ui-search-reviews__amount::text').get()
                 
             }
            
           
        if self.page_count < self.max_pages:
            next_page = response.css('li.andes-pagination__button.andes-pagination__button--next a::attr(href)').get()
            if next_page:
                self.page_count +=1
                yield scrapy.Request(url=next_page, callback=self.parse)    
                