from api import Api
import random
from BookFetcher import BookFetcher

api = Api("admin", "admin1")

bookFetcher = BookFetcher()

amountSent = bookFetcher.run(api.addAuthor, api.sendAuthors, 0)
print("Amount sent: {}".format(amountSent))

#TODO zamienic a-z na /w+