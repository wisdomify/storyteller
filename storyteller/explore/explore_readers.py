
from storyteller.readers import GKReader, SCReader


def main():
    for sample in GKReader():
        print(sample)
        break
    for sample in SCReader():
        print(sample)
        break


if __name__ == '__main__':
    main()
