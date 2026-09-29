"""Book-wide consistency test for preview quiz answer keys.

For every chapter with an assignments/preview.ipynb, checks that the answer
key in quiz-app.php matches the questions in the notebook, that each answer
is one of the question's choices, and that correct answers are not placed in
a guessable pattern (the A, B, C, D, A, B, ... cycle, a single letter, or
one letter used for more than half the questions).

Run with:  .venv/bin/python tests/grader/test_preview_keys.py   (or pytest)
"""

import json
import re
import sys
from collections import Counter

from grader_helpers import ROOT, assignment_definition, report


def preview_notebooks():
    for path in sorted(ROOT.glob("chapters/[0-9][0-9]-*/assignments/preview.ipynb")):
        yield "ch" + path.parts[-3][:2] + "-preview", path


def notebook_questions(path):
    notebook = json.loads(path.read_text())
    for cell in notebook["cells"]:
        match = re.search(r"var questions = (\[.*?\]);", "".join(cell["source"]), re.S)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                return js_object_questions(match.group(1))
    return None


def js_object_questions(text):
    """Parse the older unquoted style: { id: 'q1', prompt: '...', choices: { A: '...', ... } }."""
    questions = []
    for qid, choices in re.findall(r"id:\s*'(q\d+)'.*?choices:\s*\{(.*?)\}", text, re.S):
        letters = re.findall(r"([A-D]):\s*'", choices)
        questions.append({"id": qid, "choices": {letter: letter for letter in letters}})
    return questions


def collect_results():
    results = []
    for preview_id, path in preview_notebooks():
        questions = notebook_questions(path)
        if questions is None:
            continue  # previews without a question list are not auto-graded here
        key = (assignment_definition("dsm_quiz_definition", preview_id) or {}).get("questions", {})
        ids = [q["id"] for q in questions]
        results.append((preview_id, "key ids match notebook", sorted(key, key=lambda q: int(q[1:])) == ids, ""))
        results.append((preview_id, "answers are choices", all(key.get(q["id"]) in q["choices"] for q in questions), ""))
        answers = [key.get(q) for q in ids]
        cycle = ["ABCD"[i % 4] for i in range(len(answers))]
        most = Counter(answers).most_common(1)[0][1] if answers else 0
        guessable = answers == cycle or len(set(answers)) == 1 or most > len(answers) / 2
        results.append((preview_id, "answers not in a guessable pattern", not guessable, "".join(a or "?" for a in answers)))
    return results


def test_preview_keys():
    failures = [r for r in collect_results() if not r[2]]
    assert not failures, failures


if __name__ == "__main__":
    sys.exit(report(collect_results()))
