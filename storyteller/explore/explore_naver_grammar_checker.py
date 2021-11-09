import requests
import json

from storyteller.utils.grammar_checker import check_grammar


def main():
    text = "나느 게발자가 돼고 싶어요"
    original = text
    corrected = check_grammar(text)
    print(original, "->", corrected)


if __name__ == '__main__':
    main()
