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
        :param event:строка введенная пользователем
        :return:возращает сниппет для вывода
        """
        result = ""
        args = event.split(" ")
        for snip in self.snippets:
            if snip["label"] == args[0]:
                currentArgForAddition = 1
                for item in snip["snippetText"]:
                    if type(item) == str:
                        result += item
                    else:
                        if currentArgForAddition > len(args):
                            result += "#" + item["description"] + "#"
                        else:
                            result += args[currentArgForAddition]
                        currentArgForAddition += 1
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
    str_user = "knop Муратов 01.01.0001"
    ans = a.parsedSubstitution_evnt(str_user)
    print(ans)