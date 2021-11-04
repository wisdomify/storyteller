import os
import json
from storyteller.paths import MR_DIR, DS_DIR, SFC_DIR, KESS_DIR, KJ_DIR, KCSS_DIR, SFKE_DIR, KSNS_DIR


def main():
    json_path = os.path.join(KSNS_DIR, "ksns.json")

    file = json.load(open(json_path, 'r', encoding='utf-8-sig'))

    data = file[0]['data'][0]


"""
{'body': [{'date': '2020-10-07',
           'participantID': 'P01',
           'time': '13:18:00',
           'turnID': 'T1',
           'utterance': '여러 명 같이 하나보네?',
           'utteranceID': 'U1'},
          {'date': '2020-10-07',
           'participantID': 'P01',
           'time': '13:18:00',
           'turnID': 'T1',
           'utterance': '#@이모티콘#',
           'utteranceID': 'U2'},
          {'date': '2020-10-07',
           'participantID': 'P02',
           'time': '13:19:00',
           'turnID': 'T2',
           'utterance': '응 한 10명?',
           'utteranceID': 'U3'},
          {'date': '2020-10-07',
           'participantID': 'P02',
           'time': '13:19:00',
           'turnID': 'T2',
           'utterance': '프로그램 다운이 안 됐대',
           'utteranceID': 'U4'},
          {'date': '2020-10-07',
           'participantID': 'P01',
           'time': '13:19:00',
           'turnID': 'T3',
           'utterance': '아',
           'utteranceID': 'U5'},
          {'date': '2020-10-07',
           'participantID': 'P01',
           'time': '13:19:00',
           'turnID': 'T3',
           'utterance': '강제로 쉬는 시간',
           'utteranceID': 'U6'},
          {'date': '2020-10-07',
           'participantID': 'P01',
           'time': '13:20:00',
           'turnID': 'T3',
           'utterance': '평일엥 일하겠네 우리 #@이름#',
           'utteranceID': 'U7'},
          {'date': '2020-10-07',
           'participantID': 'P01',
           'time': '13:20:00',
           'turnID': 'T3',
           'utterance': '평일엔...',
           'utteranceID': 'U8'},
          {'date': '2020-10-07',
           'participantID': 'P02',
           'time': '14:15:00',
           'turnID': 'T4',
           'utterance': '다음 주부터는',
           'utteranceID': 'U9'},
          {'date': '2020-10-07',
           'participantID': 'P02',
           'time': '14:15:00',
           'turnID': 'T4',
           'utterance': '바쁘겠다',
           'utteranceID': 'U10'}],
 'header': {'dialogueInfo': {'dialogueID': 'b389d045-aa23-5e1e-af64-7406b1ad921c',
                             'numberOfParticipants': 2,
                             'numberOfTurns': 4,
                             'numberOfUtterances': 10,
                             'topic': '일과 직업',
                             'type': '일상 대화'},
            'participantsInfo': [{'age': '20대',
                                  'gender': '여성',
                                  'participantID': 'P01',
                                  'residentialProvince': '광주광역시'},
                                 {'age': '20대',
                                  'gender': '여성',
                                  'participantID': 'P02',
                                  'residentialProvince': '서울특별시'}]}}
"""

if __name__ == '__main__':
    main()
