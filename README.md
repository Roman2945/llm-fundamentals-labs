# LLM Fundamentals (LPNLP): виконані завдання

Роман, група ШІ-32, roman.mydzhyn@example.com

| # | Завдання | Що в папці | Статус |
|---|---|---|---|
| 01 | LPNLP 08 - Text generation (Colab) | виконаний ноутбук з виходами | усі checkpoints і `lab.answer` прийнято ✅ |
| 02 | RNN Quest (Colab) | ноутбук, `rnn_decode.py` | відповідь **Ragapop** прийнята ✅ |
| 03 | Text Classification Quest (Colab) | ноутбук з дотренуванням ModernBERT (acc 0.962), малюнок | відповідь **rocket** прийнята ✅ |
| 04 | LLM Homework - Basic (Google Doc) | Streamlit-додаток «Текстовий помічник» | готово до запуску й деплою |
| 05 | LLM Homework - Agents (Google Doc) | Streamlit AI Examiner Agent з інструментами | готово до запуску й деплою |

Ці ж ноутбуки лежать на Google Drive у папці «LLM Fundamentals - виконані лаби».

## Деплой на HuggingFace Spaces (одним кліком)
1. Створіть акаунт на https://huggingface.co і токен з правом **Write**: https://huggingface.co/settings/tokens
2. Двічі клацніть `deploy.bat` у цій папці й вставте токен.
3. Скрипт створить два Spaces (`lpnlp-text-helper` і `lpnlp-ai-examiner`), заллє код і збереже посилання в `deploy_links.txt`.
   Збірка займає 2-5 хвилин. Ці посилання й треба здати у ВНС.

## Як запустити локально
```powershell
.\.venv\Scripts\Activate.ps1
cd 04_llm_basic_app        # або 05_ai_examiner_agent
streamlit run app.py
```
Потрібен API ключ LLM: безкоштовно на https://console.groq.com/keys (Groq) або https://openrouter.ai/keys.
Ключ вводиться в боковій панелі застосунку.
