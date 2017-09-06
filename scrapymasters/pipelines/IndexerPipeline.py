from scrapymasters.common.ConfigFiles import ConfigFiles
from scrapymasters.common.MongoUtils import MongoUtils
from string import punctuation


class IndexerPipeline(object):
    # ==fc== initiallize mongoclient
    def __init__(self):
        config = ConfigFiles.config()
        self.client = MongoUtils.create_client_from_config(config)
        self.db = self.client.scrape
        """
        ==fc== Initialize an ordered batch of write operations.

                Operations will be performed on the server serially, in the
                order provided. If an error occurs all remaining operations
                are aborted.

                Returns a :class:`~pymongo.bulk.BulkOperationBuilder` instance.

                See :ref:`ordered_bulk` for examples.

                .. versionadded:: 2.7
         """
        self.bulk = self.db.words.initialize_ordered_bulk_op()

    """
    ==fc== 
    save the data to mongodb
    While MongoWriterPipeline simply stores article data in the 'articles' collection, the IndexerPipeline creates an index
    (stored in 'words') by mapping the words occuring in the body of an article to the article's url via the following structure:
    {
        'word': 'someWord',
        'urls': ['http://www.articleContainingWord.com', 'http://www.anotherArticleContainingWord.com', ...]
    }
    """
    def process_item(self, article, spider):
        body = article['body']
        for word in body.split():
            word = word.strip(punctuation).lower()

            if len(word) != 0 and word.isalpha():
                url = article['url']
                word_query = { "word": word }
                url_to_insert = {"$addToSet": {"urls": url }}
                self.bulk.find(word_query).update(url_to_insert)
        return article

    # ==fc== execute index and then Disconnect from MongoDB.
    def close_spider(self, spider):
        result = self.bulk.execute()
        print("Index write results:")
        print(result)
        self.client.close()
