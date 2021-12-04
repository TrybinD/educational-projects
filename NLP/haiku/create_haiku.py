from _collections import defaultdict
import random
from hocku_check import haiku_check, haiku_check_with_comments, syllables_counter
from haiku_loader import haiku_loader


def map_word_to_word(corpus):
    '''Загрузить список слов и связать слово с последующим словом'''
    limit = len(corpus) - 1
    dict1_to_1 = defaultdict(list)
    for index, word in enumerate(corpus):
        if index < limit:
            suffix = corpus[index+1]
            dict1_to_1[word].append(suffix)
    return dict1_to_1


def map_2_words_to_word(corpus):
    '''Загрузить список слов и создать словарь
     для увязки 2 слов с 3'''
    limit = len(corpus) - 2
    dict2_to_1 = defaultdict(list)
    for index, word in enumerate(corpus):
        if index < limit:
            key = ' '.join([word, corpus[index+1]])
            suffix = corpus[index+2]
            dict2_to_1[key].append(suffix)
    return dict2_to_1


def random_word(corpus):
    '''Вернуть случайное слово и его количество слогов'''
    word = random.choice(corpus)
    num_syls = syllables_counter(word)
    if num_syls > 4:
        random_word(corpus)
    else:
        return word, num_syls


def word_after_single(prefix, suffix_map_1, curr_syls, target_syls):
    '''Вернуть все приемлемые слова в корпусе,
     которые следуют за одним словом'''
    accepted_words = []
    suffixes = suffix_map_1.get(prefix)
    if suffixes:
        for candidate in suffixes:
            num_syls = syllables_counter(candidate)
            if curr_syls + num_syls <= target_syls:
                accepted_words.append(candidate)
    return accepted_words


def word_after_double(prefix, suffix_map_2, curr_syls, target_syls):
    '''Вернуть все приемлемые слова в корпусе,
     которые следуют за парой'''
    accepted_words = []
    suffixes = suffix_map_2.get(prefix)
    if suffixes:
        for candidate in suffixes:
            num_syls = syllables_counter(candidate)
            if curr_syls + num_syls <= target_syls:
                accepted_words.append(candidate)
    return accepted_words


def haiku_line(suffix_map_1, suffix_map_2, corpus,
               end_prev_line, target_syls, order=2):
    '''Собрать хокку из тренеровочного корпуса и вернуть ее.
    По умолчанию марковская цепь порядка 2, но можно изменить
    на порядок 1'''
    line = '2/3'
    line_syls = 0
    curr_line =[]
    if len(end_prev_line) == 0: #Создаем первую строку
        line = '1'
        word, num_syls = random_word(corpus)
        curr_line.append(word)
        line_syls += num_syls
        word_choices = word_after_single(word, suffix_map_1,
                                         line_syls, target_syls)
        while len(word_choices) == 0:
            prefix = random.choice(corpus)
            word_choices = word_after_single(prefix, suffix_map_1,
                                             line_syls, target_syls)


        word = random.choice(word_choices)
        num_syls = syllables_counter(word)
        line_syls += num_syls
        curr_line.append(word)
        if line_syls == target_syls:
            end_prev_line.extend(curr_line[-2:])
            return curr_line, end_prev_line

    else: # Вторая и третья строки
        curr_line.extend(end_prev_line)

    while True:
        if order == 1:
            prefix = curr_line[-1]
            word_choices = word_after_single(prefix, suffix_map_1,
                                             line_syls, target_syls)
            while len(word_choices) == 0:
                prefix = random.choice(corpus)
                word_choices = word_after_single(prefix, suffix_map_1,
                                                 line_syls, target_syls)
        else:
            prefix = ' '.join(curr_line[-2:])
            word_choices = word_after_double(prefix, suffix_map_2,
                                             line_syls, target_syls)
            while len(word_choices) == 0:
                index = random.randint(0, len(corpus) - 2)
                prefix = ' '.join(corpus[index:index + 2])
                word_choices = word_after_double(prefix, suffix_map_2,
                                  line_syls, target_syls)

        word = random.choice(word_choices)
        num_syls = syllables_counter(word)

        if line_syls + num_syls > target_syls:
            continue
        elif line_syls + num_syls < target_syls:
            curr_line.append(word)
            line_syls += num_syls
        elif line_syls + num_syls == target_syls:
            curr_line.append(word)
            break

    end_prev_line = []
    end_prev_line.extend(curr_line[-2:])

    if line == '1':
        final_line = curr_line[:]
    else:
        final_line = curr_line[2:]

    return final_line, end_prev_line


def create_corpus_list(corpus):
    corpus_list = []
    for h in haiku_loader(corpus):
        h = [line.lower().split() for line in h]
        h = [word for line in h for word in line]
        for word in h:
            for letter in word:
                if letter in '.,?;:!':
                    word = word[:-1]
            corpus_list.append(word)
    return corpus_list


if __name__ == '__main__':
    corpus = create_corpus_list('haiku_corpus.txt')

    suffix_map_1 = map_word_to_word(corpus)
    suffix_map_2 = map_2_words_to_word(corpus)

    haiku = []
    line1, end_prev_line1 = haiku_line(suffix_map_1, suffix_map_2,
                                       corpus, [], 5, order=2)
    haiku.append(line1)
    line2, end_prev_line2 = haiku_line(suffix_map_1, suffix_map_2,
                                       corpus, end_prev_line1, 7, order=2)
    haiku.append(line2)
    line3, end_prev_line3 = haiku_line(suffix_map_1, suffix_map_2,
                                       corpus, end_prev_line2, 5, order=2)
    haiku.append(line3)

    haiku_final = []
    for line in haiku:
        line = ' '.join(line)
        haiku_final.append(line)
    print(*haiku_final, sep='\n')
    #haiku_check_with_comments(haiku_final)