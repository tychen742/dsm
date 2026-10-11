# DSM Quiz API

This directory is copied into the published Jupyter Book by `./deploy`.

## Endpoint

`POST /api/v1/quiz-attempts.php`

`POST /api/v1/lab-attempts.php`

`POST /api/v1/homework-attempts.php`

Stores and grades a quiz, lab, or homework attempt. If Canvas settings and Canvas IDs are available, the endpoint also attempts grade sync. Otherwise the attempt is saved with `pending` sync status.

The Chapter 01 preview, lab, and homework pages post each student attempt to these endpoints. The browser does not contain the answer key; grading happens on the server. The lab and homework code graders execute restricted Chapter 01 code cells and compare normalized output.

`GET /api/v1/assignment-settings.php?assignment_id=ch02-lab`

Returns the current answer visibility setting for an assignment. Book pages use this endpoint to hide answer cells until an admin unlocks them.

Saved fields include:

- quiz ID, chapter, and assignment slug
- student identifier
- Canvas course, assignment, and user IDs when provided
- score and maximum score
- submitted answers and per-question feedback as JSON
- Canvas sync status and sync error
- submission timestamp, IP address, and user agent

## Runner Profiles

Each lab or homework definition in `lib/quiz-app.php` picks a runner profile with `runner_profile`:

- `plain_python` (default): a small set of builtins (including `abs`) and string/list methods; no imports.
- `pandas`: adds `numpy` and `pandas` imports and the `range`, `zip`, `enumerate`, `abs`, `dict`, and `tuple` builtins, and the `&`, `|`, and `~` operators for combining boolean conditions (also allowed in the `sklearn` and plot profiles).
- `sklearn`: `numpy`, `pandas`, and scikit-learn. Students can write `from sklearn.linear_model import LinearRegression`; allowed modules are `sklearn.linear_model`, `sklearn.model_selection`, `sklearn.metrics`, `sklearn.neighbors`, `sklearn.preprocessing`, and `sklearn.cluster` (also `from sklearn import metrics`). `sklearn.datasets`, `fetch_*`, and file access are blocked, as in the plot profiles.

In every profile, the submitted cell runs in one namespace, so functions defined in the cell can read the cell's top-level variables, as in a notebook. The runner also prints one numpy array before running the cell, because numpy sets up array printing lazily and that setup needs imports that student code cannot make.
- `matplotlib`: adds `numpy`, `pandas`, and `matplotlib.pyplot` imports, list comprehensions, and `range`, `zip`, `enumerate`, `abs`, `dict`, `tuple`. File and system access (`read_*`, most `to_*`, `np.load`, `imread`, `fig.canvas`, and similar) is blocked by attribute name. Plots render with the `Agg` backend; `plt.show()` and `plt.close()` do nothing, and `savefig` records its arguments instead of writing a file.
- `seaborn`: the `matplotlib` profile plus `import seaborn as sns`. Dataset loaders (`load_dataset`, `get_dataset_names`, `get_data_home`) are blocked because they read files or the network; questions supply inline DataFrames.

A code question is graded by `code_outputs` (exact normalized stdout), `plot_checks` (chart properties, `matplotlib` and `seaborn` profiles only), or both; with both, the question passes only when both pass. Plot checks are listed per question:

```php
'runner_profile' => 'matplotlib',
'plot_checks' => [
    'q1' => [
        ['path' => 'axes.count', 'expected' => 1, 'hint' => 'Create one axes with plt.subplots().'],
        ['path' => 'axes[0].title', 'expected' => 'Quarterly Revenue', 'hint' => 'Set the chart title.'],
        ['path' => 'axes[0].lines[0].linestyle', 'expected' => '--', 'hint' => 'Draw the line dashed.'],
        ['path' => 'axes[0].lines.count', 'expected' => ['min' => 2], 'hint' => 'Plot both series.'],
    ],
],
```

Paths address the last figure the code created: `size`, `dpi`, `suptitle`, `sharex`, `sharey` (true when every axes shares that axis with the first), `figure_count`, `savefig[i].fname|dpi|format`, and `axes[i]` with `title`, `xlabel`, `ylabel`, `position` (`[left, bottom, width, height]` in figure fractions), `xlim`, `ylim`, `xscale`, `yscale`, `xticklabels`, `legend`, `has_legend`, `lines[j].color|linestyle|linewidth|marker|label|points|alpha`, `bars[j].bars|heights|label|alpha` (bar charts and histograms), `scatters[j].points|colors|label|alpha` (`colors` counts distinct point colors, e.g. 2 when `hue` maps two groups), `boxes` (Seaborn box count), `meshes` (heatmap count), `texts` (annotation strings, e.g. heatmap `annot=True` values), and `legend_title`. `figure_legend` lists legend entries that figure-level Seaborn functions (`relplot`, `catplot`, `displot`) put on the figure. Append `.count` for a length. Colors compare as lowercase hex (`'r'` and `'red'` are both `#ff0000`), line styles as `-`, `--`, `-.`, `:`, and numbers with a small tolerance. `expected` can also be `['min' => n]`, `['max' => n]`, `['one_of' => [...]]`, or `['contains' => value]`.

