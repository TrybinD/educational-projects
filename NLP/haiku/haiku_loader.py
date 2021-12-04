from hocku_check import haiku_check, haiku_check_with_comments


def haiku_loader(corpus):
    with open(corpus, encoding='utf-8') as file:
        haiku = file.read().split('***')
        for i in haiku:
            yield list(filter(None, i.split('\n')))



if __name__ == '__main__':
    c = 1
    for haiku in haiku_loader('haiku_corpus.txt'):
        if haiku_check(haiku)[0] and not haiku_check(haiku)[1]:
            print(c)
            print(haiku, sep='\n')
            haiku_check_with_comments(haiku)
            print()
            c += 1
