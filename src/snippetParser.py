#!/usr/bin/env python3
__author__ = 'muratov'

import json

class SnippetParser:
    def __init__(self, path):
        self.loadSnippetList(path)
        self.defaultPath = path

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


if __name__ == '__main__':
    sn = SnippetParser("snippets")
    print(sn.snippets)