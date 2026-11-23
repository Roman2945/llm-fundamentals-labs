"""Один виклик LLM через різних провайдерів.

* Groq та OpenRouter мають OpenAI-сумісний API (бібліотека `openai`).
* Claude викликається через офіційний SDK `anthropic`.
"""
import anthropic
import openai

PROVIDERS = {
    "Groq (безкоштовний доступ)": {
        "kind": "openai",
        "base_url": "https://api.groq.com/openai/v1",
        "models": ["llama-3.3-70b-versatile", "openai/gpt-oss-120b", "openai/gpt-oss-20b", "qwen/qwen3-32b"],
        "key_hint": "gsk_...",
        "note": "Ключ: https://console.groq.com/keys",
    },
    "OpenRouter": {
        "kind": "openai",
        "base_url": "https://openrouter.ai/api/v1",
        "models": ["openai/gpt-oss-20b:free", "meta-llama/llama-3.3-70b-instruct:free", "google/gemma-3-27b-it:free"],
        "key_hint": "sk-or-...",
        "note": "Ключ: https://openrouter.ai/keys (моделі з :free безкоштовні)",
    },
    "Anthropic Claude": {
        "kind": "anthropic",
        "models": ["claude-haiku-5-5", "claude-sonnet-5-5", "claude-opus-5-5"],
        "key_hint": "sk-ant-...",
        "note": "Ключ: https://platform.claude.com (платно; Haiku 5.5 найдешевша)",
    },
}


class LLMError(Exception):
    pass


def complete(provider: str, model: str, api_key: str, system: str, user: str) -> str:
    cfg = PROVIDERS[provider]
    if cfg["kind"] == "anthropic":
        return _claude(model, api_key, system, user)
    return _openai_compatible(cfg["base_url"], model, api_key, system, user)


def _openai_compatible(base_url, model, api_key, system, user):
    client = openai.OpenAI(base_url=base_url, api_key=api_key)
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
            temperature=0.3,
        )
    except openai.AuthenticationError:
        raise LLMError("Невірний API ключ.")
    except openai.RateLimitError:
        raise LLMError("Перевищено ліміт запитів. Спробуйте за хвилину.")
    except openai.APIError as e:
        raise LLMError(f"Помилка API: {e}")
    return resp.choices[0].message.content or ""


def _claude(model, api_key, system, user):
    client = anthropic.Anthropic(api_key=api_key)
    try:
        resp = client.messages.create(
            model=model,
            max_tokens=8000,
            system=system,
            output_config={"effort": "low"},  # проста задача: мінімум "роздумів"
            messages=[{"role": "user", "content": user}],
        )
    except anthropic.AuthenticationError:
        raise LLMError("Невірний API ключ.")
    except anthropic.RateLimitError:
        raise LLMError("Перевищено ліміт запитів. Спробуйте за хвилину.")
    except anthropic.APIStatusError as e:
        raise LLMError(f"Помилка API ({e.status_code}): {e.message}")
    except anthropic.APIConnectionError:
        raise LLMError("Немає з'єднання з API.")
    if resp.stop_reason == "refusal":
        raise LLMError("Модель відмовилася обробляти цей текст.")
    return "".join(b.text for b in resp.content if b.type == "text")
