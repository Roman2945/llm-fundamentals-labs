# RNN Quest

**Виконав:** Роман, ШІ-32, roman.mydzhyn@example.com

1. `lpnlp.start(..., lab="quest_rnn")` видав пакет `https://static.lp-nlp.com/quest-rnn/d7071db0908e.zip`.
2. У пакеті ваги Elman RNN (`embedding 133x128`, `W_h 160x128`, `U_h 160x160`, `W_y 133x160`) і словник з 133 символів.
3. Forward pass + жадібний декодинг від токена `[` до `]` (`rnn_decode.py`, транспонувати нічого не довелось,
   ваги у форматі `torch.nn.Linear`: `W @ x`).
4. Розкодоване повідомлення: `Назва виконавця: https://www.youtube.com/watch?v=dtSmUF0vMKE`.
5. За посиланням пісня **Gordosti** гурту **Ragapop**.
6. `lab.answer("Ragapop")` → **«Відповідь правильна ✅»**.

Виконаний ноутбук з усіма виходами: `LPNLP_RNN_Quest_done.ipynb`.
