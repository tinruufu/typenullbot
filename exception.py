from bs4 import BeautifulSoup
import random
import re

import requests

try:
    from secrets import se_auth
except ImportError:
    print('no stack exchange credentials, api will be throttled')
    se_auth = {}


QUERIES = [
    'type',
    'null',
    'undefined',
]

KEYWORDS = {
    'exception': 2,
    'error': 2,
    'uncaught': 2,
    'unexpected': 2,
    'raised': 2,
    'undefined': 1,
    'null': 1,
    'not found': 1,
    'expected': 1,
    'cannot': 1,
    "can't": 1,
    'does not': 1,
    'has no': 1,
    ':': 1,
    'http://': -3,
    'https://': -3,
    '(': -0.5,
    ')': -0.5,
    '{': -0.5,
    '}': -0.5,
}

PAGESIZE = 30

SLURS = [s.lower() for s in requests.get(
    'https://raw.githubusercontent.com/dariusk/wordfilter/'
    'master/lib/badwords.json'
).json()]


def stackoverflow(endpoint, **params):
    default_params = {
        'site': 'stackoverflow',
        'pagesize': PAGESIZE,
        **se_auth,
    }

    default_params.update(params)

    resp = requests.get(
        'https://api.stackexchange.com/2.2/{}'.format(endpoint),
        params=default_params,
    ).json()

    if 'error_id' in resp:
        raise ValueError(resp)

    return resp


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
        is_bad(lower_snippet) or
        re.search(r'@[a-z\d_]+', lower_snippet)
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
