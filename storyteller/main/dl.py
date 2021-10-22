"""
download a given data from GCP.
"""
import argparse
from storyteller.paths import GK_DIR, SC_DIR
from storyteller.gcp import GCP
import os
import json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus_name", type=str,
                        default="gk")
    args = parser.parse_args()
    corpus_name = args.corpus_name
    # a gcp object.
    gcp = GCP('wisdomify')
    # 일단 말뭉치만 다운로드를 진행함 - 꽤나 용량이 큰 데이터도 있으니, 주의할 것!
    if corpus_name == "gk":
        # general knowledge (일반 대화)
        gcp.download('story/elastic/일반상식', to=GK_DIR, unzip=True)
    elif corpus_name == "sc":
        # sentimental conversation (감성 대화)
        gcp.download('story/elastic/감성대화', to=GK_DIR, unzip=True)
    elif corpus_name == "ds":
        # document summary (문서 요약)
        pass
    else:
        raise ValueError(f"Invalid corpus name: {corpus_name}")


if __name__ == '__main__':
    main()
