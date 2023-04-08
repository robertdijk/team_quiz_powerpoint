import argparse
import logging
import pprint
import random
from pathlib import Path
from typing import List

import pandas as pd

from team_quiz_powerpoint.helpers import load_excel_file
from team_quiz_powerpoint.pickeling import save_quiz, load_quiz
from team_quiz_powerpoint.model import Quiz

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel('DEBUG')


def main():
    parser = argparse.ArgumentParser(description='Print quiz pickle')
    parser.add_argument('-q', '--quiz', default="quiz.pickle", help="File to save the quiz in")
    args = parser.parse_args()

    q: Quiz = load_quiz(Path(args.quiz))

    pprint.pprint(q, width=40)


if __name__ == '__main__':
    main()
