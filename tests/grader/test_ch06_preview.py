"""Consistency test for the Chapter 06 preview quiz (ch06-preview).

Checks that the answer key in quiz-app.php matches the questions in
preview.ipynb, that every correct answer is a term from the chapter
glossary on the landing page, and that correct answers are not placed in
a fixed pattern such as A, B, C, D, A, B, ...

Run with:  .venv/bin/python tests/grader/test_ch06_preview.py   (or pytest)
"""

import json
import re
import sys

from grader_helpers import ROOT, assignment_definition, report

PREVIEW = ROOT / "chapters" / "06-matplotlib" / "assignments" / "preview.ipynb"
LANDING = ROOT / "chapters" / "06-matplotlib" / "0600-matplotlib.ipynb"
PREVIEW_ID = "ch06-preview"


def preview_questions():
    notebook = json.loads(PREVIEW.read_text())
    for cell in notebook["cells"]:
        match = re.search(r"var questions = (\[.*?\]);", "".join(cell["source"]), re.S)
        if match:
            return json.loads(match.group(1))
    raise AssertionError("questions not found in preview.ipynb")


def glossary_terms():
    notebook = json.loads(LANDING.read_text())
    text = "".join("".join(cell["source"]) for cell in notebook["cells"])
    rows = re.findall(r"^\| \d+ \| (.+?) \|", text, re.M)
    return {row.strip("`") for row in rows}


def collect_results():
    key = assignment_definition("dsm_quiz_definition", PREVIEW_ID)["questions"]
    questions = preview_questions()
    terms = glossary_terms()
    ids = [q["id"] for q in questions]
    results = [
        ("definition", "question ids match notebook", sorted(key, key=lambda q: int(q[1:])) == ids, ""),
        ("definition", "ten questions", len(questions) == 10, f"{len(questions)} questions"),
    ]
    for question in questions:
        answer = key.get(question["id"])
        correct = question["choices"].get(answer, "")
        results.append((question["id"], "answer is one of the choices", answer in question["choices"], answer or ""))
        results.append((question["id"], "correct choice is a glossary term", correct.strip("`") in terms, correct))
    answers = [key[q] for q in ids]
    cycle = ["ABCD"[i % 4] for i in range(len(answers))]
    results.append(("definition", "answers are not a fixed pattern", answers != cycle and len(set(answers)) > 1, "".join(answers)))
    return results


def test_ch06_preview():
    failures = [r for r in collect_results() if not r[2]]
    assert not failures, failures


if __name__ == "__main__":
    sys.exit(report(collect_results()))
