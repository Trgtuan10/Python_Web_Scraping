# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BookscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Strip all whitespace surrounding the values
        field_names = adapter.field_names()
        for f in field_names:
            value = adapter.get(f)
            adapter[f] = value[0].strip()

        lower_cases = ['category', 'product_type']
        for l in lower_cases:
            adapter[l] = adapter[l].lower()
        
        # convert price to float
        price_keys = ['price_excl_tax', 'price_incl_tax', 'tax', 'price']
        for p in price_keys:
            price_value = adapter.get(p, "").replace('£', '').strip()
            if price_value:  # Check if the price value is not empty
                adapter[p] = float(price_value)
            else:
                adapter[p] = 0.0
        
        # convert number_of_reviews to int
        adapter['number_of_reviews'] = int(adapter['number_of_reviews'].split()[0])

        # availability
        avai = adapter.get('availability')
        split_avai = avai.split('(')
        if len(split_avai) < 2:
            adapter['availability'] = 0
        else:
            adapter['availability'] = int(split_avai[1].split(" ")[0])

        # stars
        stars = adapter['stars'].split(" ")[1]
        if stars == "Zero":
            adapter['stars'] = 0
        elif stars == "One":
            adapter['stars'] = 1
        elif stars == "Two":
            adapter['stars'] = 2
        elif stars == "Three":
            adapter['stars'] = 3
        elif stars == "Four":
            adapter['stars'] = 4
        else:
            adapter['stars'] = 5

        return item
    

str = "gia la £51.77"
print(str.split())