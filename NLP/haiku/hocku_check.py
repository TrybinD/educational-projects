VOWELS = 'уеёыаоэяию'


def syllables_counter(word):
    '''Считает количество слогов в слове или словосочитание/предложение'''
    counter = 0
    for i in word.lower():
        if i in VOWELS:
            counter += 1
    return counter


def haiku_check_with_comments(haiku):
    '''Принимает хокку в виде списка из 3 сток и проверяет слоги.
    Если на вход подается не список из 3 строк он говорит об этом
    В функции есть встроенные комментарии'''
    if len(haiku) == 3:
        good = True
        for row, n in zip(haiku, [5, 7, 5]):
            if syllables_counter(row) != n:
                print("В строке '{}' {} слогов!".format(row, syllables_counter(row)))
                good = False
        if good:
            print("Правильное хокку")
        else:
            print("Хокку не канон!")
    else:
        print("Это не хокку")


def haiku_check(haiku):
    '''Выдает True если хокку каноничное или похоже на него.
    Без комментариев - служебная функция'''
    if len(haiku) == 3:
        if [syllables_counter(x) for x in haiku] == [5, 7, 5]:
            return True, True
        else:
            return True, False
    else:
        return False, False


if __name__ == '__main__':
    print("Введите ваще хокку")
    haiku = [input() for _ in range(3)]
    haiku_check_with_comments(haiku)

