import requests
from api import Api
import random
from BookFetcher import BookFetcher

api = Api("admin", "admin1")

bookFetcher = BookFetcher()

i = 1
bookFetcher.loadPage(i)
while bookFetcher.hasTags():
    while bookFetcher.hasNext():
        author = bookFetcher.getNext()
        if author is not None:
             api.addAuthor(author.firstName, author.lastName, author.title, random.randrange(40, 290))
    i += 1
    api.sendAuthors()
    bookFetcher.loadPage(i)


print(api.get("books/size"))

#TODO simplfy use of the book fetcher