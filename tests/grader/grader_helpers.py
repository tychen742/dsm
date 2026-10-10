"""Shared helpers for assignment grader tests.

Definitions are read from _html_extra/api/lib/quiz-app.php through PHP, so
tests fail if a notebook and its grader definition drift apart. PHP comes
from $DSM_PHP, a working `php` on PATH, or the php:8.4-cli Docker image.
The runner uses $DSM_GRADER_PYTHON, the repo .venv, or the current Python.
"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
API = ROOT / "_html_extra" / "api"
RUNNER = API / "lib" / "python_lab_runner.py"


def grader_python():
    if os.environ.get("DSM_GRADER_PYTHON"):
        return os.environ["DSM_GRADER_PYTHON"]
    venv = ROOT / ".venv" / "bin" / "python"
    return str(venv) if venv.exists() else sys.executable


def php_command():
    if os.environ.get("DSM_PHP"):
        return [os.environ["DSM_PHP"]], str(API)
    php = shutil.which("php")
    if php:
        try:
            if subprocess.run([php, "-v"], capture_output=True).returncode == 0:
                return [php], str(API)
        except OSError:
            pass  # e.g. a php binary built for another CPU
    if shutil.which("docker"):
        return ["docker", "run", "--rm", "-v", f"{API}:/api:ro", "php:8.4-cli", "php"], "/api"
    raise RuntimeError("No PHP found. Set DSM_PHP or install Docker.")


def assignment_definition(function, assignment_id):
    """Call a quiz-app.php definition function, e.g. dsm_lab_definition."""
    command, api_dir = php_command()
    script = f"require '{api_dir}/lib/quiz-app.php'; echo json_encode({function}('{assignment_id}'));"
    result = subprocess.run(command + ["-r", script], capture_output=True, text=True, check=True)
    return json.loads(result.stdout)


def notebook_code_cells(path, answer_tag):
    """Return (question cells, answer cells) in page order, first five of each."""
    notebook = json.loads(Path(path).read_text())
    questions, answers = [], []
    for cell in notebook["cells"]:
        tags = cell.get("metadata", {}).get("tags", [])
        source = "".join(cell["source"])
        if "thebe-interactive" in tags:
            questions.append(source)
        elif answer_tag in tags:
            answers.append(source)
    # Submit panels send the first five question cells.
    return questions[:5], answers[:5]


def run_plot_checks(code, checks, profile="matplotlib"):
    payload = json.dumps({"profile": profile, "code": code, "plot_checks": checks})
    result = subprocess.run(
        [grader_python(), "-I", str(RUNNER)], input=payload, capture_output=True, text=True, check=True
    )
    return json.loads(result.stdout)


def student_submission(question, solution):
    """The question cell with the solution body typed into it."""
    body = solution.split("\n", 1)[1]
    return question.replace("### Your code starts here.", "### Your code starts here.\n" + body, 1)


def normalize_output(text):
    """Match dsm_normalize_lab_output() in quiz-app.php."""
    return "\n".join(line.rstrip() for line in text.replace("\r\n", "\n").strip().split("\n"))


def check_questions(ids, questions, solutions, checks, wrong_answers, profile="matplotlib", outputs=None):
    """Grade solutions, filled-in submissions, unedited questions, and wrong answers.

    A case passes when the plot checks pass and, if the question has an
    expected output in `outputs`, the normalized stdout matches it.
    Returns (question id, case name, ok, detail) tuples.
    """
    outputs = outputs or {}
    results = []
    for qid, question, solution in zip(ids, questions, solutions):
        cases = [
            ("reference solution", solution, True),
            ("student submission", student_submission(question, solution), True),
            ("unedited question", question, False),
        ]
        cases += [(name, code, False) for name, code in wrong_answers.get(qid, {}).items()]
        for name, code, should_pass in cases:
            run = run_plot_checks(code, checks.get(qid, []), profile)
            passed = bool(run.get("ok")) and bool(run.get("plot", {}).get("passed"))
            detail = run.get("error") or " ".join(run.get("plot", {}).get("hints", []))
            if qid in outputs and run.get("ok"):
                output_ok = normalize_output(run.get("stdout", "")) == normalize_output(outputs[qid])
                passed = passed and output_ok
                if not output_ok:
                    detail = (detail + " Output did not match.").strip()
            has_hint = should_pass or bool(detail)
            results.append((qid, name, passed == should_pass and has_hint, detail))
    return results


def report(results):
    for qid, name, ok, detail in results:
        print(f"{'ok  ' if ok else 'FAIL'} {qid:10s} {name:32s} {detail}")
    failed = sum(1 for r in results if not r[2])
    print(f"{len(results) - failed} passed, {failed} failed")
    return 1 if failed else 0
