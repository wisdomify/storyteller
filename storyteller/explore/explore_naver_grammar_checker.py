import requests
import json


def main():
    text = "나느 게발자가 돼고 싶어요"
    base_url = 'https://m.search.naver.com/p/csearch/ocontent/spellchecker.nhn'
    payload = {
        '_callback': 'window.__jindo2_callback._spellingCheck_0',
        'q': text
    }
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'referer': 'https://search.naver.com/',
    }
    r = requests.get(base_url, params=payload, headers=headers)
    data = json.loads(r.text[42:-2])
    # corrected
    original = text
    corrected = data['message']['result']['notag_html']
    print(original, "->", corrected)


if __name__ == '__main__':
    main()
