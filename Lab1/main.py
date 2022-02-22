import nltk.data


def count_words(array: []):
    for word in array:
        print(f'"{word}" appears {array.count(word)} time(s)')


def clear_sentence_symbols(sentence: str):
    sentence = sentence.replace(".", "")
    sentence = sentence.replace(",", "")
    sentence = sentence.replace("!", "")
    sentence = sentence.replace("?", "")
    sentence = sentence.replace(":", "")
    sentence = sentence.replace(";", "")
    sentence = sentence.replace("=", "")
    return sentence


def text_to_array(text: str, array: []):
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    arr = tokenizer.tokenize(text)
    for el in arr:
        el = clear_sentence_symbols(el)
        a = nltk.word_tokenize(el)
        for word in a:
            array.append(word)


fp = open('input.txt')
data = fp.read()
words = []
text_to_array(data, words)
count_words(words)
