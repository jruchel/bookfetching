import requests
import re


class Api:
    __siteURL = "http://localhost:8080"

    __usersURL = "http://localhost:8080/users"
    __deliveryURL = "http://localhost:8080/books/bookDelivery"
    __loginURL = "http://localhost:8080/temp/login"
    __session = None
    __authorList = None
    __listSize = 0

    __bodyRegex = "b\'(.+)\'"

    def __init__(self, username, password):
        self.__session = requests.session()
        self.login(username, password)

    def __getBody(self, body):
        pattern = re.compile(self.__bodyRegex)
        matcher = pattern.match(body)
        return matcher.group(1)

    def __createAuthor(self, name, title, units):
        author = '{{"name":"{}","bibliography":[{{"title":"{}", "inStock":{}}}] }}'.format(name, title, units)
        return author

    def addAuthor(self, name, title, units):
        print("{}: {}, {}".format(name, title, units))
        if self.__authorList is None or len(self.__authorList) is 0:
            self.__authorList = "["
            self.__authorList += self.__createAuthor(name, title, units)
            self.__authorList += "]"
            self.__listSize += 1
            return self.__authorList
        self.__authorList = self.__authorList[0:len(self.__authorList) - 1]
        self.__authorList += ", {}]".format(self.__createAuthor(name, title, units))
        self.__listSize += 1
        return self.__authorList

    def getListSize(self):
        return self.__listSize

    def getAuthorList(self):
        return self.__authorList

    def login(self, username, password):
        user = self.__createUser(username, password)
        response = self.__session.post(self.__loginURL, data=user, headers={"Content-Type": "application/json"})
        return response.status_code

    def get(self, sub_page):
        response = self.__session.get(self.__getSubPage(sub_page))
        return self.__getBody(str(response.content))

    def post(self, sub_page, data, headers):
        return self.__session.post(self.__getSubPage(sub_page), data=data, headers=headers).status_code

    def post(self, sub_page, data):
        return self.__session.post(
            self.__getSubPage(sub_page),
            data=data,
            headers={"Content-Type": "application/json"}).status_code

    def getLibrarySize(self):
        return self.get("books/size")

    def getBookCount(self):
        return self.get("books/count")

    def __getSubPage(self, path):
        return (self.__siteURL + "/{}").format(path)

    def __createUser(self, username, password):
        return '{{"username":"{}", "password":"{}", "passwordConfirm":"{}"}}'.format(username, password, password)

    def clearAuthors(self):
        self.__authorList = None

    def sendAuthors(self):
        response = self.__session.post(self.__deliveryURL, data=self.__authorList,
                                       headers={"Content-Type": "application/json"})
        print("Sent {} authors".format(self.__countAuthors()))
        self.clearAuthors()
        return response.status_code

    def __countAuthors(self):
        return self.__authorList.count("name")