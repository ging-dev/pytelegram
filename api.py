import openai


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


async def get_reply_from_openai(message: str) -> str:
    """Lấy phản hồi OpenAI

    Args:
        message (str): Nội dung

    Returns:
        str: Phản hồi từ OpenAi
    """
    completion: Completion = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": message}]
    )  # type: ignore

    return completion.choices[0].message.content
