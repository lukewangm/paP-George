from rank_bm25 import BM25Okapi
import nltk
from nltk.corpus import stopwords

def clean(s):
    s = nltk.word_tokenize(s.lower())
    s = [word for word in s if word not in stopwords.words('english')]
    s = [word for word in s if word.isalnum()]
    return s


def bm25_prefilter(cases: list, query: str, k=10):
    """
    k: return top k results
    """
    # Extract the text from the 3rd index of each tuple
    case_corpuses = [clean(case[3]) for case in cases]

    bm25_comparer = BM25Okapi(case_corpuses)
    query = clean(query)
    scores = bm25_comparer.get_scores(query)

    return sorted(zip(cases, scores), key=lambda x: x[1], reverse=True)[:k]

if __name__ == "__main__":
    cases = []
    for i in range(1, 4):
        for j in range(1, 6):
            case = ""
            with open(f'data/note_{i}_cases/case_{j}.txt', 'r', encoding="utf-8") as file:
                for line in file:
                    case += line + "\n"
            cases.append(case)

    with open(f'data/notes/note_1.txt', 'r', encoding="utf-8") as file:
        query = ""
        for line in file:
            query += line + "\n"

    prefiltered_cases = bm25_prefilter(cases, query)
    print(prefiltered_cases)
    print(len(prefiltered_cases))