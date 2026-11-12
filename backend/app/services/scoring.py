from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class QuestionScore:
    question_number: int
    selected_option: str | None
    correct_option: str
    status: str
    marks_awarded: float


def evaluate_responses(
    answer_key: Mapping[int, str],
    responses: Mapping[int, str | None],
    marks_correct: float = 1.0,
    marks_incorrect: float = 0.0,
) -> dict:
    """Evaluate against a verified answer-key mapping only.

    Missing responses are unanswered and score zero. The caller must ensure
    every answer-key entry has been verified before invoking this function.
    """
    if marks_correct < 0 or marks_incorrect > 0:
        raise ValueError("Use non-negative marks_correct and non-positive marks_incorrect")

    details = []
    correct = incorrect = unanswered = 0
    total = 0.0

    for number, correct_option in sorted(answer_key.items()):
        selected = responses.get(number)
        if selected is None:
            status, marks = "unanswered", 0.0
            unanswered += 1
        elif selected.upper() == correct_option.upper():
            status, marks = "correct", marks_correct
            correct += 1
        else:
            status, marks = "incorrect", marks_incorrect
            incorrect += 1

        total += marks
        details.append(QuestionScore(number, selected, correct_option, status, marks))

    attempted = correct + incorrect
    accuracy = (correct / attempted * 100) if attempted else None
    return {
        "details": details,
        "correct_count": correct,
        "incorrect_count": incorrect,
        "unanswered_count": unanswered,
        "attempted_count": attempted,
        "score": total,
        "accuracy_percent": accuracy,
    }
