import requests
from bs4 import BeautifulSoup as Soup
import re
import random


class Author:
    name = ""
    title = ""
    units = ""

    def __init__(self, name, title, units):
        self.name = name
        self.title = title
        self.units = units


class BookFetcher:
    __siteURL = "https://thegreatestbooks.org/{}"
    __pageURL = "?page={}"
    __liTags = []
    __bs = None
    __current_tag = -1
    __current_page = 1
    __informationRegex = '\<h4\> +\d+\. +\<a href\=\"[a-z0-9\/]+"\>([a-zA-Z0-9 \']+) *\<\/a\> by \<a href\=\"[a-z0-9\/]+\"\>([a-zA-Z.\- ]+)\<\/a\>\<\/h4\>'
    __nameRegex = "([A-Za-z.\- ]+)"

    def __getPage(self, page_number):
        return self.__siteURL.format(self.__pageURL.format(page_number))

    def loadPage(self, page_number):
        pageHTML = self.__getPageHTML(page_number)
        bs = Soup(pageHTML.content, "html.parser")
        self.__liTags = bs.find_all('li', class_="item pb-3 pt-3 border-bottom")
        self.__current_page = page_number
        self.__current_tag = -1

    def hasTags(self):
        return len(self.__liTags) > 0

    def __getPageHTML(self, page_number):
        return requests.get(self.__getPage(page_number))

    def hasNext(self):
        currentTag = self.__current_tag
        totalTags = len(self.__liTags)
        return currentTag < totalTags - 1

    def run(self, onNewAuthor, onBatch, limit):
        i = 1
        count = 0
        self.loadPage(i)
        while self.hasTags() and count <= limit:
            while self.hasNext():
                author = self.getNext()
                if author is not None:
                    onNewAuthor(author.name, author.title, random.randrange(40, 290))
                    if limit > 0:
                        count += 1
                    else:
                        count -= 1
            i += 1
            onBatch()
            self.loadPage(i)
        if count <= 0:
            return count * -1
        else:
            return count

    def getNext(self):
        try:
            self.__current_tag += 1
            tag = self.__liTags[self.__current_tag]
            header = tag.find("h4")
            header = self.__removeNewLines(str(header))
            pattern = re.compile(self.__informationRegex)
            matcher = pattern.match(header)
            if matcher is None:
                return None
            title = matcher.group(1)
            name = self.__parseAuthorName(matcher.group(2))
            return Author(name, title, 0)
        except TypeError:
            return None

    def __parseAuthorName(self, name):
        pattern = re.compile(self.__nameRegex)
        match = pattern.match(name)
        if match is not None:
            return match.group(1)
        return None

    def __removeNewLines(self, string):
        return string.replace("\n", "")
