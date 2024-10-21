import os
from dataclasses import dataclass

import nltk
from nltk.corpus import stopwords
from rank_bm25 import BM25Okapi
import bert_score

class Case:
    def __init__(self, text, file_name=""):
        self.file_name = file_name
        self.text = text
        self.nltk = self._nltk_tokenize()

    def _nltk_tokenize(self):
        s = nltk.word_tokenize(self.text.lower())
        s = [word for word in s if word not in stopwords.words('english')]
        s = [word for word in s if word.isalnum()]
        return s

    def __str__(self):
        s = ""
        t = self.text if len(self.text) < 50 else self.text[:50] + "..."
        if len(self.file_name) > 0:
            s += "{" + f"file_name: {self.file_name}; {t}" + "}"
        else:
            s += "{ file_name: n/a; " + f"{t}" + "}"
        return s

    def __repr__(self):
        return self.__str__()


class CaseDatabase:

    def __init__(self):
        # TODO Consider storing both the cleaned and tokenized text, for faster retrieval
        self.cases = []

    def read_cases(self, p):
        for root, dirs, files in os.walk(p):
            for file in files:
                if file.endswith(".txt"):
                    with open(os.path.join(root, file), 'r', encoding="utf-8") as f:
                        self.cases.append(Case(f.read(), file_name=os.path.join(root, file)))

    def build_corpus(self):
        self.read_cases("data/note_1_cases")
        self.read_cases("data/note_2_cases")
        self.read_cases("data/note_3_cases")

    def simple_query(self, q, k=1):
        bm = BM25Okapi([x.nltk for x in self.cases])
        scores = bm.get_scores(q)
        # Pick the top k cases
        return sorted(zip(self.cases, scores), key=lambda x: x[1], reverse=True)[:k]

    def bert_query(self, q, k=1):
        p, r, f1 = bert_score.score([q] * len(self.cases), [x.text for x in self.cases], lang="en")
        # Pick the top k cases, sorted by f1
        return sorted(zip(self.cases, f1), key=lambda x: x[1], reverse=True)[:k]


if __name__ == "__main__":
    db = CaseDatabase()
    db.build_corpus()

    with open('data/notes/note_1.txt', 'r', encoding="utf-8") as file:
        query = file.read()
        query_nltk = nltk.word_tokenize(query.lower())
    print("Simple query:")
    print(db.simple_query(query_nltk, 2))
    print("\nBERT query:")
    print(db.bert_query(query, 2))