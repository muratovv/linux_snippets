#!/usr/bin/
__author__ = 'muratov'

from src.snippetParser import SnippetParser


class AutoSub:
    def __init__(self, snippet_path):
        self.parser = SnippetParser(snippet_path)
        self.snippets = self.parser.snippets
        self.fieldString = ""

    def fieldCange_evnt(self, event):
        """
        Вызывается при изменении поля ввода
        :param event: строка пользователя
        :return: вернет список подходящих шаблонов.
        """
        self.fieldString = event
        return self.getSubstitutionList()

    def substitution_evnt(self, event):
        """
        Вызывается при нажатии на поле списка
        :param event: метка сниппета
        :return:возвращает строку для вставки.
        """
        for snip in self.snippets:
            if snip["label"] == event:
                return self.createStringBySnippet(snip)
        else:
            return ""

    def getSubstitutionList(self):
        l = []
        for snip in self.snippets:
            if snip["label"].startswith(self.fieldString):
                l.append(snip)
        return l

    def createStringBySnippet(self, snippet):
        resultString = ""
        for item in snippet["snippetText"]:
            if type(item) == str:
                resultString += item
            else:
                resultString += "#" + item["description"] + "#"
            resultString += " "
        return resultString


if __name__ == '__main__':
    a = AutoSub("snippets")
    l = a.fieldCange_evnt("kno")
    print(l)
    ans = a.substitution_evnt("knop")
    print(ans)