#! /usr/bin/env python3
__author__ = 'muratov'

from src.snippetParser import SnippetParser


class SnippetsEngine:
    def __init__(self, snippets_path):
        self.snippets = SnippetParser(snippets_path).snippets

    def get_suggested_snippets(self, text):
        result = []

        for snippet in self.snippets:
            if snippet["label"].startswith(text):
                result.append(snippet)

        return result

    def get_expanded_label(self, label):
        for snippet in self.snippets:
            if snippet["label"] == label:
                return self.get_expanded_snippet(snippet)
        else:
            return ""

    def get_expanded_snippet(self, snippet):
        result = snippet["label"] + " "

        for item in snippet["snippetText"]:
            if type(item) == dict:
                result += "#" + item["description"] + "# "

        return result.rstrip()

    def convert_snippet_to_result(self, snippet):
        result = ""
        args = snippet.strip().split(" ")

        for snippet in self.snippets:
            if snippet["label"] == args[0]:
                arg_pos = 1

                for item in snippet["snippetText"]:
                    if type(item) == str:
                        result += item
                    else:
                        if arg_pos >= len(args):
                            result += "#" + item["description"] + "#"
                        else:
                            result += args[arg_pos]

                        arg_pos += 1

        return result


if __name__ == '__main__':
    engine = SnippetsEngine("snippets")

    print(engine.get_suggested_snippets("kno"))

    print(engine.get_expanded_label("knop"))

    print(engine.convert_snippet_to_result("knop Муратов "))

    print(engine.convert_snippet_to_result("knop Муратов 01.01.0001 "))