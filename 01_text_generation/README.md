# LPNLP 08 - Text generation

**Виконав:** Роман, ШІ-32, roman.mydzhyn@example.com

Ноутбук `LPNLP_08_Text_generation_done.ipynb` виконано повністю в Colab (з виходами всіх клітинок).

Що реалізовано (GPT-2 + HuggingFace transformers):
* `greedy_decode` — цикл генерації токен за токеном, `argmax` по softmax останнього кроку, зупинка на `eos_token` або `max_len`. Checkpoint **«greedy decode» прийнято ✅**.
* `generate(..., sample_fn)` — універсальна функція з підстановкою стратегії вибору токена.
* Sampling з температурою: `softmax(log p / T)`. Висновок: при T ≤ 0.5 текст майже детермінований і повторюється, при T ≥ 1.5 розпадається, оптимум ≈ **0.8**. Checkpoint **«softmax temperature» = 0.8 прийнято ✅**.
* Top-k sampling (k = 15 і k = 3 з prompt).
* Nucleus (top-p) sampling: накопичуємо ймовірності відсортованих токенів, доки сума < p, далі семплюємо серед ядра. При p = 0 це greedy.
* Генерація від prompt і zero-shot «класифікація» відгуків (GPT-2 замалий: негативному відгуку поставив «B+», позитивному «5»).
* Обидва `lab.answer("Готово!")` → **«Відповідь правильна ✅»**.
