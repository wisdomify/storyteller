
from storyteller.readers import GKReader, SCReader


def main():
    for doc in GKReader():
        print(doc.to_dict())
        break
    for doc in SCReader():
        print(doc.to_dict())
        break


if __name__ == '__main__':
    main()
