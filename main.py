import json
import os
import nltk
from nltk.corpus import stopwords
from openai import OpenAI
from credentials import OPENAI_API_KEY
from scraper.db_access import get_all

nltk.download('punkt_tab')
nltk.download('stopwords')
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY


# Case object for each case
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
        t = self.text if len(self.text) < 500 else self.text[:500] + "..."
        if len(self.file_name) > 0:
            s += "{" + f"file_name: {self.file_name}; {t}" + "}"
        else:
            s += "{ file_name: n/a; " + f"{t}" + "}"
        return s

    def __repr__(self):
        return self.__str__()


def read_cases(p):
    collected_cases = []
    for root, dirs, files in os.walk(p):
        for file in files:
            if file.endswith(".txt"):
                with open(os.path.join(root, file), 'r', encoding="utf-8") as f:
                    collected_cases.append(Case(f.read(), file_name=os.path.join(root, file)))
    return collected_cases

def build_database():
    # TODO: change this to match the new database structure later
    sets = ["data/note_1_cases", "data/note_2_cases", "data/note_3_cases"]

    total_cases = []
    for s in sets:
        total_cases += read_cases(s)

    return total_cases

def call_api(prompt, system_prompt=None):
    client = OpenAI()

    if system_prompt != None:
        messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}]
    else:
        messages = [{"role": "user", "content": prompt}]

    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        stream=True,
        response_format={"type": "json_object"}
    )

    return_str = ""

    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            return_str += chunk.choices[0].delta.content

    return return_str


def main():
    # assume that our query is in the following path

    path_to_sqlite = "scraper/articles.sqlite"

    # this is an array of articles, each article having four elements: id, title, full_link, abstract
    total_cases = get_all(path_to_sqlite)[:10] # for now we only use 10 articles in the database
    id_to_case_map = dict([(case[0], case) for case in total_cases])

    with open('data/notes/note_3.txt', 'r', encoding="utf-8") as file:
        query = file.read()
        query_nltk = nltk.word_tokenize(query.lower())

    # loads the documents
    # total_cases = build_database()

    # future: makes the bm25 filter

    # makes the request
    instruction = \
    """Imagine you are a highly skilled, multidisciplinary doctor. You’ve received a complex medical notes from a colleague, and everyone is struggling to make a clear diagnosis. Fortunately, you have access to several previously solved medical cases, and some of these cases are related to the current patient’s condition. You are provided with short abstracts summarizing these solved cases.
    Your task:
    - Carefully review the provided abstracts.
    - Select the most relevant cases that could provide insight into the current diagnosis.
    - Explain why you believe this case is the most relevant, based on symptoms, medical history, or other key details.
    
    You can select multiple case studies if you believe they are all relevant.
    
    Your response should be in a json format of the following structure:
    {
        "relevant_case": "case_1",
        "explanation": "case_1 is relevant because..."
    }
    """

    prompt = f"{instruction}\n\n<doctor_note>: \n{query}\n\n"
    # shuffle the cases
    import random
    random.shuffle(total_cases)
    for case in total_cases:
        id, title, full_link, abstract = case
        prompt += f"<case_{id}>: \n{abstract}\n\n"
    # Gets the response

    # cache the results for now
    cached_dir_fn = "query_cache.txt"
    if os.path.exists(cached_dir_fn):
        with open(cached_dir_fn, 'r') as f:
            return_str = f.read()
    else:
        print("about to call api")
        return_str = call_api(prompt)
        with open(cached_dir_fn, 'w') as f:
            f.write(return_str)

    return_str = json.loads(return_str)["relevant_cases"]

    # we now parse the response
    relevant_cases = []

    for key in return_str:
        if "case_id" not in key or "explanation" not in key:
            continue
        id = int(key["case_id"].split("_")[1])
        temp_obj = {}
        temp_obj["id"] = id
        temp_obj["explanation"] = key["explanation"]
        temp_obj["url"] = id_to_case_map[id][2]
        temp_obj["title"] = id_to_case_map[id][1]
        relevant_cases.append(temp_obj)

    import pdb
    pdb.set_trace()
    # return the array
    return relevant_cases


if __name__ == "__main__":
    main()