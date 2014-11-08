#! /usr/bin/env python3

import json

separator = '#'
path = 'src/snippets'


def load_snippets():
    return json.load(open(path, "r"))


def save_snippets(snippets):
    json.dump(snippets, open(path, "w", encoding="UTF-8"),
              ensure_ascii=False)


def update_or_append_snippet(snippet):
    snippets = load_snippets()

    for s in snippets:
        if s['label'] == snippet['label']:
            s['description'] = snippet['description']
            s['text'] = snippet['text']
    else:
        snippets.append(snippet)

    save_snippets(snippets)


def delete_snippet(label):
    snippets = load_snippets()

    for index in range(len(snippets)):
        if snippets[index]["label"] == label:
            del snippets[index]
            break

    save_snippets(snippets)


def get_suggested_snippets(snippets, label_prefix):
    result = []

    for snippet in snippets:
        if snippet["label"].startswith(label_prefix):
            result.append(snippet)

    return result


def get_expanded_snippet_by_label(snippets, label):
    for snippet in snippets:
        if snippet["label"] == label:
            return get_expanded_snippet(snippet)
    else:
        return ""


def get_expanded_snippet(snippet):
    result = snippet["label"] + " "

    for item in snippet["snippetText"]:
        if type(item) == dict:
            result += separator + item["description"] + separator + " "

    return result.rstrip()


def convert_expanded_snippet_to_result(snippets, snippet):
    result = ""
    args = snippet.strip().split()

    for snippet in snippets:
        if snippet["label"] == args[0]:
            arg_pos = 1

            for item in snippet["snippetText"]:
                if type(item) == str:
                    result += item
                else:
                    if arg_pos >= len(args):
                        result += separator + item["description"] + separator
                    else:
                        result += args[arg_pos]

                    arg_pos += 1

    return result