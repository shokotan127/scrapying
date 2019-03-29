import scrapy
from final.items import Article
class YhspiderSpider(scrapy.Spider):
    name = 'yhspider'
    allowed_domains = ['news.yahoo.co.jp','headlines.yahoo.co.jp']
    start_urls = ['https://news.yahoo.co.jp']

    def parse(self, response):
        """
        トップページから個別記事ページへのリンク文字列を抜き出して1つずつ順番に処理する
        """

        print('----------------parse------------------')
        urls = response.css("#contentsWrap section.topics div ul li a::attr(href)").extract()
        print(urls)
        for url in urls:
            if url!="https://news.yahoo.co.jp/topics":
                if url!="https://news.yahoo.co.jp/list/":
                    if url!= None:
                        
                        print(url)
                        yield scrapy.Request(url, callback=self.articles)


    def articles(self, response):
        """
        簡略記事から記事詳細ページへのリンクの文字列を抜き出してリクエスト
        """

        detail = response.css("div#main div.mainBox article.tpcDetail section.tpcNews div.tpcNews_body p.tpcNews_detailLink a::attr(href)").extract()
        if detail != None and detail != []:
            
            print(detail[0])
            yield scrapy.Request(detail[0], callback=self.parse_articles)


    def parse_articles(self, response):
        """
        記事詳細ページからタイトルと本文を抜きだしてItemsに格納する
        """
        print('ページ格納')
        item = Article()    # items.pyで定義したArticleクラスのオブジェクトを作成
        title = response.css('#ym_newsarticle > div.hd > h1::text').extract_first()
        
        item['title'] = title
        body = response.css('#ym_newsarticle > div.articleMain > div.paragraph > p::text').extract()
        body =  ','.join(body)
        #body = response.css('p::text').extract()
        #body = response.css('div#main div.mainBox div.content-body div.article div#ym_newsarticle div.articleMain div.paragraph p::text').extract()
        item['body'] = body
        yield item
