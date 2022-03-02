import nltk.data
import re


def count_words(array: []):
    for word in array:
        print(f'"{word}" appears {array.count(word)} time(s)')


def generate_large_string(array: []):
    return "".join(array)


def clear_sentence_symbols(sentence: str):
    sentence = re.sub(r'[^\w\s]', '', sentence)
    return sentence


def text_to_array(text: str, array: []):
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    arr = tokenizer.tokenize(text)
    for el in arr:
        el = clear_sentence_symbols(el)
        a = nltk.word_tokenize(el)
        for word in a:
            array.append(word)


def input_values():
    try:
        n = int(input('Enter N: '))
    except ValueError:
        n = 10
    try:
        k = int(input('Enter K: '))
    except ValueError:
        k = 4
    return n, k


fp = open('input.txt')
data = fp.read()
words = []
text_to_array(data, words)
print(f"Words in text: {len(words)}")
count_words(words)
nk = input_values()
print(generate_large_string(words))
