import openai
from functools import lru_cache
from collections import deque
from typing import TypedDict


class Message:
    role: str
    content: str


class Choices:
    index: int
    message: Message
    finish_reason: str


class Completion:
    id: str
    object: str
    created: str
    model: str
    choices: list[Choices]
    usage: dict


class Prompt(TypedDict):
    role: str
    content: str


context_store: dict[int, deque[Prompt]] = {}


@lru_cache
async def reply_from_openai(message: str, user_id: int) -> str:
    """Lấy phản hồi OpenAI

    Args:
        message (str): Nội dung
        user_id (int): ID người dùng

    Returns:
        str: Phản hồi từ OpenAi
    """
    if user_id not in context_store:
        context_store[user_id] = deque(maxlen=5)

    context = context_store.get(user_id)
    assert(isinstance(context, deque))

    context.append(Prompt(role='user', content=message))
    completion: Completion = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=list(context)
    )  # type: ignore

    respond = completion.choices[0].message.content
    context.append(Prompt(role='system', content=respond))

    return respond
