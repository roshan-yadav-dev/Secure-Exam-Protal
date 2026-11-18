from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field, model_validator


class ExamMode(str, Enum):
    PRACTICE = "practice"
    REAL = "real"


class ExamCreate(BaseModel):
    title: str = Field(min_length=3, max_length=120)
    question_set_id: str = Field(min_length=1)
    duration_minutes: int = Field(ge=1, le=300)
    mode: ExamMode
    marks_correct: float = Field(default=1.0, ge=0)
    marks_incorrect: float = Field(default=0.0, le=0)
    question_numbers: list[int] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_question_numbers(self):
        if any(number < 1 for number in self.question_numbers):
            raise ValueError("Question numbers must be positive integers")
        if len(set(self.question_numbers)) != len(self.question_numbers):
            raise ValueError("Question numbers must be unique")
        return self


class Option(BaseModel):
    label: Literal["A", "B", "C", "D"]
    text: str = Field(min_length=1)


class QuestionPreview(BaseModel):
    question_number: int = Field(ge=1)
    stem: str = Field(min_length=1)
    options: list[Option] = Field(min_length=2, max_length=4)
    source_page: int = Field(ge=1)
    extraction_confidence: float | None = Field(default=None, ge=0, le=1)


class AnswerKeyEntry(BaseModel):
    question_number: int = Field(ge=1)
    correct_option: Literal["A", "B", "C", "D"]
    verified: bool = False
    source_page: int | None = Field(default=None, ge=1)
