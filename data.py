import re
import nltk
from nltk import ngrams
from nltk.tokenize import word_tokenize
from collections import Counter

from pandas import DataFrame
from textblob import TextBlob

import generate_basic_dataframe

class DocsData:
    def __init__(self):
        self.df = generate_basic_dataframe.generate_basic_dataframe(use_cache=True)

    def count_specific_words_appearing_in_content(self, words: set[str], field_name: str,) -> None:
        """How many times a set of words appears in the content of each entry"""
        self.df[field_name] = self.df["content"].apply(lambda x: len([word for word in x.split() if word.lower() in words]))

    @staticmethod
    def get_phrase_frequencies(text: str, n: int) -> Counter:
        """
        Get the frequencies of each n-gram in a text for n in the range 0 to N

        Parameters:
        text (str): The text from which to count n-gram frequencies
        n (int): The maximum number of words in the sequence

        Returns:
        dict: A dictionary where the keys are n-grams and the values are frequencies
        """
        # Tokenize the text
        nltk.download('punkt')
        text = re.sub(r'\n', ' ', text)
        text = re.sub(r'[^\w\s]', '', text)
        text = text.lower()
        words = word_tokenize(text)

        # Generate n-grams for each number in the range 1 to N+1
        n_grams = ngrams(words, n)

        return Counter(n_grams)

    @staticmethod
    def get_word_frequencies(text: str) -> Counter:
        """
        Get the frequencies of each word in a text

        Parameters:
        text (str): The text from which to count word frequencies

        Returns:
        dict: A dictionary where the keys are words and the values are frequencies
        """
        # Tokenize the text
        nltk.download('punkt')
        words = word_tokenize(text)
        return Counter(words)

    def extend_dataframe(self) -> None:
        """Extend the DataFrame with new columns: word_count, sentiment_polarity, sentiment_subjectivity, phrases_counter, words_counter"""
        self.df["word_count"] = self.df["content"].apply(lambda x: len(str(x).split(" ")))
        self.df["sentiment_polarity"] = self.df["content"].apply(lambda x: TextBlob(x).sentiment[0])
        self.df["sentiment_subjectivity"] = self.df["content"].apply(lambda x: TextBlob(x).sentiment[1])
        self.df['phrases_counter'] = self.df['content'].apply(lambda text: self.get_phrase_frequencies(text, 5))
        self.df['words_counter'] = self.df['content'].apply(self.get_word_frequencies)

    def get_dataframe(self) -> DataFrame:
        return self.df