Students only see the `hint` of each failing check, never the expected value, so feedback does not reveal answers before the due date.

To see what the runner extracts from a solution, pipe it through the runner with `include_summary`:

```bash
echo '{"profile": "matplotlib", "include_summary": true, "code": "fig, ax = plt.subplots()\nax.plot([1, 2], [3, 4])"}' | ./grader-venv/bin/python -I lib/python_lab_runner.py
```

### Matplotlib Font Cache

Matplotlib builds a font cache on first import, which takes about 10 seconds and exceeds the grader timeout. Set `mplconfig_dir` to a directory the web server user can write, and warm the cache as that user after installing or upgrading Matplotlib:

```bash
sudo mkdir -p /var/www/dsm_private/mplconfig
sudo chown www-data:www-data /var/www/dsm_private/mplconfig
sudo -u www-data MPLCONFIGDIR=/var/www/dsm_private/mplconfig /var/www/dsm_private/grader-venv/bin/python -c "import matplotlib.pyplot"
```

If `mplconfig_dir` is empty, the runner uses `dsm-mplconfig` under the system temp directory, which may be cleared on reboot.

## Production Configuration

Do not commit production secrets. Put configuration outside the repository, then point `DSM_QUIZ_CONFIG` to it or use the production default path:

`/home/tychen/dsm_private/quiz_config.php`

The legacy `/var/www/dsm_private/quiz_config.php` path is supported only as a fallback. Keep real credentials outside the public web root.

## Grader Python Environment

The server-side grader re-runs submitted code outside Thebe. Keep its Python environment aligned with the packages students use in assignment notebooks.

Production DSM uses a dedicated grader virtual environment:

```bash
cd /var/www/dsm_private
python3 -m venv grader-venv
./grader-venv/bin/python -m pip install --upgrade pip
./grader-venv/bin/python -m pip install numpy pandas matplotlib seaborn scikit-learn
chmod -R g+rX /var/www/dsm_private/grader-venv
```

Configure the API to use that interpreter in the private config:

```php
'lab_grader' => [
    'python_bin' => '/var/www/dsm_private/grader-venv/bin/python',
    'timeout_seconds' => 3,
    'max_code_bytes' => 12000,
    'mplconfig_dir' => '/var/www/dsm_private/mplconfig',
],
```

Do not rely on a shell user's `~/.local` Python packages for production grading. Apache runs grader requests as the web server user, so user-site packages visible to `tychen` may not be visible to the grader.

Example:

```php
<?php
return [
    'database' => [
        'driver' => 'mysql',
        'dsn' => 'mysql:host=127.0.0.1;dbname=dsm_quiz;charset=utf8mb4',
        'username' => 'dsm_quiz',
        'password' => 'CHANGE_ME',
    ],
    'canvas' => [
        'base_url' => 'https://YOUR_CANVAS_DOMAIN',
        'access_token' => 'CHANGE_ME',
        'enabled' => true,
    ],
    'course' => [
        'students' => [
            [
                'student_identifier' => 'jtbyc9',
                'display_name' => 'Student Name',
                'email' => 'student@example.edu',
                'password_hash' => 'PASTE_PASSWORD_HASH_HERE',
            ],
        ],
    ],
    'student_auth' => [
        'require_authenticated_submissions' => true,
    ],
    'lab_grader' => [
        'python_bin' => '/var/www/dsm_private/grader-venv/bin/python',
        'timeout_seconds' => 3,
        'max_code_bytes' => 12000,
    ],
    'lti' => [
        'enabled' => true,
        'issuer' => 'https://canvas.instructure.com',
        'client_id' => 'CANVAS_DEVELOPER_KEY_CLIENT_ID',
        'deployment_ids' => ['CANVAS_DEPLOYMENT_ID'],
        'auth_login_url' => 'https://sso.canvaslms.com/api/lti/authorize_redirect',
        'jwks_url' => 'https://sso.canvaslms.com/api/lti/security/jwks',
        'redirect_uri' => 'https://thinkdsm.org/api/lti/launch.php',
        'default_target_link_uri' => 'https://thinkdsm.org/chapters/01-intro/assignments/preview.html',
    ],
    'auth' => [
        'bootstrap_admins' => [
            [
                'email' => 'you@example.edu',
                'display_name' => 'Your Name',
                'password_hash' => 'PASTE_PASSWORD_HASH_HERE',
            ],
        ],
    ],
];
```

