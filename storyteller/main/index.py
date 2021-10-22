"""
index a pre-downloaded corpus into elasticsearch.
"""
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus_name", type=str,
                        default="gk")
    args = parser.parse_args()
    corpus_name: str = args.corpus_name

    if corpus_name == "gk":
        pass
    elif corpus_name == "sc":
        pass
    else:
        raise ValueError(f"Invalid corpus_name: {corpus_name}")


if __name__ == '__main__':
    main()
