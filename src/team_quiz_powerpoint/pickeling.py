import pickle
from pathlib import Path
from typing import List

from team_quiz_powerpoint.model import Question, Quiz


def save_quiz(quiz: Quiz, output: Path) -> ():
    with output.open('wb') as f:
        pickle.dump(quiz, f)


def load_quiz(output: Path) -> Quiz:
    with output.open('rb') as f:
        quiz = pickle.load(f)
    return quiz