Create the password hash on the server:

```bash
php -r 'echo password_hash("CHANGE_ME", PASSWORD_DEFAULT), PHP_EOL;'
```

For local development, if no config is found, the API tries SQLite at `/tmp/dsm_quiz_attempts.sqlite`. If the primary database save fails, the endpoint falls back to a newline-delimited JSON file at `/var/www/dsm_private/dsm_quiz_attempts.jsonl` so student submissions are still captured.

The JSONL fallback is a safety net, not the preferred production store. Configure MySQL/MariaDB before using the Canvas sync job for a class.

In production, each successful MySQL submission is also copied to an SQLite backup file. The default backup path is:

`/home/tychen/dsm_private/backups/dsm_quiz_attempts_backup.sqlite`

The backup directory must be writable by the web server group. The admin module reads from MySQL, not from this backup file; use the backup only for recovery.

## Admin Gradebook

After the database and admin bootstrap config are in place, open:

`/api/admin/`

The admin module supports:

- password-protected admin login
- score table with student identifier, quiz, score, Canvas status, and submitted answers
- detailed CSV export
- Canvas-ready CSV export keyed by `SIS Login ID`
- manual sync of pending or failed attempts to Canvas
- assignment answer locking and unlocking

The admin module requires a working PDO database connection. It does not read from the JSONL fallback store directly.

## Student Authentication

Student rows are stored in `quiz_users` with `role = 'student'`. The API creates or updates these rows from `course.students`, optional `course.allowed_student_identifiers`, or Canvas LTI launches.

Successful password, admin, and Canvas LTI logins are recorded in `login_events` with a timestamp, user ID, auth source, IP address, and user agent for later analysis and research. The `last_login_at` field remains only as a quick current-state summary.

Use `course.students` when you want direct student password login. Store only password hashes created with `password_hash`, not plaintext passwords. Students can sign in at:

`/api/student/login.php`

When `student_auth.require_authenticated_submissions` is `true`, preview, lab, and homework endpoints reject submissions without a Canvas LTI session or student password session. In that mode the submitted SIS Login ID is not trusted; the API uses the authenticated database user instead.

When `student_auth.require_university_email_verification` is `true`, a student must complete the first-login code flow before password login is accepted. The code is sent to a university email whose local part matches the student identifier, such as `jtbyc9@umsystem.edu`.

## Canvas LTI 1.3 Login

The LTI endpoints are:

- Login initiation URL: `https://thinkdsm.org/api/lti/login.php`
- Redirect URI: `https://thinkdsm.org/api/lti/launch.php`
- Target link URI for Chapter 01 preview: `https://thinkdsm.org/chapters/01-intro/assignments/preview.html`

Configure these URLs in a Canvas LTI 1.3 Developer Key. After installing the tool in a course, copy the Canvas client ID and deployment ID into the private `lti` config.

When launched from Canvas, the tool validates the signed Canvas `id_token`, creates or updates a student row in `quiz_users`, stores the Canvas identity in a secure LTI session, and saves quiz attempts with that identity. The student-facing quiz page calls `/api/v1/session.php` to fill the student identifier automatically.

## Manual Canvas Workflow

Use this workflow until the Canvas LTI tool is installed by an admin:

1. In Canvas, create assignments named with the hyphenated book assignment ID, such as `ch01-preview`, `ch01-lab`, and `ch01-homework`.
2. Set points to `10`.
3. Put the DSM assignment URLs in the Canvas assignment instructions:
   `https://thinkdsm.org/chapters/01-intro/assignments/preview.html`
   `https://thinkdsm.org/chapters/01-intro/assignments/lab.html`
   `https://thinkdsm.org/chapters/01-intro/assignments/homework.html`
4. Ask students to enter their Canvas `SIS Login ID` before submitting.
5. Review submissions in `https://thinkdsm.org/api/admin/`.
6. Export Canvas CSV from the admin page and upload it in Canvas Gradebook.

Manual submissions save in MySQL, but they do not automatically verify Canvas identity unless `student_auth.require_authenticated_submissions` is enabled and students sign in first. LTI launch remains the preferred production identity path.

## Later Canvas Sync

Pending or failed attempts can be synced after submission:

```bash
php /var/www/dsm/api/cli/sync-canvas.php --limit=100
```

Run the command from cron after production configuration is in place. The script reads the same `DSM_QUIZ_CONFIG` file, finds saved attempts with `pending` or `failed` status, sends the saved score to Canvas, and updates each row to `synced`, `failed`, or `skipped`.

Rows can only sync when they include `canvas_course_id`, `canvas_assignment_id`, and `canvas_user_id`. If the book is opened directly without Canvas/LTI launch parameters, attempts still save, but Canvas sync is marked `skipped` until those IDs are available.
