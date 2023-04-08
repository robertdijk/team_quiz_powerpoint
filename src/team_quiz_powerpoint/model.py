import itertools
import random
from dataclasses import dataclass, field
from enum import IntEnum
from typing import Optional, List, Tuple

from team_quiz_powerpoint.helpers import iter_nth


class Answer(IntEnum):
    A = 1
    B = 2
    C = 3
    D = 4


@dataclass
class Team():
    name: str


@dataclass
class Question:
    id: int
    question: str
    correct_answer: str
    wrong_answers: (str, str, str)
    team: Team
    author: Optional[str] = None
    _permutation: int = field(default_factory=(lambda: random.randrange(24)))

    def get_answers(self) -> List[str]:
        answers = [self.correct_answer, self.wrong_answers[0], self.wrong_answers[1], self.wrong_answers[2]]
        answers = iter_nth(itertools.permutations(answers), self._permutation)
        return answers

    def get_correct_answer(self) -> Answer:
        return Answer(self.get_answers().index(self.correct_answer) + 1)


@dataclass()
class Player:
    id: int
    name: str
    team: Team = None
    answers: List[Optional[Answer]] = field(default_factory=list)


@dataclass
class Quiz():
    questions: List[Question] = field(default_factory=list)
    teams: List[Team] = field(default_factory=list)
    players: List[Player] = field(default_factory=list)

    def get_or_make_team(self, team_name: str) -> Team:
        team_name = team_name.lower()

        for t in self.teams:
            if t.name == team_name:
                return t

        new_team = Team(team_name)
        self.teams.append(new_team)
        return new_team

    def add_question_from_row(self, data, field_names) -> ():
        self.questions = list(filter(lambda e: e.id != data.loc["ID"], self.questions))

        q = Question(data.loc["ID"], data.loc[field_names["question-field"]],
                     data.loc[field_names["correct-answer-field"]],
                     (data.loc[field_names["wrong-answer-field-1"]],
                      data.loc[field_names["wrong-answer-field-2"]],
                      data.loc[field_names["wrong-answer-field-3"]]),
                     self.get_or_make_team(data.loc[field_names["team-field"]]))
        q.author = data.loc[field_names["name-field"]]

        self.questions.append(q)

    def add_player_from_row(self, data, field_names) -> ():
        self.players = list(filter(lambda e: e.id != data.loc["ID"], self.players))

        p = Player(data.loc["ID"],
                   data.loc[field_names["name-field"]],
                   self.get_or_make_team(data.loc[field_names["team-field"]]))
        for i in range(len(self.questions)):
            try:
                answer = Answer[data.loc[field_names["question-field"].format(i)]]
                p.answers.append(answer)
            except KeyError:
                p.answers.append(None)

        self.players.append(p)

    def get_team_scores_for_question(self, question_index) -> List[Tuple[Team, int, int]]:
        result: List[List] = [[t, 0, 0] for t in self.teams]

        correct_answer = self.questions[question_index].get_correct_answer()

        for p in self.players:
            team_score = next(obj for obj in result if obj[0] == p.team)
            if p.answers[question_index] == correct_answer:
                team_score[1] += 1
            else:
                team_score[2] += 1

        result: List[Tuple[Team, int, int]] = [(r[0], r[1], r[2]) for r in result]
        return result

    def get_player_score(self, player: Player, question_team_filter: Optional[Team] = None) -> Tuple[int, int]:
        correct = 0
        incorrect = 0

        for index, question in enumerate(self.questions):
            if question_team_filter and question.team is not question_team_filter:
                continue
            if player.answers[index] and player.answers[index] == question.get_correct_answer():
                correct += 1
            else:
                incorrect += 1
        return correct, incorrect

    def get_players_ranking(self):
        scores = [(p, self.get_player_score(p)) for p in self.players]
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores

    def get_team_score(self, team: Team, question_team_filter: Optional[Team] = None) -> Tuple[int, int]:
        correct = 0
        incorrect = 0

        for player in self.players:
            if player.team == team:
                score = self.get_player_score(player, question_team_filter)
                correct += score[0]
                incorrect += score[1]

        return correct, incorrect

    def get_team_scores(self, question_team_filter: Optional[Team] = None) -> List[Tuple[Team, int, int]]:
        result = []
        for team in self.teams:
            score = self.get_team_score(team, question_team_filter)
            result.append((team, score[0], score[1]))

        return result
