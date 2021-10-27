from more_itertools import chunked


def main():
    for batch in chunked(range(1000), 28):
        # https://more-itertools.readthedocs.io/en/stable/api.html#more_itertools.chunked
        # chunked can generate batches from a generator
        print(len(batch))


if __name__ == '__main__':
    main()
