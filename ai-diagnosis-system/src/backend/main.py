import json
import os
import nltk
import ssl

from nltk import deprecated

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('punkt_tab')
nltk.download('stopwords')
from nltk.corpus import stopwords

from openai import OpenAI
from credentials import OPENAI_API_KEY
from prefilter import bm25_prefilter
from scraper.db_access import get_all


os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY


# Case object for each case
@deprecated
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


@deprecated
def read_cases(p):
    collected_cases = []
    for root, dirs, files in os.walk(p):
        for file in files:
            if file.endswith(".txt"):
                with open(os.path.join(root, file), 'r', encoding="utf-8") as f:
                    collected_cases.append(Case(f.read(), file_name=os.path.join(root, file)))
    return collected_cases

@deprecated
def build_database():
    # TODO: change this to match the new database structure later
    sets = ["data/note_1_cases", "data/note_2_cases", "data/note_3_cases"]

    total_cases = []
    for s in sets:
        total_cases += read_cases(s)

    return total_cases

def call_api(prompt, system_prompt=None):
    """Calls the OpenAI API with the given prompt and returns the response"""
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

def get_openai_response(query, num_articles=10):
    """
    this function will return an array of dictionaries with the following structure:
    [{
        "id": "1",
        "explanation": "case_1 is relevant because..."
        "url": "https://www.example.com",
        "title": "Case 1 Title"
    }]
    PLEASE make sure the query passed in is a STRING containing the doctor's note.
    """

    path_to_sqlite = "scraper/articles.sqlite"

    # this is an array of articles, each article having four elements: id, title, full_link, abstract
    total_cases = get_all(path_to_sqlite)

    # we implement bm25 filter here
    total_cases = bm25_prefilter(total_cases, query, k=num_articles)

    # we create a dictionary mapping the id to the case
    id_to_case_map = dict([(case[0], case) for case in total_cases])

    # makes the request
    instruction = \
        """Imagine you are a highly skilled, multidisciplinary doctor. You’ve received a complex medical notes from a colleague, and everyone is struggling to make a clear diagnosis. Fortunately, you have access to several previously solved medical cases, and some of these cases are related to the current patient’s condition. You are provided with short abstracts summarizing these solved cases.
        Your task:
        - Carefully review the provided abstracts.
        - Select the most relevant cases that could provide insight into the current diagnosis.
        - Explain why you believe this case is the most relevant, based on symptoms, medical history, or other key details.
    
        You can select multiple case studies if you believe they are all relevant. You should give at least 3 cases and at most 5 cases.
    
        Your response should be in a json format of the following structure:
        {'relevant_cases': [{
            "case_id": "case_4",
            "explanation": "This case is relevant because..."
        },
        {
            "case_id": "case_7",
            "explanation": "This case is relevant because..."
        }]}
        """

    prompt = f"{instruction}\n\n<doctor_note>: \n{query}\n\n"
    # shuffle the cases
    import random
    random.shuffle(total_cases)
    for case in total_cases:
        id, title, full_link, abstract = case
        prompt += f"<case_{id}>: \n{abstract}\n\n"
    # Gets the response

    return_str = call_api(prompt)
    print(return_str)

    if ("relevant_cases" not in return_str):
        return []
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

    # return the array



    # json.dumps(get_openai_response(query, num_articles=10))
    return json.dumps(relevant_cases)

def main():

    with open('data/notes/note_3.txt', 'r', encoding="utf-8") as file:
        query = file.read()
        query_nltk = nltk.word_tokenize(query.lower())

    json_object = get_openai_response(query, num_articles=10)

    import pdb
    pdb.set_trace()


if __name__ == "__main__":
    main()