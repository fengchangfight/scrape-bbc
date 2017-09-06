from scrapymasters.common.ConfigFiles import ConfigFiles
from scrapymasters.common.MongoUtils import MongoUtils
from string import punctuation




config = {
            'url': 'localhost:27017',
            'username': "",
            'password': "",
            'dbname': "scrape",
            'scrapeUrl': "http://www.bbc.com/"
        }


client = MongoUtils.create_client_from_config(config)
db = client.scrape
bulk = db.words.initialize_ordered_bulk_op()
word = "sometimes"
word_query = { "word": word }
url = "http://www.bbc.com/news/world-latin-america-41168117"
url_to_insert = {"$addToSet": {"urls": url }}\

print(db.words.find(word_query).count())
print("=======")

bulk.find(word_query).update(url_to_insert)

result = bulk.execute()
print("Index write results:")
print(result)
client.close()