#!/usr/bin/env python3
__author__ = 'muratov'

import json

from src.Exeptions import ParseExeption, badUserSnippetExeption


class SnippetParser:
    def __init__(self, path):
        self.loadSnippetList(path)
        self.defaultPath = path


    def loadSnippetList(self, path):
        self.snippets = json.load(open(path, "r"))
        for obj in self.snippets:
            self.checkCorrect(obj)

    def saveSnippetList(self, path=""):
        if path == "":
            self.defaultPath = path
        json.dump(self.snippets, open(path, "w", encoding="UTF-8"),
                  ensure_ascii=False)

    def addSnippet(self, obj):
        if not obj in self.snippets:
            self.checkCorrect(obj)
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

    def getObjFromString(self, obj_string):
        """
        вернет объект сниппет
        :param obj_string:
            obj_string.label - label
            obj_string.text - row text
            obj_string.description - description
        :return:
        """
        obj = {"label": obj_string.label, "description": obj_string.description, "snippetText": []}
        if obj["label"] == "" or obj["snippetText"] == "":
            raise badUserSnippetExeption()
        currentTextPart = 0
        for part in obj_string.text.split("#"):
            if currentTextPart % 2 == 0:
                # text
                if part != "":
                    obj["snippetText"].append(part)
            else:
                if part != "":
                    obj["snippetText"].append(dict(description=part))
                else:
                    raise badUserSnippetExeption()
            currentTextPart += 1
        try:
            self.checkCorrect(obj)
        except ParseExeption:
            raise badUserSnippetExeption()
        return obj

    def checkCorrect(self, snippet):
        if type(snippet["label"]) == str and snippet["label"].find(" ") == -1:
            if type(snippet["description"]) == str:
                if type(snippet["snippetText"]) == list:
                    for text_item in snippet["snippetText"]:
                        if type(text_item) == str:
                            continue
                        elif type(text_item) == dict:
                            continue
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

    class A:
        pass
    a = A()
    a.label = "label1"
    a.description = "my description"
    a.text = "#arg1#Fuuuuu #arg2#! 0#arg3#"
    print(sn.getObjFromString(a))