#! /usr/bin/env python3


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
            result += "#" + item["description"] + "# "

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
                        result += "#" + item["description"] + "#"
                    else:
                        result += args[arg_pos]

                    arg_pos += 1

    return result