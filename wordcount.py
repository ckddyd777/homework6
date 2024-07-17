import sys, re, operator, string
from abc import ABCMeta
import pandas as pd
from io import BytesIO

class WordCountBase():
    __metaclass__ = ABCMeta

    def info(self):
        return self.__class__.__name__

class DataLoader(WordCountBase):
    def __init__(self, path_to_file):
        pattern = re.compile('[\W_]+')

        if type(path_to_file) is str:
            with open(path_to_file) as f:
                self._data = f.read()
        elif type(path_to_file) is list:
            self._data = []
            for path in path_to_file:
                data = path.read().decode("utf-8", errors="replace")
                self._data.append(pattern.sub(' ', data).lower())
        else:
            self._data = path_to_file.read().decode("utf-8", errors="replace")
            self._data = pattern.sub(' ', self._data).lower()

    def words(self):
        return self._data.split()

    def info(self):
        return super(DataLoader, self).info() + ": My major data structure is a " + self._data.__class__.__name__

class StopWord(WordCountBase):
    def __init__(self):
        with open('./data/stop_words.txt', 'r') as f:
            self._stop_words = f.read().split(',')
        self._stop_words.extend(list(string.ascii_lowercase))

    def is_stop_word(self, word):
        return word in self._stop_words

    def info(self):
        return super(StopWord, self).info() + ": My major data structure is a " + self._stop_words.__class__.__name__

class WordFrequency(WordCountBase):
    def __init__(self):
        self._word_freqs = {}

    def increment_count(self, word):
        if word in self._word_freqs:
            self._word_freqs[word] += 1
        else:
            self._word_freqs[word] = 1

    def sorted(self):
        return sorted(self._word_freqs.items(), key=operator.itemgetter(1), reverse=True)

    def info(self):
        return super(WordFrequency, self).info() + ": My major data structure is a " + self._word_freqs.__class__.__name__

class WordFrequencyController(WordCountBase):
    def __init__(self, path_to_file):
        self._storage_manager = []
        if type(path_to_file) is list:
            for path in path_to_file:
                self._storage_manager.append(DataLoader(path))
        self._stop_word_manager = StopWord()
        self._word_freq_manager = WordFrequency()

    def run(self):
        for storage in self._storage_manager:
            for w in storage.words():
                if not self._stop_word_manager.is_stop_word(w):
                    self._word_freq_manager.increment_count(w)

        word_freqs = self._word_freq_manager.sorted()
        df = pd.DataFrame(word_freqs[0:25])
        return df
