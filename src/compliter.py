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
        :return:возвращает строку для вставки. Вид <label> "descr1" "descr2" ...
        """
        for snip in self.snippets:
            if snip["label"] == event:
                return self.createStringBySnippet(snip)
        else:
            return ""

    def parsedSubstitution_evnt(self, event):
        """
        :param event:
            event.string строка вида <label> <arg1> <arg2>...<agrN>
            event.snippet сниппет из которого будем доставать.
        :return:возращает сниппет для вывода
        """
        result = ""
        args = event.string.split(" ")
        if event.snippet["label"] == args[0]:
            currentArgForAddition = 1
            for item in event.snippet["snippetText"]:
                if type(item) == str:
                    result += item
                else:
                    result += args[currentArgForAddition]
                    currentArgForAddition += 1
            return result
        else:
            return result

    def getSubstitutionList(self):
        l_ = []
        for snip in self.snippets:
            if snip["label"].startswith(self.fieldString):
                l_.append(snip)
        return l_

    def createStringBySnippet(self, snippet):
        resultString = snippet["label"] + " "
        for item in snippet["snippetText"]:
            if type(item) == dict:
                resultString += "#" + item["description"] + "#"
            resultString += " "
        return resultString


if __name__ == '__main__':
    a = AutoSub("snippets")
    l = a.fieldCange_evnt("kno")
    print(l)
    ans = a.substitution_evnt("knop")
    print(ans)