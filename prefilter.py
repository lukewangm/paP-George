from rank_bm25 import BM25Okapi
import nltk
from nltk.corpus import stopwords
import numpy as np

from bm25 import clean

def bm25_prefilter(cases: list, query: str, k=10, return_scores=False):
    """
    k: return top k results
    """
    case_corpuses = [clean(case) for case in cases]
    bm25_comparer = BM25Okapi(case_corpuses)
    query = clean(query)
    
    scores = bm25_comparer.get_scores(query)
    top_k_idx = np.argsort(scores)[::-1][:k]
    
    top_cases = [cases[i] for i in top_k_idx]
    top_scores = [scores[i] for i in top_k_idx]
    if return_scores:
        return top_cases, top_scores
    else:
        return top_cases

cases = []
for i in range(1, 4):
    for j in range(1, 6):
        case = ""
        with open(f'data/note_{i}_cases/case_{j}.txt', 'r', encoding="utf-8") as file:
            for line in file:
                case += line + "\n"
        cases.append(case)
        
        
print(cases)
print(len(cases))

i=0
with open(f'data/notes/note_{i+1}.txt', 'r', encoding="utf-8") as file:
    query = ""
    for line in file:
        query += line + "\n"
        
print(query)
prefiltered_cases = bm25_prefilter(cases, query)
print(prefiltered_cases)
print(len(prefiltered_cases))