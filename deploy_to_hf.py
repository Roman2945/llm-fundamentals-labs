"""Деплой обох Streamlit-додатків на HuggingFace Spaces одним запуском.

Потрібен токен HuggingFace з правом WRITE: https://huggingface.co/settings/tokens
Запуск: deploy.bat (подвійний клік) або  python deploy_to_hf.py
"""
import getpass
import os
import sys
from pathlib import Path

from huggingface_hub import HfApi

ROOT = Path(__file__).parent
APPS = [
    ("04_llm_basic_app", "lpnlp-text-helper", "LLM проєкт (базовий): Текстовий помічник"),
    ("05_ai_examiner_agent", "lpnlp-ai-examiner", "Agents: AI Examiner Agent"),
]
IGNORE = ["__pycache__/*", "**/__pycache__/*", "*.pyc", ".venv/*", "data/results/*", "data/exams.jsonl"]


def main():
    token = os.environ.get("HF_TOKEN") or getpass.getpass(
        "Вставте токен HuggingFace (Write) і натисніть Enter (символи не відображаються): ").strip()
    if not token:
        sys.exit("Токен не введено.")
    api = HfApi(token=token)
    try:
        user = api.whoami()["name"]
    except Exception as e:  # noqa: BLE001
        sys.exit(f"Токен не підійшов: {e}")
    print(f"Користувач HuggingFace: {user}\n")

    links = []
    for folder, space, title in APPS:
        repo_id = f"{user}/{space}"
        print(f"→ {title}: створюю Space {repo_id} ...")
        api.create_repo(repo_id, repo_type="space", space_sdk="docker", exist_ok=True)
        api.upload_folder(repo_id=repo_id, repo_type="space", folder_path=str(ROOT / folder),
                          ignore_patterns=IGNORE, commit_message="Deploy from LLM-Fundamentals-Labs")
        url = f"https://huggingface.co/spaces/{repo_id}"
        links.append(f"{title}: {url}")
        print(f"  готово: {url}\n")

    (ROOT / "deploy_links.txt").write_text("\n".join(links) + "\n", encoding="utf-8")
    print("Посилання збережено в deploy_links.txt. Збірка Space триває 2-5 хвилин,")
    print("після цього сторінка відкриється й можна вводити API ключ LLM.")
    for line in links:
        print(line)


if __name__ == "__main__":
    main()
