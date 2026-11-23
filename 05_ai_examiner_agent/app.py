"""AI Examiner Agent: веб-інтерфейс на Streamlit."""
import anthropic
import openai
import streamlit as st

from agent import PROVIDER_MODELS, ExamAgent

st.set_page_config(page_title="AI Examiner", page_icon="🎓")
st.title("🎓 AI Examiner: іспит з NLP")
st.markdown(
    "LLM-агент приймає усний іспит з курсу NLP. Він питає ім'я та email, перевіряє студента в базі "
    "(`start_exam`), бере теми (`get_next_topic`), веде діалог і наприкінці ставить оцінку 0..10 "
    "з відгуком та записує результат (`end_exam`). Ключ API вводиться збоку й ніде не зберігається."
)

with st.sidebar:
    st.header("Налаштування LLM")
    provider = st.selectbox("Провайдер", list(PROVIDER_MODELS))
    model = st.selectbox("Модель", PROVIDER_MODELS[provider])
    custom = st.text_input("Або впишіть назву моделі вручну", "")
    api_key = st.text_input("API ключ", type="password")
    show_tools = st.checkbox("Показувати виклики інструментів", value=True)
    if st.button("Почати новий іспит"):
        st.session_state.pop("agent", None)
        st.session_state.pop("chat", None)
        st.rerun()
    st.caption("Тестові студенти: data/students.json")

if not api_key:
    st.info("Введіть API ключ у боковій панелі, щоб почати.")
    st.stop()

config = (provider, custom.strip() or model, api_key)
if st.session_state.get("config") != config:
    st.session_state.config = config
    st.session_state.agent = ExamAgent(*config)
    st.session_state.chat = [("assistant", "Вітаю! Я екзаменатор курсу NLP. Назвіть, будь ласка, ваше ім'я та email.")]

agent: ExamAgent = st.session_state.agent

for role, text in st.session_state.chat:
    with st.chat_message(role):
        st.markdown(text)

if show_tools:
    calls = [h for h in agent.history if h["role"] == "tool_call"]
    if calls:
        with st.sidebar.expander(f"Виклики інструментів ({len(calls)})"):
            for h in calls:
                st.code(h["content"], language="text")

if agent.session.finished:
    st.success(f"Іспит завершено. Оцінка: {agent.session.score:g} / 10. Результат записано.")
    st.stop()

if prompt := st.chat_input("Ваша відповідь..."):
    st.session_state.chat.append(("user", prompt))
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Екзаменатор думає..."):
            try:
                answer = agent.reply(prompt)
            except (anthropic.AuthenticationError, openai.AuthenticationError):
                answer = "⚠️ Невірний API ключ."
            except (anthropic.APIError, openai.APIError) as e:
                answer = f"⚠️ Помилка API: {e}"
        st.markdown(answer or "…")
    st.session_state.chat.append(("assistant", answer or "…"))
    st.rerun()
