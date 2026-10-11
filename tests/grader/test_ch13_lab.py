"""Grader test for the Chapter 13 lab (ch13-lab).

Runs every lab question through the server-side runner (sklearn profile) with
the expected outputs defined in _html_extra/api/lib/quiz-app.php:

- the reference solution (lab-answer cell) must pass,
- a student submission (question cell with the solution filled in) must pass,
- the unedited question cell must fail,
- common wrong answers must fail with a hint.

Run with:  .venv/bin/python tests/grader/test_ch13_lab.py   (or pytest)
"""

import sys

from grader_helpers import ROOT, assignment_definition, check_questions, notebook_code_cells, report

LAB = ROOT / "chapters" / "13-multiple-regression" / "assignments" / "lab.ipynb"
LAB_ID = "ch13-lab"

SETUP = "import numpy as np\nimport pandas as pd\n"

LR = "from sklearn.linear_model import LinearRegression\n"
SP = "from sklearn.model_selection import train_test_split\nfrom sklearn.metrics import mean_squared_error, r2_score\n"
H = "homes = pd.DataFrame({'sqft': [2800, 2700, 2600, 2700, 1300, 2600, 2800, 1600, 1500, 1300, 2600, 2900, 2200, 2300, 2600, 1200], 'rooms': [9, 9, 8, 9, 5, 8, 9, 6, 6, 3, 9, 9, 7, 9, 9, 4], 'age': [44, 26, 42, 7, 45, 41, 27, 25, 17, 13, 15, 39, 20, 49, 20, 27], 'price': [400, 417, 350, 450, 151, 363, 390, 247, 259, 198, 403, 387, 326, 325, 409, 168]})\n"

WRONG_ANSWERS = {
    "q1": {
        "sqft only": SETUP + LR + H + "m = LinearRegression().fit(homes[['sqft']], homes['price'])\nprint('Intercept:', round(m.intercept_, 2))\nprint('sqft:', round(m.coef_[0], 2))",
    },
    "q2": {
        "difference reversed": SETUP + LR + H + "m = LinearRegression().fit(homes[['sqft', 'rooms', 'age']], homes['price'])\na = m.predict(pd.DataFrame({'sqft': [1800], 'rooms': [6], 'age': [20]}))[0]\nb = m.predict(pd.DataFrame({'sqft': [1800], 'rooms': [7], 'age': [20]}))[0]\nprint('House A:', round(a, 1))\nprint('House B:', round(b, 1))\nprint('Difference:', round(a - b, 2))",
    },
    "q3": {
        "includes a predictor with itself": SETUP + "print('Most correlated pair:', 'sqft', 'and', 'sqft')\nprint('Correlation:', 1.0)",
    },
    "q4": {
        "no random_state": SETUP + LR + SP + H + "X = homes[['sqft', 'rooms', 'age']]\ny = homes['price']\nXtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=0)\ns = LinearRegression().fit(Xtr[['sqft']], ytr)\nm = LinearRegression().fit(Xtr, ytr)\nprint('Simple RMSE:', round(np.sqrt(mean_squared_error(yte, s.predict(Xte[['sqft']]))), 2))\nprint('Multiple RMSE:', round(np.sqrt(mean_squared_error(yte, m.predict(Xte))), 2))",
        "MSE instead of RMSE": SETUP + LR + SP + H + "X = homes[['sqft', 'rooms', 'age']]\ny = homes['price']\nXtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=1)\ns = LinearRegression().fit(Xtr[['sqft']], ytr)\nm = LinearRegression().fit(Xtr, ytr)\nprint('Simple RMSE:', round(mean_squared_error(yte, s.predict(Xte[['sqft']])), 2))\nprint('Multiple RMSE:', round(mean_squared_error(yte, m.predict(Xte)), 2))",
    },
    "q5": {
        "training R-squared": SETUP + LR + SP + H + "X = homes[['sqft', 'rooms', 'age']]\ny = homes['price']\nXtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=1)\nm = LinearRegression().fit(Xtr, ytr)\nprint('Test R-squared:', round(r2_score(ytr, m.predict(Xtr)), 3))",
    },
}


def collect_results():
    definition = assignment_definition("dsm_lab_definition", LAB_ID)
    checks = {}
    outputs = definition["code_outputs"]
    questions, solutions = notebook_code_cells(LAB, "lab-answer")
    ids = [f"q{n}" for n in range(1, len(questions) + 1)]
    results = [
        ("definition", "question ids match notebook", sorted(outputs) == ids, ""),
        ("definition", "runner profile", definition.get("runner_profile") == "sklearn", ""),
        ("definition", "output ids are question ids", set(outputs) <= set(ids), ""),
    ]
    return results + check_questions(ids, questions, solutions, checks, WRONG_ANSWERS, "sklearn", outputs)


def test_ch13_lab():
    failures = [r for r in collect_results() if not r[2]]
    assert not failures, failures


if __name__ == "__main__":
    sys.exit(report(collect_results()))
