from bs4 import BeautifulSoup
import random

import requests


QUERIES = [
    'typeerror',
    'null',
    'undefined',
]

KEYWORDS = {
    'error': 2,
    'exception': 2,
    'not found': 1,
    'expected': 1,
    'cannot': 1,
    "can't": 1,
    'does not': 1,
    'has no': 1,
    ':': 1,
    '(': -0.5,
    ')': -0.5,
}

PAGESIZE = 100

SLURS = [s.lower() for s in requests.get(
    'https://raw.githubusercontent.com/dariusk/wordfilter/'
    'master/lib/badwords.json'
).json()]


def stackoverflow(endpoint, **params):
    default_params = {
        'site': 'stackoverflow',
        'pagesize': PAGESIZE,
    }

    default_params.update(params)

    return requests.get(
        'https://api.stackexchange.com/2.2/{}'.format(endpoint),
        params=default_params,
    ).json()


def get_question(query):
    total = stackoverflow(
        'search', intitle=query, filter='!--YDD7Dv_qhO',
    )['total']

    index = random.randint(0, total-1)
    page = index // PAGESIZE
    pageindex = index % 100

    question_id = stackoverflow(
        'search', intitle=query, page=page,
    )['items'][pageindex]['question_id']

    question, = stackoverflow(
        'questions/{}'.format(question_id), filter='!--KJ7DG6mRbp',
    )['items']
    return question['body']


def is_bad(snippet):
    for slur in SLURS:
        if slur in snippet:
            return True

    return False


def score_snippet(snippet):
    total_score = 0
    lower_snippet = snippet.lower()

    if (
        (not 20 < len(snippet) < 140) or
        ('\n ' in snippet) or
        is_bad(lower_snippet)
    ):
        return 0

    for keyword, score in KEYWORDS.items():
        if keyword in lower_snippet:
            total_score += score

    return total_score


def get_exception():
    query = random.choice(QUERIES)
    max_score = 0
    best_text = None

    while max_score == 0:
        soup = BeautifulSoup(get_question(query), 'html.parser')

        for element in soup.select('code'):
            text = element.text.strip()
            score = score_snippet(text)
            if score > max_score:
                max_score = score
                best_text = text

    return best_text


if __name__ == '__main__':
    print(get_exception())
