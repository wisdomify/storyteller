import os
import json
from storyteller.paths import MR_DIR, DS_DIR


def main():
    json_path = os.path.join(DS_DIR, "ds.json")

    file = json.load(open(json_path, 'r', encoding='utf-8-sig'))

    data = file[0]['documents'][0]


"""

file[0]['documents'][0]
{'abstractive': ['이명박 대통령은 어제 30대 그룹 총수를 모아놓고 시대적 요구는 역시 총수가 앞장서야 한다고 발언하며 '
                 '기부문화 확산을 은근히 강조했으나 대통령의 강요나 포퓰리즘에 의한 압박보다는 자발적 문화로 구축해야 효과가 '
                 '더 큰 법으로 방안 마련을 맡기고 시간을 줘야 할 것으로 보인다.'],
 'annotator_id': 3924,
 'category': '오피니언',
 'char_count': '1153',
 'document_quality_scores': {'accurate': 3,
                             'informative': 3,
                             'readable': 4,
                             'trustworthy': 3},
 'extractive': [0, 6, 7],
 'id': '100062073',
 'media_name': '매일경제',
 'media_sub_type': '경제지',
 'media_type': 'online',
 'publish_date': '2011-09-01 00:03:01',
 'size': 'medium',
 'text': [[{'highlight_indices': '9,11;37,39;53,55;91,93;104,106',
            'index': 0,
            'sentence': '이명박 대통령이 어제 30대 그룹 총수를 모아놓고 "시대적 요구는 역시 총수가 앞장서야 한다. '
                        '이미 상당한 변화의 조짐이 있다는 것을 고맙게 생각한다. 총수들께서 직접 관심을 가져주시면 빨리 '
                        '전파돼 긍정적인 평가를 받을 수 있다고 본다"고 말했다.'},
           {'highlight_indices': '0,2;6,8;14,16;59,61;104,106',
            'index': 1,
            'sentence': '언뜻 보아 무슨 말인지 불분명하나 이 대통령이 지난 8ㆍ15 연설 후 정몽준 의원, 정몽구 '
                        "현대차 회장이 각각 2000억원과 5000억원을 기부한 사실과 '공생발전'이란 화두를 연결하면 "
                        '금방 짐작이 간다.'},
           {'highlight_indices': '0,2;11,12;18,21',
            'index': 2,
            'sentence': '다른 그룹 총수들도 좀 나서라고 은근히 떠민 것이다.'},
           {'highlight_indices': '0,1',
            'index': 3,
            'sentence': '이 대통령은 기부에 대한 후속 선언이 나오지 않은 탓인지 총수들의 사회공헌 방안에 불만을 '
                        '표시했다는 후문이다.'}],
          [{'highlight_indices': '55,56',
            'index': 4,
            'sentence': '최근 미국 프랑스 벨기에 등에서 부유세가 거론되고 독일조차 2년간 한시적으로 5%의 자산세를 '
                        '거둬 약 155조원을 마련하자는 논의가 있었다.'},
           {'highlight_indices': '0,2',
            'index': 5,
            'sentence': '이런 흐름에 한국만 동떨어져 있기는 어려운 게 글로벌 시대의 특징이다.'},
           {'highlight_indices': '21,23',
            'index': 6,
            'sentence': '항간에는 이번 회동 후 삼성을 비롯해 몇몇 그룹이 노블레스 오블리주 방안을 준비하고 있다는 말이 '
                        '나도는데 대통령의 강요나 포퓰리즘에 의한 압박보다 자발적 문화로 만들어가야 효과가 큰 '
                        '법이다.'}],
          [{'highlight_indices': '0,2;36,38',
            'index': 7,
            'sentence': '그런 면에서 재계에 적절한 방안 마련을 맡기고 정치권이나 여론은 너무 압박하지 말고 시간을 줘야 '
                        '한다.'},
           {'highlight_indices': '',
            'index': 8,
            'sentence': "국가채무 문제로 글로벌 경기 침체 우려가 큰 상황에서 기업들은 '생존'에 큰 부담을 느끼고 있기 "
                        '때문이다.'}],
          [{'highlight_indices': '',
            'index': 9,
            'sentence': "이날 전경련에 따르면 30대 그룹은 올해 고용 12만4000명, 투자 114조원 등 '선물'을 "
                        '준비했다.'},
           {'highlight_indices': '35,36;47,49',
            'index': 10,
            'sentence': '세계적인 더블딥이 우려되는 상황에서 공격경영이 어렵겠지만 연초 한 번 발표한 내용을 약간 수정해 '
                        '내놓은 전경련의 행태는 답답하다.'},
           {'highlight_indices': '13,14;15,16',
            'index': 11,
            'sentence': '설립 50주년이 됐으면 좀 더 창의적이고 유연하게 바뀔 때도 됐다.'}],
          [{'highlight_indices': '23,25;60,61',
            'index': 12,
            'sentence': '허창수 전경련 회장은 "대기업ㆍ중소기업이 서로 공생하고 발전할 수 있도록 노력하겠다. 기업이 '
                        '사회적 책임을 다하겠다"는 원론적인 발언에 그쳐 전경련 특유의 무미건조함을 드러냈다.'},
           {'highlight_indices': '78,80',
            'index': 13,
            'sentence': '한편 이건희 삼성전자 회장은 "중소기업계 협력을 강화해 국제적으로 경쟁력 있는 기업 생태계를 '
                        '만들어 나가겠다"고 발언했고, 정몽구 회장은 "이제 1차 협력업체는 경쟁력을 확보한 만큼 '
                        '2ㆍ3차 협력업체 지원에 힘쓰겠다"고 했는데 의미 있는 내용이라고 본다.'},
           {'highlight_indices': '0,3;19,21',
            'index': 14,
            'sentence': '그대로 실천하면 동반성장 생태계는 한층 강화될 것이다.'}]],
 'title': '[사설] 기부문화 확산 은근히 강조한 李대통령'}
"""


if __name__ == '__main__':
    main()
