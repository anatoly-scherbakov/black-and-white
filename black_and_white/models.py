from typing import Optional, List, Dict, Union

import pydantic


class Choice(pydantic.BaseModel):
    title: str
    goto: Optional[str] = None


class QuestItem(pydantic.BaseModel):
    title: str
    content: Optional[str] = None


class Question(QuestItem):
    choices: Optional[List[Choice]] = None

    @pydantic.validator('choices', each_item=False, pre=True)
    def validate_choices(cls, value: dict):
        return [
            Choice(
                title=title,
                goto=goto
            )
            for title, goto in value.items()
        ]


class Banner(QuestItem):
    goto: Optional[str] = None


class Quest(Dict[str, Union[Banner, Question]]):
    pass
