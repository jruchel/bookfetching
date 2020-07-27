import requests
from api import Api
from bs4 import BeautifulSoup as Soup
import re


# loadPage(pageNr) loads the given page number, then downloads all li tags into an array and sets an index for it
# hasNext return true if there is still another li tag on the page
# getNext returns the author and book title of the next book
# if hasNext is false goes to the next page until there is an error

# getNext looks at the page

class Author:
    firstName = ""
    lastName = ""
    title = ""
    units = ""

    def __init__(self, firstName, lastName, title, units):
        self.firstName = firstName
        self.lastName = lastName
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
    __nameRegexArray = ["([A-Z. ]+)", "([A-Za-z-]+)"]
    __lastNameRegex = '([A-Za-z\-]+)'

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
            names = self.__parseAuthorName(matcher.group(2))
            firstName = names[0]
            lastName = ""
            if len(names) > 1:
               lastName = names[1]
            return Author(firstName, lastName, title, 0)
        except TypeError:
            return None

    def __parseAuthorName(self, name):
        for regex in self.__nameRegexArray:
            pattern = re.compile((regex + " {}".format(self.__lastNameRegex)))
            match = pattern.match(name)
            if match is not None:
                return [match.group(1), match.group(2)]
        for regex in self.__nameRegexArray:
            pattern = re.compile(regex)
            match = pattern.fullmatch(name)
            if match is not None:
                return [match.group(1)]
        return None

    def __removeNewLines(self, string):
        return string.replace("\n", "")
