"""Grader test for the Chapter 06 lab (ch06-lab).

Runs every lab question through the server-side runner with the plot checks
defined in _html_extra/api/lib/quiz-app.php:

- the reference solution (lab-answer cell) must pass,
- a student submission (question cell with the solution filled in) must pass,
- the unedited question cell must fail,
- common wrong answers must fail with a hint.

The checks are read from quiz-app.php through PHP, so the test fails if the
notebook and the grader definition drift apart. PHP comes from $DSM_PHP, a
working `php` on PATH, or the php:8.4-cli Docker image.

Run with:  .venv/bin/python tests/grader/test_ch06_lab.py   (or pytest)
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
LAB = ROOT / "chapters" / "06-matplotlib" / "assignments" / "lab.ipynb"
LAB_ID = "ch06-lab"

WRONG_ANSWERS = {
    "q1": {
        "no marker": "fig, ax = plt.subplots()\nax.plot(['Q1','Q2','Q3','Q4'], [120,135,128,150])\nax.set_title('Quarterly Revenue')\nax.set_xlabel('Quarter')\nax.set_ylabel('Revenue ($K)')",
        "axes swapped": "fig, ax = plt.subplots()\nax.plot([120,135,128,150], ['Q1','Q2','Q3','Q4'], marker='o')\nax.set_title('Quarterly Revenue')\nax.set_xlabel('Quarter')\nax.set_ylabel('Revenue ($K)')",
    },
    "q2": {
        "no legend": "fig, ax = plt.subplots()\nax.plot(['Q1','Q2','Q3','Q4'], [120,135,128,150], label='Actual')\nax.plot(['Q1','Q2','Q3','Q4'], [118,130,140,145], ls='--', color='gray', label='Forecast')\nax.set_title('Actual vs Forecast')",
        "styles reversed": "fig, ax = plt.subplots()\nax.plot(['Q1','Q2','Q3','Q4'], [120,135,128,150], ls='--', color='gray', label='Actual')\nax.plot(['Q1','Q2','Q3','Q4'], [118,130,140,145], label='Forecast')\nax.set_title('Actual vs Forecast')\nax.legend()",
    },
    "q3": {
        "default bins": "fig, axes = plt.subplots(1, 2, figsize=(10, 4))\naxes[0].bar(['North','South','East','West'], [150,120,180,90])\naxes[0].set_title('Revenue by Region')\naxes[1].hist([45,52,38,61,75,49,58,66,40,55,70,48])\naxes[1].set_title('Order Values')\nfig.suptitle('Regional Dashboard')",
        "axes title instead of suptitle": "fig, axes = plt.subplots(1, 2, figsize=(10, 4))\naxes[0].bar(['North','South','East','West'], [150,120,180,90])\naxes[0].set_title('Regional Dashboard')\naxes[1].hist([45,52,38,61,75,49,58,66,40,55,70,48], bins=5)\naxes[1].set_title('Order Values')",
    },
    "q4": {
        "line plot": "fig, ax = plt.subplots()\nax.plot([5,10,15,20,25,30,35,40], [60,85,110,120,150,165,190,205], 'o')\nax.set_xlabel('Ad Spend ($K)')\nax.set_ylabel('Sales ($K)')\nax.set_xlim(0, 50)\nax.set_ylim(0, 250)",
        "default limits": "fig, ax = plt.subplots()\nax.scatter([5,10,15,20,25,30,35,40], [60,85,110,120,150,165,190,205])\nax.set_xlabel('Ad Spend ($K)')\nax.set_ylabel('Sales ($K)')",
    },
    "q5": {
        "no savefig": "fig, ax = plt.subplots(figsize=(8, 4))\nax.bar(['North','South','East','West'], [12.5,9.8,14.2,7.6])\nax.set_title('Q2 Margin by Region')\nax.set_ylabel('Margin (%)')",
        "default dpi": "fig, ax = plt.subplots(figsize=(8, 4))\nax.bar(['North','South','East','West'], [12.5,9.8,14.2,7.6])\nax.set_title('Q2 Margin by Region')\nax.set_ylabel('Margin (%)')\nfig.savefig('regional_margin_q2.png')",
    },
}


def grader_python():
    if os.environ.get("DSM_GRADER_PYTHON"):
        return os.environ["DSM_GRADER_PYTHON"]
    venv = ROOT / ".venv" / "bin" / "python"
    return str(venv) if venv.exists() else sys.executable


def php_command():
    if os.environ.get("DSM_PHP"):
        return [os.environ["DSM_PHP"]], "/"
    php = shutil.which("php")
    if php:
        try:
            if subprocess.run([php, "-v"], capture_output=True).returncode == 0:
                return [php], "/"
        except OSError:
            pass  # e.g. a php binary built for another CPU
    if shutil.which("docker"):
        return ["docker", "run", "--rm", "-v", f"{API}:/api:ro", "php:8.4-cli", "php"], "/api"
    raise RuntimeError("No PHP found. Set DSM_PHP or install Docker.")


def lab_definition():
    command, api_root = php_command()
    api_dir = str(API) if api_root == "/" else api_root
    script = (
        f"require '{api_dir}/lib/quiz-app.php'; "
        f"echo json_encode(dsm_lab_definition('{LAB_ID}'));"
    )
    result = subprocess.run(command + ["-r", script], capture_output=True, text=True, check=True)
    return json.loads(result.stdout)


def lab_cells():
    notebook = json.loads(LAB.read_text())
    questions, solutions = [], []
    for cell in notebook["cells"]:
        tags = cell.get("metadata", {}).get("tags", [])
        source = "".join(cell["source"])
        if "thebe-interactive" in tags:
            questions.append(source)
        elif "lab-answer" in tags:
            solutions.append(source)
    # The submit panel sends the first five question cells as q1..q5.
    return questions[:5], solutions[:5]


def run_checks(code, checks):
    payload = json.dumps({"profile": "matplotlib", "code": code, "plot_checks": checks})
    result = subprocess.run(
        [grader_python(), "-I", str(RUNNER)], input=payload, capture_output=True, text=True, check=True
    )
    return json.loads(result.stdout)


def student_submission(question, solution):
    body = solution.split("\n", 1)[1]
    return question.replace("### Your code starts here.", "### Your code starts here.\n" + body, 1)


def collect_results():
    definition = lab_definition()
    checks = definition["plot_checks"]
    questions, solutions = lab_cells()
    results = []

    ids = [f"q{n}" for n in range(1, len(questions) + 1)]
    results.append(("definition", "question ids match notebook", sorted(checks) == ids, ""))
    results.append(("definition", "runner profile", definition.get("runner_profile") == "matplotlib", ""))

    for qid, question, solution in zip(ids, questions, solutions):
        cases = [
            ("reference solution", solution, True),
            ("student submission", student_submission(question, solution), True),
            ("unedited question", question, False),
        ]
        cases += [(name, code, False) for name, code in WRONG_ANSWERS.get(qid, {}).items()]
        for name, code, should_pass in cases:
            run = run_checks(code, checks.get(qid, []))
            passed = bool(run.get("ok")) and bool(run.get("plot", {}).get("passed"))
            detail = run.get("error") or " ".join(run.get("plot", {}).get("hints", []))
            has_hint = should_pass or bool(detail)
            results.append((qid, name, passed == should_pass and has_hint, detail))
    return results


def test_ch06_lab():
    failures = [r for r in collect_results() if not r[2]]
    assert not failures, failures


if __name__ == "__main__":
    all_results = collect_results()
    for qid, name, ok, detail in all_results:
        print(f"{'ok  ' if ok else 'FAIL'} {qid:10s} {name:32s} {detail}")
    failed = sum(1 for r in all_results if not r[2])
    print(f"{len(all_results) - failed} passed, {failed} failed")
    sys.exit(1 if failed else 0)
