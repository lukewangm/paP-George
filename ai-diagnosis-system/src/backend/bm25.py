from rank_bm25 import BM25Okapi
import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download()
nltk.download('punkt_tab')
nltk.download('stopwords')
from nltk.corpus import stopwords


def clean(s):
    s = nltk.word_tokenize(s.lower())
    s = [word for word in s if word not in stopwords.words('english')]
    s = [word for word in s if word.isalnum()]
    return s

def build_corpus():
    corpuses = []
    for i in range(1, 4):
        corpuses.append([])
        for j in range(1, 6):
            corpuses[i-1].append("")
            with open(f'../../../data/note_{i}_cases/case_{j}.txt', 'r', encoding="utf-8") as file:
                for line in file:
                    corpuses[i-1][j-1] += line + "\n"

    # Tokenize and remove stopwords
    for i in range(3):
        for j in range(5):
            corpuses[i][j] = clean(corpuses[i][j])

    corpuses = [(corpuses[i], BM25Okapi(corpuses[i])) for i in range(3)]

    return corpuses

corpuses = build_corpus()
for i in range(3):
    with open(f'../../../data/notes/note_{i+1}.txt', 'r', encoding="utf-8") as file:
        query = ""
        for line in file:
            query += line + "\n"
        query = clean(query)
    scores = corpuses[i][1].get_scores(query)
    print(scores)
    print(corpuses[i][1].get_top_n(query, corpuses[i][0], n=1))

