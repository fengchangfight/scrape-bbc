from string import punctuation


class Indexer:
    def __init__(self):
        pass

    # ==fc== build index from splitting words in article body, it returns the index dict
    @staticmethod
    def map_bodywords_to_articles(articles):
        article_word_index = {}

        for article in articles:
            body = article['body']
            for word in body.split():
                word = word.strip(punctuation).lower()
                if len(word) != 0:
                    url = article['url']
                    # Need to clean word (remove punctuation etc)
                    if word in article_word_index:
                        article_word_index[word].append(url)
                    else:
                        article_word_index[word] = [url]

        return article_word_index
