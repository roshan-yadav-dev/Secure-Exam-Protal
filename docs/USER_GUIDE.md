# Learner User Guide

This guide describes the intended learner workflow. Features marked as planned are not yet available in the current application build.

## 1. Prepare your PDFs

You need two separate files:
1. **Question paper PDF** — contains numbered MCQs and their options.
2. **Answer-key PDF** — contains the corresponding correct option for each question.

For the first release, use single-correct MCQs with option labels A, B, C and D. Keep question numbers consistent between both documents. If the answer key uses a different numbering scheme, you will need to map entries manually.

Scanned PDFs, handwritten annotations, multi-column layouts and image-heavy papers may require manual correction after extraction.

## 2. Upload and verify

1. Sign in.
2. Upload the question paper.
3. Upload the matching answer-key PDF.
4. Wait for extraction to finish.
5. Review question numbers, question text and option labels.
6. Review each extracted answer-key mapping against the uploaded key.
7. Correct any extraction or mapping errors.
8. Mark the set verified only after all selected questions are correct.

Do not start an exam with unverified answers. Incorrect answer-key mapping produces incorrect scores and misleading PDF annotations.

## 3. Configure an exam

Choose:
- Exam title.
- Verified question set.
- Questions to include.
- Duration.
- Marks for a correct answer.
- Negative marks for an incorrect answer.
- Mode: Practice or Real Exam.

For a GATE-style mock, enter the scoring values from the specific paper/instructions you are following. Do not assume every exam uses the same negative-marking rule.

## 4. Attempt questions

The intended exam workspace includes:
- Question and option display.
- Previous/next navigation.
- Question palette.
- Save/select answer.
- Mark for review.
- Clear response.
- Countdown timer.
- Submit confirmation.

Your answers should be saved to the server as you progress. The server's deadline is authoritative; the browser timer is only a display.

## 5. Practice Mode

Practice Mode is designed for learning. Depending on the exam setting, feedback may be shown immediately after an answer or after the attempt. The correct answer and available explanation can be reviewed.

## 6. Real Exam Mode

Real Exam Mode simulates a timed test:
- Correct answers are hidden while the attempt is active.
- The timer continues to the server-defined deadline.
- The attempt is submitted manually or automatically on expiry.
- Results and answer review are available only after submission.

## 7. Understand your result

The result summary includes:
- Correct count.
- Incorrect count.
- Unanswered count.
- Attempted count.
- Total score.
- Accuracy among attempted questions.

Scoring:
- Correct: add the configured positive marks.
- Incorrect: add the configured negative marks.
- Unanswered: zero marks.

Accuracy is `correct / attempted × 100`. If no question was attempted, accuracy is displayed as not applicable.

## 8. Download the annotated PDF

The report is generated from a copy of your original question paper:
- Green: correct option.
- Red: your selected incorrect option.
- Unanswered: correct option highlighted green, with an unanswered label.
- A legend and result summary explain the markings.

If the PDF layout cannot be mapped confidently, the report should include a review note rather than placing a highlight on the wrong text.

## 9. Troubleshooting

- **PDF rejected:** confirm it is a valid PDF and within the configured upload size/page limits.
- **Questions missing:** check whether the document is scanned or uses a complex layout; correct the extraction manually.
- **Answer numbers do not match:** map question numbers manually before verification.
- **Timer expired:** the server may have reached the deadline even if the browser timer appeared out of sync.
- **Report unavailable:** report generation may still be processing or may have failed; retry only after checking attempt status.
