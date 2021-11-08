from soynlp.normalizer import emoticon_normalize, only_text, repeat_normalize


def explore_soynlp():
    emoticon_normalised = emoticon_normalize('ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ 와하하하하하하하하하핰 그그그그게 아니 ㅎㅎㅎㅎㅎ 앜ㅋㅋㅋㅋ', num_repeats=1)
    """
        >>> 'ㅋ 와하핰 그게 아니 ㅎ 아ㅋ'
    """
    emoticon_normalised = emoticon_normalize(only_text('아이고 ㅋ [WISDOM]. ㅋㅋㅋㅋㅋㅋ 통했ㅋㅋ 그르니까'), num_repeats=1)
    print(emoticon_normalised)


if __name__ == '__main__':
    explore_soynlp()
