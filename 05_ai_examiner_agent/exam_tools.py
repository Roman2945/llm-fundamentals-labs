"""Функції-інструменти агента-екзаменатора.

Замість бази даних використовуються JSON-файли в папці data/:
  * students.json  -- список студентів (ім'я, email)
  * topics.json    -- список тем курсу NLP
  * exams.jsonl    -- журнал початку/завершення іспитів
  * results/       -- повні результати іспитів з історією чату
"""
import json
import random
from datetime import datetime
from pathlib import Path

DATA = Path(__file__).parent / "data"
RESULTS = DATA / "results"


def now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def _load(name):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def _log(event: dict):
    with open(DATA / "exams.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps({**event, "datetime": now()}, ensure_ascii=False) + "\n")


class StudentNotFound(Exception):
    pass


class ExamSession:
    """Стан одного іспиту. get_next_topic() не має аргументів, тож стан
    (які теми ще лишилися) зберігається тут, по одному об'єкту на сесію."""

    def __init__(self, n_topics=(2, 3), seed=None):
        self.n_topics = n_topics
        self.rng = random.Random(seed)
        self.email = None
        self.name = None
        self.topics: list[str] = []
        self.next_index = 0
        self.finished = False
        self.score = None

    # --- start_exam(email, name) -> list[str] ---------------------------
    def start_exam(self, email: str, name: str) -> list[str]:
        email = email.strip().lower()
        students = _load("students.json")
        match = [s for s in students if s["email"].lower() == email]
        if not match:
            raise StudentNotFound(f"Студента з email {email} немає в базі даних.")
        student = match[0]
        all_topics = _load("topics.json")
        k = self.rng.randint(*self.n_topics)
        self.email, self.name = email, student["name"]
        self.topics = self.rng.sample(all_topics, k)
        self.next_index = 0
        _log({"event": "start_exam", "email": email, "name": student["name"], "topics": self.topics})
        return self.topics

    # --- get_next_topic() -> str ---------------------------------------
    def get_next_topic(self) -> str:
        if not self.topics:
            raise RuntimeError("Іспит ще не розпочато: спочатку викличте start_exam.")
        if self.next_index >= len(self.topics):
            return "NO_MORE_TOPICS"
        topic = self.topics[self.next_index]
        self.next_index += 1
        return topic

    # --- end_exam(email, score, history) -> None -----------------------
    def end_exam(self, email: str, score: float, history: list[dict]) -> None:
        score = max(0.0, min(10.0, float(score)))
        self.finished, self.score = True, score
        RESULTS.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        out = RESULTS / f"{email.replace('@', '_at_')}_{stamp}.json"
        out.write_text(
            json.dumps(
                {"email": email, "name": self.name, "topics": self.topics, "score": score,
                 "finished_at": now(), "history": history},
                ensure_ascii=False, indent=2,
            ),
            encoding="utf-8",
        )
        _log({"event": "end_exam", "email": email, "score": score, "file": out.name})
