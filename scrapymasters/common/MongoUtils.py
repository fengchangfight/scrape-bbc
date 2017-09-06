from pymongo import MongoClient


class MongoUtils:
    def __init__(self):
        pass

    # ==fc== create mongo client from config file
    @staticmethod
    def create_client_from_config(config):
        if config["username"] == "" and config["password"] == "":
            client = MongoClient("mongodb://" + config["url"] + "/" + config["dbname"])
            print("Using " + "mongodb://" + config["url"] + "/" + config["dbname"])
        else:
            client = MongoClient("mongodb://" + config["username"] + ":" + config["password"] + "@" + config["url"]
                             + "/" + config["dbname"])
        return client

    # ==fc== a kind of search article by url
    @staticmethod
    def find_article_by_url(db, url):
        cursor = db.articles.find({"url": url})

        result = []
        for item in cursor:
            result.append(item)

        return result

    #==fc== search logic : word->url->article
    @staticmethod
    def find_article_by_word(db, word):
        word_index = db.words.find({"word": word})

        result = []
        for item in word_index:
            for url in item['urls']:
                result.append(MongoUtils.find_article_by_url(db, url))
        return result

    #==fc== just find all articles
    @staticmethod
    def find_all_articles(db):
        return db.articles.find()

    # ==fc== just find all words from words table
    @staticmethod
    def find_all_words(db):
        return db.words.find()
