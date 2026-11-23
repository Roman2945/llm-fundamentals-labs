"""Офлайн-перевірка циклу агента з фейковою LLM (без API ключа)."""
import json, types
import agent as A

script = [
    [("start_exam", {"email": "test@example.com", "name": "Test"})],
    "Тема: ... Що таке BPE?",
    [("get_next_topic", {})],
    "Наступне питання",
    [("get_next_topic", {}), ],
    [("get_next_topic", {})],
    [("get_next_topic", {})],
    "Оцінка 7/10",
]

class FakeCompletions:
    def __init__(self): self.i = 0
    def create(self, **kw):
        step = script[self.i]; self.i += 1
        if isinstance(step, str):
            msg = types.SimpleNamespace(content=step, tool_calls=None)
        else:
            calls = [types.SimpleNamespace(id=f"c{self.i}{k}", function=types.SimpleNamespace(name=n, arguments=json.dumps(a)))
                     for k, (n, a) in enumerate(step)]
            msg = types.SimpleNamespace(content=None, tool_calls=calls)
        return types.SimpleNamespace(choices=[types.SimpleNamespace(message=msg)])

ag = A.ExamAgent("Groq (безкоштовний доступ)", "x", "k")
ag.client = types.SimpleNamespace(chat=types.SimpleNamespace(completions=FakeCompletions()))
print(ag.reply("Test, test@example.com"))
print(ag.reply("відповідь"))
topics = ag.session.topics
# finish
script.append([("end_exam", {"email": "test@example.com", "score": 7})]); script.append("Готово")
ag.client.chat.completions.i = 4
print(ag.reply("не знаю"))
print(ag.reply("ok"))
print("finished:", ag.session.finished, ag.session.score, topics)
for h in ag.history: print(h["role"], "|", h["content"][:70])
