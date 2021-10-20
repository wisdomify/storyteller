"""
This does not work on M1, sadly.
"""

from koeda import EDA


def main():

    eda = EDA(
        morpheme_analyzer="Okt", alpha_sr=0.3, alpha_ri=0.3, alpha_rs=0.3, prob_rd=0.3
    )

    text = "아버지가 방에 들어가신다"

    result = eda(text)
    print(result)
    # 아버지가 정실에 들어가신다

    result = eda(text, p=(0.9, 0.9, 0.9, 0.9), repetition=2)
    print(result)
    # ['아버지가 객실 아빠 안방 방에 정실 들어가신다', '아버지가 탈의실 방 휴게실 에 안방 탈의실 들어가신다']


if __name__ == '__main__':
    main()