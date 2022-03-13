import nltk.data
import re
import os
import sys


def generate_ngram_dict(n: int, text: str) -> dict:
    dictionary = dict()
    for i in range(0, len(text) - n + 1, 1):
        ngram = ''
        for j in range(i, i + n):
            ngram += text[j]
        if ngram != '':
            if not dictionary.get(ngram):
                dictionary[ngram] = 1
            else:
                dictionary[ngram] += 1
    return dictionary


def spacing(message: str):
    print("")
    s = ""
    for _ in range(0, 50):
        s += "="
    print(s)
    print(message)
    print(s)
    print("")


def count_words(array: []):
    print(f"Words in text: {len(array)}")


def count_words_appear(array: []):
    words_dict = dict()
    for word in array:
        words_dict[word] = array.count(word)

    for key, value in words_dict.items():
        print(f"{key} appears {value} time(s)")


def generate_large_string(array: []) -> str:
    return "".join(array)


def clear_sentence_symbols(sentence: str) -> str:
    sentence = re.sub(r'[^\w\s]', '', sentence)
    return sentence


def text_to_array(text: str) -> []:
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')

    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    words = []
    array = tokenizer.tokenize(text)
    for element in array:
        element = clear_sentence_symbols(element)
        sentence = nltk.word_tokenize(element)
        for word in sentence:
            words.append(word)
    return words


def input_values() -> (int, int):
    try:
        n = int(input('Enter N: '))
    except ValueError:
        n = 10
    try:
        k = int(input('Enter K: '))
    except ValueError:
        k = 4
    return n, k


def find_top_k(dictionary: dict, k: int):
    sorted_dictionary = dict()
    sorted_values = sorted(dictionary, key=dictionary.get)
    count = 0
    for value in sorted_values:
        sorted_dictionary[value] = dictionary[value]
        count += 1
    if count < k:
        for key, value in sorted_dictionary.items():
            print(f"{key} appears {value} time(s)")
    else:
        reversed_dictionary = dict(reversed(list(sorted_dictionary.items())))
        kk = 0
        for key, value in reversed_dictionary.items():
            if kk >= k:
                break
            print(f"{key} appears {value} time(s)")
            kk += 1


def is_empty(path: str) -> bool:
    return True if os.path.getsize(path) == 0 else False


def read_file(path: str) -> str:
    if is_empty(path):
        print("File is empty.")
        sys.exit()
    else:
        with open(path) as open_file:
            s = open_file.read()
    return s


def main():
    data = read_file('input.txt')
    nk = input_values()
    words = text_to_array(data)
    spacing("Words count")
    count_words(words)
    spacing("Words appear")
    count_words_appear(words)
    spacing("Ngrams stats")
    s = generate_large_string(words)
    d = generate_ngram_dict(nk[0], s)
    find_top_k(d, nk[1])


if __name__ == "__main__":
    main()
