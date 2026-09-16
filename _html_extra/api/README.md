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
./grader-venv/bin/python -m pip install numpy pandas
chmod -R g+rX /var/www/dsm_private/grader-venv
```

Configure the API to use that interpreter in the private config:

```php
'lab_grader' => [
    'python_bin' => '/var/www/dsm_private/grader-venv/bin/python',
    'timeout_seconds' => 3,
    'max_code_bytes' => 12000,
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
