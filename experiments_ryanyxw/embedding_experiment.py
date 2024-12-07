from openai import OpenAI
from experiments_ryanyxw.openai_api import get_embedding
from credentials import OPENAI_API_KEY
import numpy as np
import os
# setup the API key
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

def cosine_similarity(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

def main():
    client = OpenAI()

    # load the data of case_1 for each note
    cases = []
    for i in range(1, 4):
        with open(f"/Users/ryanyxw/Desktop/USC/Senior/Fall/CSCI401/papaSamZeim/data/note_{i}_cases/case_1.txt", "r") as f:
            cases.append(f.read())

    # load the doctor's notes
    note = ""
    with open(f"/Users/ryanyxw/Desktop/USC/Senior/Fall/CSCI401/papaSamZeim/data/notes/note_1.txt", "r") as f:
        note = f.read()


    # get embeddings
    cases_embed = [get_embedding(client, case) for case in cases]
    note_embed = get_embedding(client, note)


    # calculate the cosine similarity
    similarities = [cosine_similarity(note_embed, case_embed) for case_embed in cases_embed]

    # get the index of the most similar case
    most_similar_case = np.argmax(similarities)
    print(f"Most similar case is case_{most_similar_case + 1}")
    import pdb
    pdb.set_trace()

if __name__ == "__main__":
    main()
