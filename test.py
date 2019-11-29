from scrapy import Selector

sel = Selector(text="<p>112</p>")
content= sel.xpath('string(/*)').extract()
print(content)