from dependency_injector.wiring import inject, Provide
from openai import OpenAI

from app.core.config import settings
from app.core.container import Container


@inject
def get_content_summary(
        content: str,
        openai_client: OpenAI = Provide[
            Container.openai_client
        ],
) -> str:
    prompt = (
        'Напиши подробное, '
        'структурированное содержание для Википедии статьи '
        'на основе следующего текста:\n\n'
        f'{content[:10000]}'
    )

    completion = openai_client.chat.completions.create(
        model=settings.openai_model_name,
        messages=[{'role': 'user', 'content': prompt}]
    )
    return completion.choices[0].message.content