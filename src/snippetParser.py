#!/usr/bin/env python3
__author__ = 'muratov'

import json

from src.Exeptions import ParseExeption


class SnippetParser:
    def __init__(self, path):
        self.loadSnippetList(path)
        self.defaultPath = path
        for obj in self.snippets:
            self.checkCorrect(obj)

    def loadSnippetList(self, path):
        self.snippets = json.load(open(path, "r"))

    def saveSnippetList(self, path=""):
        if path == "":
            self.defaultPath = path
        json.dump(self.snippets, open(path, "w", encoding="UTF-8"),
                  ensure_ascii=False)

    def addSnippet(self, obj):
        if not obj in self.snippets:
            self.snippets.append(obj)
            self.saveSnippetList()

    def deleteSnippet(self, label):
        for numSnip in range(len(self.snippets)):
            if self.snippets[numSnip]["label"] == label:
                del self.snippets[numSnip]
                break
        else:
            return False
        self.saveSnippetList()
        return True

    def checkCorrect(self, obj):
        for item in self.snippets:
            if type(item["label"]) == str:
                if type(item["description"]) == str:
                    if type(item["snippetText"]) == list:
                        for text_item in item["snippetText"]:
                            if type(text_item) == str:
                                continue
                            elif type(text_item) == dict:
                                if type(text_item["type"]) == str and \
                                                        type(text_item["description"]) == str:
                                    continue
                                else:
                                    raise ParseExeption()
                            else:
                                raise ParseExeption()
                    else:
                        raise ParseExeption()
                else:
                    raise ParseExeption()
            else:
                raise ParseExeption()


if __name__ == '__main__':
    sn = SnippetParser("snippets")
    print(sn.snippets)