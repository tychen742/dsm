<?php
declare(strict_types=1);

function dsm_load_config(): array
{
    $default = [
        'database' => [
            'driver' => 'sqlite',
            'dsn' => 'sqlite:/tmp/dsm_quiz_attempts.sqlite',
            'username' => null,
            'password' => null,
        ],
        'canvas' => [
            'enabled' => false,
            'base_url' => null,
            'access_token' => null,
        ],
        'file_store' => [
            'path' => '/var/www/dsm_private/dsm_quiz_attempts.jsonl',
            'sqlite_backup_path' => '/home/tychen/dsm_private/backups/dsm_quiz_attempts_backup.sqlite',
            'sqlite_backup_enabled' => true,
        ],
        'auth' => [
            'session_name' => 'dsm_quiz_admin',
            'bootstrap_admins' => [],
        ],
        'student_auth' => [
            'session_name' => 'dsm_student',
            'require_authenticated_submissions' => false,
            'require_university_email_verification' => false,
            'allowed_email_domains' => ['umsystem.edu', 'mst.edu'],
            'verification_code_minutes' => 20,
            'email_from' => 'no-reply@thinkdsm.org',
            'smtp' => [
                'host' => null,
                'port' => 587,
                'username' => null,
                'password' => null,
                'secure' => 'tls',
            ],
        ],
        'lab_grader' => [
            'python_bin' => 'python3',
            'timeout_seconds' => 3,
            'max_code_bytes' => 12000,
            'python_paths' => [],
        ],
        'lti' => [
            'enabled' => false,
            'session_name' => 'dsm_lti',
            'issuer' => 'https://canvas.instructure.com',
            'client_id' => null,
            'deployment_ids' => [],
            'auth_login_url' => 'https://sso.canvaslms.com/api/lti/authorize_redirect',
            'jwks_url' => 'https://sso.canvaslms.com/api/lti/security/jwks',
            'redirect_uri' => 'https://thinkdsm.org/api/lti/launch.php',
            'default_target_link_uri' => 'https://thinkdsm.org/chapters/01-intro/assignments/preview.html',
        ],
    ];

    $paths = [];
    $envPath = getenv('DSM_QUIZ_CONFIG');
    if (is_string($envPath) && $envPath !== '') {
        $paths[] = $envPath;
    }
    $paths[] = __DIR__ . '/../../.env.local.php';
    $paths[] = '/home/tychen/dsm_private/quiz_config.php';
    $paths[] = '/var/www/dsm_private/quiz_config.php';

    foreach ($paths as $path) {
        if (is_readable($path)) {
            $loaded = require $path;
            if (is_array($loaded)) {
                return array_replace_recursive($default, $loaded);
            }
        }
    }

    return $default;
}

function dsm_connect_database(array $database): PDO
{
    return new PDO(
        (string) $database['dsn'],
        $database['username'] ?? null,
        $database['password'] ?? null,
        [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
        ]
    );
}

function dsm_initialize_schema(PDO $pdo): void
{
    $driver = (string) $pdo->getAttribute(PDO::ATTR_DRIVER_NAME);
    $idColumn = $driver === 'sqlite'
        ? 'id INTEGER PRIMARY KEY AUTOINCREMENT'
        : 'id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY';

    $pdo->exec(
        'CREATE TABLE IF NOT EXISTS quiz_users (
            ' . $idColumn . ',
            email VARCHAR(255) NOT NULL UNIQUE,
            display_name VARCHAR(255) NULL,
            role VARCHAR(32) NOT NULL DEFAULT \'student\',
            password_hash VARCHAR(255) NULL,
            status VARCHAR(32) NOT NULL DEFAULT \'active\',
            canvas_user_id VARCHAR(64) NULL,
            student_identifier VARCHAR(255) NULL,
            email_verified_at DATETIME NULL,
            verification_code_hash VARCHAR(255) NULL,
            verification_code_expires_at DATETIME NULL,
            last_login_at DATETIME NULL,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        )'
    );
    dsm_add_column_if_missing($pdo, 'quiz_users', 'student_identifier', 'VARCHAR(255) NULL');
    dsm_add_column_if_missing($pdo, 'quiz_users', 'canvas_user_id', 'VARCHAR(64) NULL');
    dsm_add_column_if_missing($pdo, 'quiz_users', 'email_verified_at', 'DATETIME NULL');
    dsm_add_column_if_missing($pdo, 'quiz_users', 'verification_code_hash', 'VARCHAR(255) NULL');
    dsm_add_column_if_missing($pdo, 'quiz_users', 'verification_code_expires_at', 'DATETIME NULL');
    dsm_add_column_if_missing($pdo, 'quiz_users', 'last_login_at', 'DATETIME NULL');

    $pdo->exec(
        'CREATE TABLE IF NOT EXISTS login_events (
            ' . $idColumn . ',
            user_id INT NOT NULL,
            auth_source VARCHAR(32) NOT NULL,
            ip_address VARCHAR(64) NULL,
            user_agent TEXT NULL,
            logged_in_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        )'
    );

    $pdo->exec(
        'CREATE TABLE IF NOT EXISTS quiz_attempts (
            ' . $idColumn . ',
            quiz_id VARCHAR(100) NOT NULL,
            chapter VARCHAR(100) NOT NULL,
            assignment_slug VARCHAR(100) NOT NULL,
            student_user_id INT NULL,
            canvas_course_id VARCHAR(64) NULL,
            canvas_assignment_id VARCHAR(64) NULL,
            canvas_user_id VARCHAR(64) NULL,
            lti_deployment_id VARCHAR(255) NULL,
            lti_context_id VARCHAR(255) NULL,
            lti_resource_link_id VARCHAR(255) NULL,
            lti_lineitem_url TEXT NULL,
            student_identifier VARCHAR(255) NULL,
            score DECIMAL(6,2) NOT NULL,
            max_score DECIMAL(6,2) NOT NULL,
            answers_json TEXT NOT NULL,
            feedback_json TEXT NOT NULL,
            canvas_sync_status VARCHAR(32) NOT NULL DEFAULT \'pending\',
            canvas_sync_error TEXT NULL,
            synced_to_canvas_at DATETIME NULL,
            ip_address VARCHAR(64) NULL,
            user_agent TEXT NULL,
            submitted_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        )'
    );

    dsm_add_column_if_missing($pdo, 'quiz_attempts', 'student_user_id', 'INT NULL');
    dsm_add_column_if_missing($pdo, 'quiz_attempts', 'lti_deployment_id', 'VARCHAR(255) NULL');
    dsm_add_column_if_missing($pdo, 'quiz_attempts', 'lti_context_id', 'VARCHAR(255) NULL');
    dsm_add_column_if_missing($pdo, 'quiz_attempts', 'lti_resource_link_id', 'VARCHAR(255) NULL');
    dsm_add_column_if_missing($pdo, 'quiz_attempts', 'lti_lineitem_url', 'TEXT NULL');
    dsm_ensure_decimal_score_columns($pdo);
    dsm_migrate_assignment_aliases($pdo);

    $assignmentIdColumn = $driver === 'sqlite'
        ? 'assignment_id VARCHAR(100) NOT NULL PRIMARY KEY'
        : 'assignment_id VARCHAR(100) NOT NULL PRIMARY KEY';
    $integerDefault = $driver === 'sqlite'
        ? 'INTEGER NOT NULL DEFAULT 0'
        : 'TINYINT(1) NOT NULL DEFAULT 0';

    $pdo->exec(
        'CREATE TABLE IF NOT EXISTS assignment_settings (
            ' . $assignmentIdColumn . ',
            answers_unlocked ' . $integerDefault . ',
            updated_by INT NULL,
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        )'
    );
}

function dsm_add_column_if_missing(PDO $pdo, string $table, string $column, string $definition): void
{
    $driver = (string) $pdo->getAttribute(PDO::ATTR_DRIVER_NAME);
    if ($driver === 'sqlite') {
        $stmt = $pdo->query('PRAGMA table_info(' . $table . ')');
        foreach ($stmt->fetchAll() as $row) {
            if (($row['name'] ?? '') === $column) {
                return;
            }
        }
    } else {
        $stmt = $pdo->prepare('SHOW COLUMNS FROM ' . $table . ' LIKE :column');
        $stmt->execute(['column' => $column]);
        if ($stmt->fetch()) {
            return;
        }
    }

    $pdo->exec('ALTER TABLE ' . $table . ' ADD COLUMN ' . $column . ' ' . $definition);
}

function dsm_ensure_decimal_score_columns(PDO $pdo): void
{
    $driver = (string) $pdo->getAttribute(PDO::ATTR_DRIVER_NAME);
    if ($driver === 'sqlite') {
        return;
    }

    foreach (['score', 'max_score'] as $column) {
        $stmt = $pdo->prepare('SHOW COLUMNS FROM quiz_attempts LIKE :column');
        $stmt->execute(['column' => $column]);
        $info = $stmt->fetch();
        $type = strtolower((string) ($info['Type'] ?? ''));
        if (strpos($type, 'decimal') === 0) {
            continue;
        }

        $pdo->exec('ALTER TABLE quiz_attempts MODIFY ' . $column . ' DECIMAL(6,2) NOT NULL');
    }
}

function dsm_migrate_assignment_aliases(PDO $pdo): void
{
    $stmt = $pdo->prepare('UPDATE quiz_attempts SET quiz_id = :canonical_id WHERE quiz_id = :legacy_id');

    foreach (dsm_assignment_aliases() as $legacyId => $canonicalId) {
        $stmt->execute([
            'legacy_id' => $legacyId,
            'canonical_id' => $canonicalId,
        ]);
    }
}

function dsm_record_login_event(PDO $pdo, int $userId, string $authSource): void
{
    $pdo->prepare(
        'INSERT INTO login_events (user_id, auth_source, ip_address, user_agent)
         VALUES (:user_id, :auth_source, :ip_address, :user_agent)'
    )->execute([
        'user_id' => $userId,
        'auth_source' => $authSource,
        'ip_address' => $_SERVER['REMOTE_ADDR'] ?? null,
        'user_agent' => $_SERVER['HTTP_USER_AGENT'] ?? null,
    ]);
}

function dsm_seed_admins(PDO $pdo, array $config): void
{
    foreach (($config['auth']['bootstrap_admins'] ?? []) as $admin) {
        $email = trim((string) ($admin['email'] ?? ''));
        $passwordHash = (string) ($admin['password_hash'] ?? '');
        if ($email === '' || $passwordHash === '') {
            continue;
        }

        $stmt = $pdo->prepare('SELECT id FROM quiz_users WHERE LOWER(email) = LOWER(:email) LIMIT 1');
        $stmt->execute(['email' => $email]);
        if ($stmt->fetch()) {
            continue;
        }

        $insert = $pdo->prepare(
            'INSERT INTO quiz_users (email, display_name, role, password_hash, status, canvas_user_id)
             VALUES (:email, :display_name, \'admin\', :password_hash, \'active\', :canvas_user_id)'
        );
        $insert->execute([
            'email' => $email,
            'display_name' => $admin['display_name'] ?? $email,
            'password_hash' => $passwordHash,
            'canvas_user_id' => $admin['canvas_user_id'] ?? null,
        ]);
    }
}

function dsm_normalize_student_identifier(?string $identifier): string
{
    $identifier = strtolower(trim((string) $identifier));
    return preg_replace('/@.*$/', '', $identifier) ?? $identifier;
}

function dsm_seed_course_students(PDO $pdo, array $config): void
{
    $students = [];
    foreach (($config['course']['students'] ?? []) as $student) {
        if (is_array($student)) {
            $students[] = $student;
        }
    }

    foreach (($config['course']['allowed_student_identifiers'] ?? []) as $identifier) {
        $students[] = ['student_identifier' => (string) $identifier];
    }

    foreach ($students as $student) {
        $identifier = dsm_normalize_student_identifier((string) ($student['student_identifier'] ?? $student['sis_login_id'] ?? ''));
        if ($identifier === '') {
            continue;
        }

        $email = trim((string) ($student['email'] ?? ''));
        $displayName = trim((string) ($student['display_name'] ?? $student['name'] ?? ''));
        $passwordHash = (string) ($student['password_hash'] ?? '');

        $stmt = $pdo->prepare(
            'SELECT id FROM quiz_users
             WHERE LOWER(student_identifier) = LOWER(:student_identifier)
                OR LOWER(email) = LOWER(:email)
             LIMIT 1'
        );
        $stmt->execute([
            'student_identifier' => $identifier,
            'email' => $email !== '' ? $email : $identifier . '@student.local',
        ]);
        $existing = $stmt->fetch();

        if (is_array($existing)) {
            $sql = 'UPDATE quiz_users
                    SET student_identifier = :student_identifier,
                        role = \'student\',
                        status = \'active\'';
            $params = [
                'student_identifier' => $identifier,
                'id' => (int) $existing['id'],
            ];
            if ($displayName !== '') {
                $sql .= ', display_name = :display_name';
                $params['display_name'] = $displayName;
            }
            if ($email !== '') {
                $sql .= ', email = :email';
                $params['email'] = $email;
            }
            if ($passwordHash !== '') {
                $sql .= ', password_hash = :password_hash';
                $params['password_hash'] = $passwordHash;
            }
            $sql .= ' WHERE id = :id';
            $pdo->prepare($sql)->execute($params);
            continue;
        }

        $insert = $pdo->prepare(
            'INSERT INTO quiz_users (email, display_name, role, password_hash, status, canvas_user_id, student_identifier)
             VALUES (:email, :display_name, \'student\', :password_hash, \'active\', NULL, :student_identifier)'
        );
        $insert->execute([
            'email' => $email !== '' ? $email : $identifier . '@student.local',
            'display_name' => $displayName !== '' ? $displayName : $identifier,
            'password_hash' => $passwordHash !== '' ? $passwordHash : null,
            'student_identifier' => $identifier,
        ]);
    }
}

function dsm_database_ready(array $config): PDO
{
    $pdo = dsm_connect_database($config['database']);
    dsm_initialize_schema($pdo);
    dsm_seed_admins($pdo, $config);
    dsm_seed_course_students($pdo, $config);
    dsm_seed_assignment_settings($pdo);
    return $pdo;
}

function dsm_assignment_aliases(): array
{
    return [
        'preview02' => 'ch02-preview',
        'lab02' => 'ch02-lab',
        'homework02' => 'ch02-homework',
    ];
}

function dsm_canonical_assignment_id(string $assignmentId): string
{
    return dsm_assignment_aliases()[$assignmentId] ?? $assignmentId;
}

function dsm_assignment_query_ids(string $assignmentId): array
{
    $canonicalId = dsm_canonical_assignment_id($assignmentId);
    $ids = [$canonicalId];

    foreach (dsm_assignment_aliases() as $legacyId => $targetId) {
        if ($targetId === $canonicalId) {
            $ids[] = $legacyId;
        }
    }

    return array_values(array_unique($ids));
}

function dsm_assignment_id_filter(string $assignmentId, string $prefix): array
{
    $params = [];
    $placeholders = [];

    foreach (dsm_assignment_query_ids($assignmentId) as $index => $id) {
        $param = $prefix . $index;
        $params[$param] = $id;
        $placeholders[] = ':' . $param;
    }

    return [
        'sql' => implode(', ', $placeholders),
        'params' => $params,
    ];
}

function dsm_quiz_definition(string $quizId): ?array
{
    $quizId = dsm_canonical_assignment_id($quizId);

    $quizzes = [
        'ch01-preview' => [
            'chapter' => '01-intro',
            'assignment_slug' => 'preview',
            'max_score' => 10,
            'canvas_assignment_column' => 'ch01-preview',
            'questions' => [
                'q1' => 'A',
                'q2' => 'B',
                'q3' => 'A',
                'q4' => 'B',
                'q5' => 'C',
                'q6' => 'A',
                'q7' => 'B',
                'q8' => 'A',
                'q9' => 'A',
                'q10' => 'C',
                'q11' => 'A',
                'q12' => 'B',
            ],
        ],
        'ch02-preview' => [
            'chapter' => '02-python',
            'assignment_slug' => 'preview',
            'max_score' => 10,
            'canvas_assignment_column' => 'ch02-preview',
            'questions' => [
                'q1' => 'A',
                'q2' => 'B',
                'q3' => 'C',
                'q4' => 'A',
                'q5' => 'B',
                'q6' => 'B',
                'q7' => 'B',
                'q8' => 'A',
                'q9' => 'A',
                'q10' => 'D',
            ],
        ],
        'ch04-preview' => [
            'chapter' => '04-pandas',
            'assignment_slug' => 'preview',
            'max_score' => 10,
            'canvas_assignment_column' => 'ch04-preview',
            'questions' => [
                'q1' => 'A',
                'q2' => 'B',
                'q3' => 'C',
                'q4' => 'C',
                'q5' => 'B',
                'q6' => 'D',
                'q7' => 'A',
                'q8' => 'C',
                'q9' => 'B',
                'q10' => 'B',
            ],
        ],
        'ch03-preview' => [
            'chapter' => '03-numpy',
            'assignment_slug' => 'preview',
            'max_score' => 10,
            'canvas_assignment_column' => 'ch03-preview',
            'questions' => [
                'q1' => 'A',
                'q2' => 'B',
                'q3' => 'C',
                'q4' => 'D',
                'q5' => 'A',
                'q6' => 'B',
                'q7' => 'C',
                'q8' => 'D',
                'q9' => 'A',
                'q10' => 'B',
            ],
        ],
        'ch05-preview' => [
            'chapter' => '05-visualization',
            'assignment_slug' => 'preview',
            'max_score' => 10,
            'canvas_assignment_column' => 'ch05-preview',
            'questions' => [
                'q1' => 'A',
                'q2' => 'B',
                'q3' => 'C',
                'q4' => 'D',
                'q5' => 'A',
                'q6' => 'B',
                'q7' => 'C',
                'q8' => 'D',
                'q9' => 'A',
                'q10' => 'B',
            ],
        ],
        'ch06-preview' => [
            'chapter' => '06-matplotlib',
            'assignment_slug' => 'preview',
            'max_score' => 10,
            'canvas_assignment_column' => 'ch06-preview',
            'questions' => [
                'q1' => 'A',
                'q2' => 'B',
                'q3' => 'C',
                'q4' => 'D',
                'q5' => 'A',
                'q6' => 'B',
                'q7' => 'C',
                'q8' => 'D',
                'q9' => 'A',
                'q10' => 'B',
            ],
        ],
        'ch07-preview' => [
            'chapter' => '07-seaborn',
            'assignment_slug' => 'preview',
            'max_score' => 10,
            'canvas_assignment_column' => 'ch07-preview',
            'questions' => [
                'q1' => 'A',
                'q2' => 'B',
                'q3' => 'C',
                'q4' => 'D',
                'q5' => 'A',
                'q6' => 'B',
                'q7' => 'C',
                'q8' => 'D',
                'q9' => 'A',
                'q10' => 'B',
            ],
        ],
        'ch08-preview' => [
            'chapter' => '08-prob-stats',
            'assignment_slug' => 'preview',
            'max_score' => 10,
            'canvas_assignment_column' => 'ch08-preview',
            'questions' => [
                'q1' => 'A',
                'q2' => 'B',
                'q3' => 'C',
                'q4' => 'D',
                'q5' => 'A',
                'q6' => 'B',
                'q7' => 'C',
                'q8' => 'D',
                'q9' => 'A',
                'q10' => 'B',
            ],
        ],
        'ch09-preview' => [
            'chapter' => '09-test-hypothesis',
            'assignment_slug' => 'preview',
            'max_score' => 10,
            'canvas_assignment_column' => 'ch09-preview',
            'questions' => [
                'q1' => 'A',
                'q2' => 'B',
                'q3' => 'C',
                'q4' => 'D',
                'q5' => 'A',
                'q6' => 'B',
                'q7' => 'C',
                'q8' => 'D',
                'q9' => 'A',
                'q10' => 'B',
            ],
        ],
        'ch10-preview' => [
            'chapter' => '10-two-samples',
            'assignment_slug' => 'preview',
            'max_score' => 10,
            'canvas_assignment_column' => 'ch10-preview',
            'questions' => [
                'q1' => 'A',
                'q2' => 'B',
                'q3' => 'C',
                'q4' => 'D',
                'q5' => 'A',
                'q6' => 'B',
                'q7' => 'C',
                'q8' => 'D',
                'q9' => 'A',
                'q10' => 'B',
            ],
        ],
        'ch11-preview' => [
            'chapter' => '11-estimation',
            'assignment_slug' => 'preview',
            'max_score' => 10,
            'canvas_assignment_column' => 'ch11-preview',
            'questions' => [
                'q1' => 'A',
                'q2' => 'B',
                'q3' => 'C',
                'q4' => 'D',
                'q5' => 'A',
                'q6' => 'B',
                'q7' => 'C',
                'q8' => 'D',
                'q9' => 'A',
                'q10' => 'B',
            ],
        ],
        'ch12-preview' => [
            'chapter' => '12-regression',
            'assignment_slug' => 'preview',
            'max_score' => 10,
            'canvas_assignment_column' => 'ch12-preview',
            'questions' => [
                'q1' => 'A',
                'q2' => 'B',
                'q3' => 'C',
                'q4' => 'D',
                'q5' => 'A',
                'q6' => 'B',
                'q7' => 'C',
                'q8' => 'D',
                'q9' => 'A',
                'q10' => 'B',
            ],
        ],
        'ch13-preview' => [
            'chapter' => '13-multiple-regression',
            'assignment_slug' => 'preview',
            'max_score' => 10,
            'canvas_assignment_column' => 'ch13-preview',
            'questions' => [
                'q1' => 'A',
                'q2' => 'B',
                'q3' => 'C',
                'q4' => 'D',
                'q5' => 'A',
                'q6' => 'B',
                'q7' => 'C',
                'q8' => 'D',
                'q9' => 'A',
                'q10' => 'B',
            ],
        ],
        'ch14-preview' => [
            'chapter' => '14-classification',
            'assignment_slug' => 'preview',
            'max_score' => 10,
            'canvas_assignment_column' => 'ch14-preview',
            'questions' => [
                'q1' => 'A',
                'q2' => 'B',
                'q3' => 'C',
                'q4' => 'D',
                'q5' => 'A',
                'q6' => 'B',
                'q7' => 'C',
                'q8' => 'D',
                'q9' => 'A',
                'q10' => 'B',
            ],
        ],
        'ch15-preview' => [
            'chapter' => '15-clustering',
            'assignment_slug' => 'preview',
            'max_score' => 10,
            'canvas_assignment_column' => 'ch15-preview',
            'questions' => [
                'q1' => 'A',
                'q2' => 'B',
                'q3' => 'C',
                'q4' => 'D',
                'q5' => 'A',
                'q6' => 'B',
                'q7' => 'C',
                'q8' => 'D',
                'q9' => 'A',
                'q10' => 'B',
            ],
        ],
    ];

    return $quizzes[$quizId] ?? null;
}

function dsm_lab_definition(string $labId): ?array
{
    $labId = dsm_canonical_assignment_id($labId);

    $labs = [
        'ch01-lab' => [
            'chapter' => '01-intro',
            'assignment_slug' => 'lab',
            'max_score' => 10,
            'canvas_assignment_column' => 'ch01-lab',
        ],
        'ch02-lab' => [
            'chapter' => '02-python',
            'assignment_slug' => 'lab',
            'max_score' => 10,
            'canvas_assignment_column' => 'ch02-lab',
            'code_outputs' => [
                'q1' => 'Subtotal: 180
Discount: 18.0
Final total: 162.0',
                'q2' => 'Decision: Reorder',
                'q3' => 'High sales: [340, 410]
First high sale: 340',
                'q4' => 'Sales count: 3
HR count: 1',
                'q5' => 'Margin: 375',
            ],
        ],
        'ch03-lab' => [
            'chapter' => '03-numpy',
            'assignment_slug' => 'lab',
            'max_score' => 10,
            'canvas_assignment_column' => 'ch03-lab',
            'code_outputs' => [
                'q1' => 'Rows: 3
Columns: 4
Values: 12',
                'q2' => 'Adjusted prices: [13, 17, 21, 25]',
                'q3' => 'Selected sales: [120, 135, 150]',
                'q4' => 'Squared errors: [4, 1, 9, 16]
Total squared error: 30',
                'q5' => 'Sample size: 5
Sample mean: 42.0',
            ],
        ],
        'ch04-lab' => [
            'chapter' => '04-pandas',
            'assignment_slug' => 'lab',
            'max_score' => 10,
            'canvas_assignment_column' => 'ch04-lab',
            'runner_profile' => 'pandas',
            'code_outputs' => [
                'q1' => 'Rows: 4
Columns: 2',
                'q2' => 'B score: 91
First score: 82',
                'q3' => 'Missing sales: 1
Filled total: 215',
                'q4' => 'High regions: [\'North\', \'East\']
Top revenue: 1400',
                'q5' => 'East total: 250
West total: 200',
            ],
        ],
        'ch05-lab' => [
            'chapter' => '05-visualization',
            'assignment_slug' => 'lab',
            'max_score' => 10,
            'canvas_assignment_column' => 'ch05-lab',
            'code_outputs' => [
                'q1' => 'Trend chart: line
Comparison chart: bar
Relationship chart: scatter',
                'q2' => 'First point: Jan 120
Last point: Mar 150',
                'q3' => 'Low: 2
Medium: 4
High: 2',
                'q4' => 'Chart title: Sales by Region
First label: East: 240',
                'q5' => 'Regular count: 5
Outliers: [210]',
            ],
        ],
        'ch06-lab' => [
            'chapter' => '06-matplotlib',
            'assignment_slug' => 'lab',
            'max_score' => 10,
            'canvas_assignment_column' => 'ch06-lab',
            'code_outputs' => [
                'q1' => 'X values: [1, 2, 3, 4]
Y values: [20, 24, 23, 29]',
                'q2' => 'Title: Quarterly Revenue
X label: Quarter
Y label: Revenue',
                'q3' => 'Rows: 2
Columns: 2
Axes: 4',
                'q4' => 'Trend: line
Groups: bar
Relationship: scatter
Distribution: hist',
                'q5' => 'Filename: regional_margin_q2.png',
            ],
        ],
        'ch07-lab' => [
            'chapter' => '07-seaborn',
            'assignment_slug' => 'lab',
            'max_score' => 10,
            'canvas_assignment_column' => 'ch07-lab',
            'code_outputs' => [
                'q1' => 'Observations: 5
Variables: 3',
                'q2' => 'Retail: 3
Online: 2',
                'q3' => 'Facets: [\'East\', \'North\', \'West\']
Facet count: 3',
                'q4' => 'Basic mean: 7.0
Premium mean: 9.0',
                'q5' => 'X variable: ad_spend
Y variable: revenue
Hue variable: region',
            ],
        ],
        'ch08-lab' => [
            'chapter' => '08-prob-stats',
            'assignment_slug' => 'lab',
            'max_score' => 10,
            'canvas_assignment_column' => 'ch08-lab',
            'code_outputs' => [
                'q1' => 'Delay probability: 0.15',
                'q2' => 'Expected sales: 155.0',
                'q3' => 'Mean wait: 6.0
Median wait: 5',
                'q4' => 'Renewed proportion: 0.6',
                'q5' => 'Sample A mean: 12.0
Sample B mean: 15.0
Difference: 3.0',
            ],
        ],
        'ch09-lab' => [
            'chapter' => '09-test-hypothesis',
            'assignment_slug' => 'lab',
            'max_score' => 10,
            'canvas_assignment_column' => 'ch09-lab',
            'code_outputs' => [
                'q1' => 'Observed difference: 8',
                'q2' => 'Total distance: 0.04',
                'q3' => 'Extreme simulations: 2',
                'q4' => 'P-value: 0.4',
                'q5' => 'Decision: strong evidence',
            ],
        ],
        'ch10-lab' => [
            'chapter' => '10-two-samples',
            'assignment_slug' => 'lab',
            'max_score' => 10,
            'canvas_assignment_column' => 'ch10-lab',
            'code_outputs' => [
                'q1' => 'Treatment mean: 114.0
Control mean: 100.0',
                'q2' => 'Lift: 14.0',
                'q3' => 'Version A rate: 0.1
Version B rate: 0.14',
                'q4' => 'Extreme differences: 2',
                'q5' => 'Conditions met: 2
Ready for causal claim: False',
            ],
        ],
        'ch11-lab' => [
            'chapter' => '11-estimation',
            'assignment_slug' => 'lab',
            'max_score' => 10,
            'canvas_assignment_column' => 'ch11-lab',
            'code_outputs' => [
                'q1' => '75th percentile: 88',
                'q2' => 'Estimate: 52.0',
                'q3' => 'Bootstrap median: 42',
                'q4' => 'Interval width: 8',
                'q5' => 'Metric: average order value
Lower: 42
Upper: 58',
            ],
        ],
        'ch12-lab' => [
            'chapter' => '12-regression',
            'assignment_slug' => 'lab',
            'max_score' => 10,
            'canvas_assignment_column' => 'ch12-lab',
            'code_outputs' => [
                'q1' => 'Predicted sales: 155',
                'q2' => 'Residual: 7',
                'q3' => 'Squared residuals: [4, 1, 9]
SSE: 14',
                'q4' => 'Direction: negative',
                'q5' => 'First absolute residual: 2
Last absolute residual: 9
Pattern flag: True',
            ],
        ],
        'ch13-lab' => [
            'chapter' => '13-multiple-regression',
            'assignment_slug' => 'lab',
            'max_score' => 10,
            'canvas_assignment_column' => 'ch13-lab',
            'code_outputs' => [
                'q1' => 'Predicted price: 320',
                'q2' => 'Added room effect: 30',
                'q3' => 'Train rows: 4
Test rows: 2',
                'q4' => 'Best model: multiple',
                'q5' => 'Scaled size: 2.4',
            ],
        ],
        'ch14-lab' => [
            'chapter' => '14-classification',
            'assignment_slug' => 'lab',
            'max_score' => 10,
            'canvas_assignment_column' => 'ch14-lab',
            'code_outputs' => [
                'q1' => 'Features: [42, 3]
Label: renew',
                'q2' => 'Squared distance: 25',
                'q3' => 'Accuracy: 0.75',
                'q4' => 'True positives: 2
False positives: 1',
                'q5' => 'Predicted class: low risk',
            ],
        ],
        'ch15-lab' => [
            'chapter' => '15-clustering',
            'assignment_slug' => 'lab',
            'max_score' => 10,
            'canvas_assignment_column' => 'ch15-lab',
            'code_outputs' => [
                'q1' => 'Distance to A: 5
Distance to B: 13',
                'q2' => 'Assigned cluster: A',
                'q3' => 'New center: 12.0',
                'q4' => 'Elbow k: 4',
                'q5' => 'Cluster A: 3
Cluster B: 2',
            ],
        ],
    ];

    return $labs[$labId] ?? null;
}

function dsm_homework_definition(string $homeworkId): ?array
{
    $homeworkId = dsm_canonical_assignment_id($homeworkId);

    $homework = [
        'ch01-homework' => [
            'chapter' => '01-intro',
            'assignment_slug' => 'homework',
            'max_score' => 10,
            'canvas_assignment_column' => 'ch01-homework',
            'true_false' => [
                'q1' => true,
                'q2' => false,
                'q3' => true,
                'q4' => false,
                'q5' => false,
            ],
            'code_outputs' => [
                'q6' => 'Question A: descriptive
Question B: predictive
Question C: prescriptive',
                'q7' => 'North store has 7 late shipments out of 80.',
                'q8' => 'DSM homework
Syntax fixed.',
                'q9' => 'Inventory code: R-82-0x2d',
                'q10' => 'Open cases: 17
Closure rate: 0.67',
            ],
        ],
        'ch02-homework' => [
            'chapter' => '02-python',
            'assignment_slug' => 'homework',
            'max_score' => 10,
            'canvas_assignment_column' => 'ch02-homework',
            'true_false' => [
                'q1' => true,
                'q2' => false,
                'q3' => true,
                'q4' => true,
                'q5' => false,
            ],
            'code_outputs' => [
                'q6' => 'East profit: 375',
                'q7' => 'Segment: medium',
                'q8' => 'Days counted: 2
Customers before closing: 80',
                'q9' => 'Software purchases: 3
Service purchases: 2',
                'q10' => 'Revenue per employee: 250.0',
            ],
        ],
        'ch03-homework' => [
            'chapter' => '03-numpy',
            'assignment_slug' => 'homework',
            'max_score' => 10,
            'canvas_assignment_column' => 'ch03-homework',
            'true_false' => [
                'q1' => true,
                'q2' => true,
                'q3' => false,
                'q4' => true,
                'q5' => false,
            ],
            'code_outputs' => [
                'q6' => 'Week 1 total: 42
Week 2 total: 47',
                'q7' => 'Final prices: [90, 135, 180]',
                'q8' => 'Recent demand: [32, 35, 37]',
                'q9' => 'Met target: [False, True, True, False]',
                'q10' => 'Average simulated demand: 51.0',
            ],
        ],
        'ch04-homework' => [
            'chapter' => '04-pandas',
            'assignment_slug' => 'homework',
            'max_score' => 10,
            'canvas_assignment_column' => 'ch04-homework',
            'runner_profile' => 'pandas',
            'true_false' => [
                'q1' => true,
                'q2' => false,
                'q3' => true,
                'q4' => true,
                'q5' => false,
            ],
            'code_outputs' => [
                'q6' => 'Customer rows: 3
Purchase total: 12',
                'q7' => 'Average order: 35.0',
                'q8' => 'West revenue: 900
First region: East',
                'q9' => 'Missing ratings: 1
Rating total: 8',
                'q10' => 'Matched rows: 2
Pen price: 2.5',
            ],
        ],
        'ch05-homework' => [
            'chapter' => '05-visualization',
            'assignment_slug' => 'homework',
            'max_score' => 10,
            'canvas_assignment_column' => 'ch05-homework',
            'true_false' => [
                'q1' => true,
                'q2' => true,
                'q3' => false,
                'q4' => true,
                'q5' => false,
            ],
            'code_outputs' => [
                'q6' => 'Bar charts: 2
Line charts: 1',
                'q7' => 'Minimum sales: 80
Maximum sales: 140',
                'q8' => 'First pair: [10, 80]
Pair count: 3',
                'q9' => 'Colors: [\'gray\', \'red\', \'gray\']',
                'q10' => 'Scale warning: True',
            ],
        ],
        'ch06-homework' => [
            'chapter' => '06-matplotlib',
            'assignment_slug' => 'homework',
            'max_score' => 10,
            'canvas_assignment_column' => 'ch06-homework',
            'true_false' => [
                'q1' => true,
                'q2' => true,
                'q3' => false,
                'q4' => true,
                'q5' => false,
            ],
            'code_outputs' => [
                'q6' => 'Figure area: 24',
                'q7' => 'Legend labels: [\'North\', \'South\']',
                'q8' => 'Pixel width: 600',
                'q9' => 'Forecast style: dashed',
                'q10' => 'Axis titles: [\'Revenue\', \'Margin\']',
            ],
        ],
        'ch07-homework' => [
            'chapter' => '07-seaborn',
            'assignment_slug' => 'homework',
            'max_score' => 10,
            'canvas_assignment_column' => 'ch07-homework',
            'true_false' => [
                'q1' => true,
                'q2' => true,
                'q3' => false,
                'q4' => true,
                'q5' => false,
            ],
            'code_outputs' => [
                'q6' => 'Long rows: 4',
                'q7' => 'X: discount
Y: sales',
                'q8' => 'Average rating: 4.0',
                'q9' => 'Facet count: 3',
                'q10' => 'Heatmap cells: 12',
            ],
        ],
        'ch08-homework' => [
            'chapter' => '08-prob-stats',
            'assignment_slug' => 'homework',
            'max_score' => 10,
            'canvas_assignment_column' => 'ch08-homework',
            'true_false' => [
                'q1' => true,
                'q2' => true,
                'q3' => true,
                'q4' => false,
                'q5' => false,
            ],
            'code_outputs' => [
                'q6' => 'On-time probability: 0.85',
                'q7' => 'Wait range: 9',
                'q8' => 'Mean sales: 30.0
Above mean: 1',
                'q9' => 'Empirical probability: 0.5',
                'q10' => 'Larger sample has smaller SE: True',
            ],
        ],
        'ch09-homework' => [
            'chapter' => '09-test-hypothesis',
            'assignment_slug' => 'homework',
            'max_score' => 10,
            'canvas_assignment_column' => 'ch09-homework',
            'true_false' => [
                'q1' => true,
                'q2' => true,
                'q3' => false,
                'q4' => true,
                'q5' => false,
            ],
            'code_outputs' => [
                'q6' => 'Test statistic: 6',
                'q7' => 'Tail count: 3',
                'q8' => 'Evidence: weak',
                'q9' => 'Distance: 0.1',
                'q10' => 'Reject null: True',
            ],
        ],
        'ch10-homework' => [
            'chapter' => '10-two-samples',
            'assignment_slug' => 'homework',
            'max_score' => 10,
            'canvas_assignment_column' => 'ch10-homework',
            'true_false' => [
                'q1' => true,
                'q2' => true,
                'q3' => true,
                'q4' => false,
                'q5' => false,
            ],
            'code_outputs' => [
                'q6' => 'Difference: 12.0',
                'q7' => 'Lift percent: 20.0',
                'q8' => 'Treatment labels: 3',
                'q9' => 'Tail rate: 0.25',
                'q10' => 'RCT ready: True',
            ],
        ],
        'ch11-homework' => [
            'chapter' => '11-estimation',
            'assignment_slug' => 'homework',
            'max_score' => 10,
            'canvas_assignment_column' => 'ch11-homework',
            'true_false' => [
                'q1' => true,
                'q2' => true,
                'q3' => true,
                'q4' => false,
                'q5' => false,
            ],
            'code_outputs' => [
                'q6' => 'Median: 72',
                'q7' => 'Bootstrap mean: 20.0',
                'q8' => 'Interval midpoint: 50.0',
                'q9' => '25th percentile: 12',
                'q10' => 'Estimate range: 44 to 56',
            ],
        ],
        'ch12-homework' => [
            'chapter' => '12-regression',
            'assignment_slug' => 'homework',
            'max_score' => 10,
            'canvas_assignment_column' => 'ch12-homework',
            'true_false' => [
                'q1' => true,
                'q2' => true,
                'q3' => true,
                'q4' => false,
                'q5' => false,
            ],
            'code_outputs' => [
                'q6' => 'Predicted demand: 70',
                'q7' => 'Residuals: [2, -1, 3]',
                'q8' => 'MSE: 4.0',
                'q9' => 'Outlier flag: True',
                'q10' => 'Strength: strong',
            ],
        ],
        'ch13-homework' => [
            'chapter' => '13-multiple-regression',
            'assignment_slug' => 'homework',
            'max_score' => 10,
            'canvas_assignment_column' => 'ch13-homework',
            'true_false' => [
                'q1' => true,
                'q2' => true,
                'q3' => true,
                'q4' => false,
                'q5' => false,
            ],
            'code_outputs' => [
                'q6' => 'Predicted revenue: 510',
                'q7' => 'Larger coefficient: service_score',
                'q8' => 'Selected model: model_b',
                'q9' => 'Feature count: 3',
                'q10' => 'Average absolute error: 5.0',
            ],
        ],
        'ch14-homework' => [
            'chapter' => '14-classification',
            'assignment_slug' => 'homework',
            'max_score' => 10,
            'canvas_assignment_column' => 'ch14-homework',
            'true_false' => [
                'q1' => true,
                'q2' => true,
                'q3' => true,
                'q4' => false,
                'q5' => false,
            ],
            'code_outputs' => [
                'q6' => 'Churn predictions: 2',
                'q7' => 'Nearest label: approve',
                'q8' => 'Correct predictions: 3',
                'q9' => 'Distance score: 20',
                'q10' => 'Training rows: 3
Test rows: 2',
            ],
        ],
        'ch15-homework' => [
            'chapter' => '15-clustering',
            'assignment_slug' => 'homework',
            'max_score' => 10,
            'canvas_assignment_column' => 'ch15-homework',
            'true_false' => [
                'q1' => true,
                'q2' => true,
                'q3' => true,
                'q4' => false,
                'q5' => false,
            ],
            'code_outputs' => [
                'q6' => 'Cluster count: 3',
                'q7' => 'Nearest center: B',
                'q8' => 'Scaled spending: 4.5',
                'q9' => 'Cluster average: 18.0',
                'q10' => 'Best k: 3',
            ],
        ],
    ];

    return $homework[$homeworkId] ?? null;
}

function dsm_assignment_definition(string $assignmentId): ?array
{
    return dsm_quiz_definition($assignmentId)
        ?? dsm_lab_definition($assignmentId)
        ?? dsm_homework_definition($assignmentId);
}

function dsm_all_assignment_definitions(): array
{
    $assignmentIds = ['ch01-preview', 'ch01-lab', 'ch01-homework', 'ch02-preview', 'ch02-lab', 'ch02-homework', 'ch03-preview', 'ch03-lab', 'ch03-homework', 'ch04-preview', 'ch04-lab', 'ch04-homework', 'ch05-preview', 'ch05-lab', 'ch05-homework', 'ch06-preview', 'ch06-lab', 'ch06-homework', 'ch07-preview', 'ch07-lab', 'ch07-homework', 'ch08-preview', 'ch08-lab', 'ch08-homework', 'ch09-preview', 'ch09-lab', 'ch09-homework', 'ch10-preview', 'ch10-lab', 'ch10-homework', 'ch11-preview', 'ch11-lab', 'ch11-homework', 'ch12-preview', 'ch12-lab', 'ch12-homework', 'ch13-preview', 'ch13-lab', 'ch13-homework', 'ch14-preview', 'ch14-lab', 'ch14-homework', 'ch15-preview', 'ch15-lab', 'ch15-homework'];
    $assignments = [];
    foreach ($assignmentIds as $assignmentId) {
        $definition = dsm_assignment_definition($assignmentId);
        if ($definition === null) {
            continue;
        }
        $assignments[$assignmentId] = $definition;
    }
    return $assignments;
}

function dsm_seed_assignment_settings(PDO $pdo): void
{
    foreach (dsm_all_assignment_definitions() as $assignmentId => $definition) {
        $defaultUnlocked = ($definition['assignment_slug'] ?? '') === 'lab' && $assignmentId === 'ch01-lab' ? 1 : 0;
        $stmt = $pdo->prepare('SELECT assignment_id FROM assignment_settings WHERE assignment_id = :assignment_id LIMIT 1');
        $stmt->execute(['assignment_id' => $assignmentId]);
        if ($stmt->fetch()) {
            continue;
        }

        $insert = $pdo->prepare(
            'INSERT INTO assignment_settings (assignment_id, answers_unlocked)
             VALUES (:assignment_id, :answers_unlocked)'
        );
        $insert->execute([
            'assignment_id' => $assignmentId,
            'answers_unlocked' => $defaultUnlocked,
        ]);
    }
}

function dsm_list_assignment_settings(PDO $pdo): array
{
    $settings = [];
    $stmt = $pdo->query(
        'SELECT assignment_id, answers_unlocked, updated_by, updated_at
         FROM assignment_settings'
    );
    foreach ($stmt->fetchAll() as $row) {
        $settings[(string) $row['assignment_id']] = $row;
    }

    $rows = [];
    foreach (dsm_all_assignment_definitions() as $assignmentId => $definition) {
        $setting = $settings[$assignmentId] ?? [
            'assignment_id' => $assignmentId,
            'answers_unlocked' => 0,
            'updated_by' => null,
            'updated_at' => null,
        ];
        $rows[] = $setting + [
            'chapter' => $definition['chapter'] ?? '',
            'assignment_slug' => $definition['assignment_slug'] ?? '',
            'max_score' => $definition['max_score'] ?? '',
            'canvas_assignment_column' => $definition['canvas_assignment_column'] ?? '',
        ];
    }

    return $rows;
}

function dsm_assignment_answers_unlocked(PDO $pdo, string $assignmentId): bool
{
    if (dsm_assignment_definition($assignmentId) === null) {
        return false;
    }

    $stmt = $pdo->prepare(
        'SELECT answers_unlocked
         FROM assignment_settings
         WHERE assignment_id = :assignment_id
         LIMIT 1'
    );
    $stmt->execute(['assignment_id' => $assignmentId]);
    $row = $stmt->fetch();
    return is_array($row) && (int) ($row['answers_unlocked'] ?? 0) === 1;
}

function dsm_update_assignment_answer_lock(PDO $pdo, string $assignmentId, bool $answersUnlocked, int $adminUserId): void
{
    if (dsm_assignment_definition($assignmentId) === null) {
        throw new RuntimeException('Unknown assignment.');
    }

    $driver = (string) $pdo->getAttribute(PDO::ATTR_DRIVER_NAME);
    if ($driver === 'sqlite') {
        $stmt = $pdo->prepare(
            'INSERT INTO assignment_settings (assignment_id, answers_unlocked, updated_by, updated_at)
             VALUES (:assignment_id, :answers_unlocked, :updated_by, CURRENT_TIMESTAMP)
             ON CONFLICT(assignment_id) DO UPDATE SET
                answers_unlocked = excluded.answers_unlocked,
                updated_by = excluded.updated_by,
                updated_at = CURRENT_TIMESTAMP'
        );
    } else {
        $stmt = $pdo->prepare(
            'INSERT INTO assignment_settings (assignment_id, answers_unlocked, updated_by, updated_at)
             VALUES (:assignment_id, :answers_unlocked, :updated_by, CURRENT_TIMESTAMP)
             ON DUPLICATE KEY UPDATE
                answers_unlocked = VALUES(answers_unlocked),
                updated_by = VALUES(updated_by),
                updated_at = CURRENT_TIMESTAMP'
        );
    }
    $stmt->execute([
        'assignment_id' => $assignmentId,
        'answers_unlocked' => $answersUnlocked ? 1 : 0,
        'updated_by' => $adminUserId,
    ]);
}

function dsm_grade_attempt(array $quiz, array $answers): array
{
    $feedback = [];
    $normalizedAnswers = [];
    $correctCount = 0;

    foreach ($quiz['questions'] as $questionKey => $correctAnswer) {
        $submitted = strtoupper(trim((string) ($answers[$questionKey] ?? '')));
        $isCorrect = $submitted === $correctAnswer;
        if ($isCorrect) {
            $correctCount++;
        }

        $normalizedAnswers[$questionKey] = $submitted !== '' ? $submitted : null;
        $feedback[$questionKey] = [
            'correct' => $isCorrect,
            'submitted' => $submitted !== '' ? $submitted : null,
            'message' => $submitted === ''
                ? 'No answer submitted.'
                : ($isCorrect ? 'Correct.' : 'Try again.'),
        ];
    }

    $questionCount = count($quiz['questions']);
    $maxScore = (float) ($quiz['max_score'] ?? $questionCount);
    $score = $questionCount > 0 ? round(($correctCount / $questionCount) * $maxScore, 2) : 0.0;

    return [
        'score' => $score,
        'max_score' => $maxScore,
        'answers' => $normalizedAnswers,
        'feedback' => $feedback,
    ];
}

function dsm_grade_lab_attempt(array $lab, array $answers): array
{
    $normalizedAnswers = [
        'phase_1' => dsm_normalize_lab_string($answers['phase_1'] ?? ''),
        'phase_6' => dsm_normalize_lab_string($answers['phase_6'] ?? ''),
        'data_visualization_tool' => dsm_normalize_lab_string($answers['data_visualization_tool'] ?? ''),
        'manual_binary' => dsm_normalize_lab_binary($answers['manual_binary'] ?? ''),
        'subtotal' => dsm_normalize_lab_string($answers['subtotal'] ?? ''),
        'tax' => dsm_normalize_lab_string($answers['tax'] ?? ''),
        'total' => dsm_normalize_lab_string($answers['total'] ?? ''),
        'c_decimal' => dsm_normalize_lab_string($answers['c_decimal'] ?? ''),
        'c_binary' => dsm_normalize_lab_binary($answers['c_binary'] ?? ''),
        'item_hex' => dsm_normalize_lab_hex($answers['item_hex'] ?? ''),
    ];

    $feedback = [];
    $score = 0.0;

    $q1Score = 0.0;
    $q1Score += dsm_normalize_lab_phrase($normalizedAnswers['phase_1']) === 'business understanding' ? 1.0 : 0.0;
    $q1Score += dsm_normalize_lab_phrase($normalizedAnswers['phase_6']) === 'deployment' ? 1.0 : 0.0;
    $score += $q1Score;
    $feedback['q1'] = dsm_lab_feedback($q1Score, 2.0);

    $visualizationTools = ['matplotlib', 'seaborn', 'plotly'];
    $q2Score = in_array(dsm_normalize_lab_phrase($normalizedAnswers['data_visualization_tool']), $visualizationTools, true) ? 2.0 : 0.0;
    $score += $q2Score;
    $feedback['q2'] = dsm_lab_feedback($q2Score, 2.0);

    $q3Score = in_array($normalizedAnswers['manual_binary'], ['0b1101', '1101'], true) ? 2.0 : 0.0;
    $score += $q3Score;
    $feedback['q3'] = dsm_lab_feedback($q3Score, 2.0);

    $q4Score = 0.0;
    $q4Score += dsm_lab_number_equals($normalizedAnswers['subtotal'], 75.0) ? (2.0 / 3.0) : 0.0;
    $q4Score += dsm_lab_number_equals($normalizedAnswers['tax'], 6.19) ? (2.0 / 3.0) : 0.0;
    $q4Score += dsm_lab_number_equals($normalizedAnswers['total'], 81.19) ? (2.0 / 3.0) : 0.0;
    $score += $q4Score;
    $feedback['q4'] = dsm_lab_feedback($q4Score, 2.0);

    $q5Score = 0.0;
    $q5Score += dsm_lab_number_equals($normalizedAnswers['c_decimal'], 67.0) ? (2.0 / 3.0) : 0.0;
    $q5Score += $normalizedAnswers['c_binary'] === '0b1000011' ? (2.0 / 3.0) : 0.0;
    $q5Score += $normalizedAnswers['item_hex'] === '0x40' ? (2.0 / 3.0) : 0.0;
    $score += $q5Score;
    $feedback['q5'] = dsm_lab_feedback($q5Score, 2.0);

    return [
        'score' => round($score, 2),
        'max_score' => (float) ($lab['max_score'] ?? 10),
        'answers' => $normalizedAnswers,
        'feedback' => $feedback,
    ];
}

function dsm_grade_lab_code_attempt(array $lab, array $codeByQuestion, array $graderConfig = []): array
{
    $expectedOutputs = $lab['code_outputs'] ?? [
        'q1' => "First phase: Business Understanding\nLast phase: Deployment",
        'q2' => "Visualization tool: Matplotlib",
        'q3' => "Manual conversion: 0b1101\nPython check: 0b1101",
        'q4' => "Subtotal: 75.0\nTax: 6.19\nTotal: 81.19",
        'q5' => "C decimal: 67\nC binary: 0b1000011\nItem hex: 0x40",
    ];

    $feedback = [];
    $normalizedCode = [];
    $score = 0.0;

    foreach ($expectedOutputs as $question => $expectedOutput) {
        $code = (string) ($codeByQuestion[$question] ?? '');
        $normalizedCode[$question] = dsm_limit_lab_code($code, (int) ($graderConfig['max_code_bytes'] ?? 12000));
        $runnerConfig = $graderConfig;
        $runnerConfig['runner_profile'] = (string) ($lab['runner_profile'] ?? 'plain_python');
        $run = dsm_run_lab_code_cell($normalizedCode[$question], $runnerConfig);
        $actualOutput = dsm_normalize_lab_output((string) ($run['stdout'] ?? ''));
        $expectedNormalized = dsm_normalize_lab_output($expectedOutput);
        $accepted = !empty($run['ok']) && $actualOutput === $expectedNormalized;
        $itemScore = $accepted ? 2.0 : 0.0;
        $score += $itemScore;

        $message = $accepted ? 'Accepted.' : 'Output did not match.';
        if (empty($run['ok']) && !empty($run['error'])) {
            $message = (string) $run['error'];
        }

        $feedback[$question] = [
            'correct' => $accepted,
            'score' => $itemScore,
            'max_score' => 2.0,
            'message' => $message,
            'stdout' => $actualOutput,
            'stderr' => dsm_limit_lab_code((string) ($run['stderr'] ?? ''), 2000),
        ];
    }

    return [
        'score' => round($score, 2),
        'max_score' => (float) ($lab['max_score'] ?? 10),
        'answers' => ['code' => $normalizedCode],
        'feedback' => $feedback,
    ];
}

function dsm_grade_homework_attempt(array $homework, array $answers, array $codeByQuestion, array $graderConfig = []): array
{
    $feedback = [];
    $normalizedAnswers = [];
    $score = 0.0;

    foreach (($homework['true_false'] ?? []) as $question => $expected) {
        $submittedRaw = strtolower(trim((string) ($answers[$question] ?? '')));
        $submitted = null;
        if (in_array($submittedRaw, ['true', 't', '1'], true)) {
            $submitted = true;
        } elseif (in_array($submittedRaw, ['false', 'f', '0'], true)) {
            $submitted = false;
        }

        $accepted = $submitted !== null && $submitted === (bool) $expected;
        $itemScore = $accepted ? 1.0 : 0.0;
        $score += $itemScore;
        $normalizedAnswers[$question] = $submitted;
        $feedback[$question] = [
            'correct' => $accepted,
            'score' => $itemScore,
            'max_score' => 1.0,
            'message' => $submitted === null ? 'No answer submitted.' : ($accepted ? 'Accepted.' : 'Try again.'),
        ];
    }

    $normalizedCode = [];
    foreach (($homework['code_outputs'] ?? []) as $question => $expectedOutput) {
        $code = (string) ($codeByQuestion[$question] ?? '');
        $normalizedCode[$question] = dsm_limit_lab_code($code, (int) ($graderConfig['max_code_bytes'] ?? 12000));
        $runnerConfig = $graderConfig;
        $runnerConfig['runner_profile'] = (string) ($homework['runner_profile'] ?? 'plain_python');
        $run = dsm_run_lab_code_cell($normalizedCode[$question], $runnerConfig);
        $actualOutput = dsm_normalize_lab_output((string) ($run['stdout'] ?? ''));
        $expectedNormalized = dsm_normalize_lab_output((string) $expectedOutput);
        $accepted = !empty($run['ok']) && $actualOutput === $expectedNormalized;
        $itemScore = $accepted ? 1.0 : 0.0;
        $score += $itemScore;

        $message = $accepted ? 'Accepted.' : 'Output did not match.';
        if (empty($run['ok']) && !empty($run['error'])) {
            $message = (string) $run['error'];
        }

        $feedback[$question] = [
            'correct' => $accepted,
            'score' => $itemScore,
            'max_score' => 1.0,
            'message' => $message,
            'stdout' => $actualOutput,
            'stderr' => dsm_limit_lab_code((string) ($run['stderr'] ?? ''), 2000),
        ];
    }

    return [
        'score' => round($score, 2),
        'max_score' => (float) ($homework['max_score'] ?? 10),
        'answers' => [
            'true_false' => $normalizedAnswers,
            'code' => $normalizedCode,
        ],
        'feedback' => $feedback,
    ];
}

function dsm_limit_lab_code(string $code, int $maxBytes): string
{
    $maxBytes = max(1000, $maxBytes);
    if (strlen($code) <= $maxBytes) {
        return $code;
    }
    return substr($code, 0, $maxBytes);
}

function dsm_normalize_lab_output(string $output): string
{
    $output = str_replace(["\r\n", "\r"], "\n", $output);
    $lines = array_map(static fn (string $line): string => rtrim($line), explode("\n", trim($output)));
    return implode("\n", $lines);
}

function dsm_run_lab_code_cell(string $code, array $graderConfig = []): array
{
    $runner = __DIR__ . '/python_lab_runner.py';
    if (!is_readable($runner)) {
        return ['ok' => false, 'stdout' => '', 'stderr' => '', 'error' => 'Code runner is not available.'];
    }

    $pythonBin = (string) ($graderConfig['python_bin'] ?? 'python3');
    $timeoutSeconds = max(1, min(10, (int) ($graderConfig['timeout_seconds'] ?? 3)));
    $runnerProfile = (string) ($graderConfig['runner_profile'] ?? 'plain_python');
    if (!in_array($runnerProfile, ['plain_python', 'pandas'], true)) {
        $runnerProfile = 'plain_python';
    }
    $pythonPaths = $graderConfig['python_paths'] ?? [];
    if (!is_array($pythonPaths)) {
        $pythonPaths = [];
    }
    $pythonPaths = array_values(array_filter($pythonPaths, static fn ($path): bool => is_string($path) && $path !== ''));
    $payload = json_encode([
        'code' => $code,
        'profile' => $runnerProfile,
        'python_paths' => $pythonPaths,
    ], JSON_UNESCAPED_SLASHES);
    if (!is_string($payload)) {
        return ['ok' => false, 'stdout' => '', 'stderr' => '', 'error' => 'Could not prepare code for grading.'];
    }

    $descriptorSpec = [
        0 => ['pipe', 'r'],
        1 => ['pipe', 'w'],
        2 => ['pipe', 'w'],
    ];
    $pythonArgs = $runnerProfile === 'pandas'
        ? [$pythonBin, $runner]
        : [$pythonBin, '-I', '-S', $runner];
    $process = proc_open($pythonArgs, $descriptorSpec, $pipes, sys_get_temp_dir());
    if (!is_resource($process)) {
        return ['ok' => false, 'stdout' => '', 'stderr' => '', 'error' => 'Could not start code runner.'];
    }

    fwrite($pipes[0], $payload);
    fclose($pipes[0]);
    stream_set_blocking($pipes[1], false);
    stream_set_blocking($pipes[2], false);

    $stdout = '';
    $stderr = '';
    $deadline = microtime(true) + $timeoutSeconds;
    $timedOut = false;
    while (true) {
        $stdout .= stream_get_contents($pipes[1]);
        $stderr .= stream_get_contents($pipes[2]);
        $status = proc_get_status($process);
        if (!$status['running']) {
            break;
        }
        if (microtime(true) >= $deadline) {
            $timedOut = true;
            proc_terminate($process);
            break;
        }
        usleep(20000);
    }

    $stdout .= stream_get_contents($pipes[1]);
    $stderr .= stream_get_contents($pipes[2]);
    fclose($pipes[1]);
    fclose($pipes[2]);
    $exitCode = proc_close($process);

    if ($timedOut) {
        return ['ok' => false, 'stdout' => $stdout, 'stderr' => $stderr, 'error' => 'Code timed out.'];
    }

    $decoded = json_decode($stdout, true);
    if (is_array($decoded) && array_key_exists('ok', $decoded)) {
        return $decoded;
    }

    return [
        'ok' => $exitCode === 0,
        'stdout' => $stdout,
        'stderr' => $stderr,
        'error' => $exitCode === 0 ? null : 'Code runner failed.',
    ];
}

function dsm_lab_feedback(float $score, float $maxScore): array
{
    if ($score >= $maxScore - 0.001) {
        return [
            'correct' => true,
            'score' => round($score, 2),
            'max_score' => $maxScore,
            'message' => 'Accepted.',
        ];
    }

    return [
        'correct' => false,
        'score' => round($score, 2),
        'max_score' => $maxScore,
        'message' => $score > 0 ? 'Some entries need review.' : 'Try again.',
    ];
}

function dsm_normalize_lab_string(mixed $value): string
{
    return trim((string) $value);
}

function dsm_normalize_lab_phrase(string $value): string
{
    $value = strtolower(trim($value));
    $value = preg_replace('/[^a-z0-9]+/', ' ', $value) ?? $value;
    return trim(preg_replace('/\s+/', ' ', $value) ?? $value);
}

function dsm_normalize_lab_binary(mixed $value): string
{
    return strtolower(str_replace(' ', '', trim((string) $value)));
}

function dsm_normalize_lab_hex(mixed $value): string
{
    return strtolower(str_replace(' ', '', trim((string) $value)));
}

function dsm_lab_number_equals(string $submitted, float $expected): bool
{
    if (!is_numeric($submitted)) {
        return false;
    }
    return abs((float) $submitted - $expected) <= 0.01;
}

function dsm_save_attempt_record(array $config, array $attempt): int|string
{
    try {
        $pdo = dsm_database_ready($config);
        $attemptId = dsm_save_attempt($pdo, $attempt);
        dsm_save_attempt_sqlite_backup($config['file_store'], $attempt);
        return $attemptId;
    } catch (Throwable $exception) {
        error_log('DSM quiz database save failed, using file fallback: ' . $exception->getMessage());
        $attemptId = dsm_save_attempt_file($config['file_store'], $attempt, $exception->getMessage());
        dsm_save_attempt_sqlite_backup($config['file_store'], $attempt);
        return $attemptId;
    }
}

function dsm_save_attempt(PDO $pdo, array $attempt): int
{
    $sql = 'INSERT INTO quiz_attempts (
        quiz_id, chapter, assignment_slug, student_user_id, canvas_course_id, canvas_assignment_id,
        canvas_user_id, lti_deployment_id, lti_context_id, lti_resource_link_id, lti_lineitem_url,
        student_identifier, score, max_score, answers_json, feedback_json,
        canvas_sync_status, canvas_sync_error, synced_to_canvas_at, ip_address, user_agent
    ) VALUES (
        :quiz_id, :chapter, :assignment_slug, :student_user_id, :canvas_course_id, :canvas_assignment_id,
        :canvas_user_id, :lti_deployment_id, :lti_context_id, :lti_resource_link_id, :lti_lineitem_url,
        :student_identifier, :score, :max_score, :answers_json, :feedback_json,
        :canvas_sync_status, :canvas_sync_error, :synced_to_canvas_at, :ip_address, :user_agent
    )';

    $stmt = $pdo->prepare($sql);
    $stmt->execute($attempt);
    return (int) $pdo->lastInsertId();
}

function dsm_save_attempt_file(array $fileStore, array $attempt, string $storageWarning): string
{
    $path = (string) ($fileStore['path'] ?? (sys_get_temp_dir() . '/dsm_quiz_attempts.jsonl'));
    $directory = dirname($path);
    if (!is_dir($directory) && !@mkdir($directory, 0770, true) && !is_dir($directory)) {
        $path = sys_get_temp_dir() . '/dsm_quiz_attempts.jsonl';
    }

    $attemptId = gmdate('YmdHis') . '-' . bin2hex(random_bytes(4));
    $record = $attempt + [
        'id' => $attemptId,
        'submitted_at' => gmdate('Y-m-d H:i:s'),
        'storage_warning' => $storageWarning,
    ];

    $json = json_encode($record, JSON_UNESCAPED_SLASHES);
    if ($json === false || file_put_contents($path, $json . PHP_EOL, FILE_APPEND | LOCK_EX) === false) {
        throw new RuntimeException('Could not write quiz attempt file.');
    }

    return $attemptId;
}

function dsm_save_attempt_sqlite_backup(array $fileStore, array $attempt): void
{
    if (($fileStore['sqlite_backup_enabled'] ?? true) === false) {
        return;
    }

    try {
        $path = (string) ($fileStore['sqlite_backup_path'] ?? (sys_get_temp_dir() . '/dsm_quiz_attempts_backup.sqlite'));
        $directory = dirname($path);
        if (!is_dir($directory) && !@mkdir($directory, 0770, true) && !is_dir($directory)) {
            $path = sys_get_temp_dir() . '/dsm_quiz_attempts_backup.sqlite';
        }

        $pdo = dsm_connect_database([
            'dsn' => 'sqlite:' . $path,
            'username' => null,
            'password' => null,
        ]);
        dsm_initialize_schema($pdo);
        dsm_save_attempt($pdo, $attempt);
    } catch (Throwable $exception) {
        error_log('DSM quiz SQLite backup failed: ' . $exception->getMessage());
    }
}

function dsm_canvas_ready(array $config, array $identity): bool
{
    return !empty($config['canvas']['enabled'])
        && !empty($config['canvas']['base_url'])
        && !empty($config['canvas']['access_token'])
        && !empty($identity['canvas_course_id'])
        && !empty($identity['canvas_assignment_id'])
        && !empty($identity['canvas_user_id']);
}

function dsm_find_existing_best_score(PDO $pdo, string $quizId, array $identity): ?float
{
    $idFilter = dsm_assignment_id_filter($quizId, 'assignment_id_');

    if (
        !empty($identity['canvas_course_id'])
        && !empty($identity['canvas_assignment_id'])
        && !empty($identity['canvas_user_id'])
    ) {
        $stmt = $pdo->prepare(
            'SELECT MAX(score) AS best_score
             FROM quiz_attempts
             WHERE quiz_id IN (' . $idFilter['sql'] . ')
               AND canvas_course_id = :canvas_course_id
               AND canvas_assignment_id = :canvas_assignment_id
               AND canvas_user_id = :canvas_user_id'
        );
        $stmt->execute($idFilter['params'] + [
            'canvas_course_id' => $identity['canvas_course_id'],
            'canvas_assignment_id' => $identity['canvas_assignment_id'],
            'canvas_user_id' => $identity['canvas_user_id'],
        ]);
    } elseif (!empty($identity['student_identifier'])) {
        $stmt = $pdo->prepare(
            'SELECT MAX(score) AS best_score
             FROM quiz_attempts
             WHERE quiz_id IN (' . $idFilter['sql'] . ')
               AND student_identifier = :student_identifier'
        );
        $stmt->execute($idFilter['params'] + [
            'student_identifier' => $identity['student_identifier'],
        ]);
    } else {
        return null;
    }

    $score = $stmt->fetchColumn();
    return $score === false || $score === null ? null : (float) $score;
}

function dsm_is_score_at_least_best(PDO $pdo, string $quizId, array $identity, float $score): bool
{
    $bestScore = dsm_find_existing_best_score($pdo, $quizId, $identity);
    return $bestScore === null || $score >= $bestScore - 0.001;
}

function dsm_attempt_summary(PDO $pdo, string $quizId, array $identity): array
{
    $idFilter = dsm_assignment_id_filter($quizId, 'assignment_id_');

    if (
        !empty($identity['canvas_course_id'])
        && !empty($identity['canvas_assignment_id'])
        && !empty($identity['canvas_user_id'])
    ) {
        $stmt = $pdo->prepare(
            'SELECT COUNT(*) AS attempt_count, MAX(score) AS best_score
             FROM quiz_attempts
             WHERE quiz_id IN (' . $idFilter['sql'] . ')
               AND canvas_course_id = :canvas_course_id
               AND canvas_assignment_id = :canvas_assignment_id
               AND canvas_user_id = :canvas_user_id'
        );
        $stmt->execute($idFilter['params'] + [
            'canvas_course_id' => $identity['canvas_course_id'],
            'canvas_assignment_id' => $identity['canvas_assignment_id'],
            'canvas_user_id' => $identity['canvas_user_id'],
        ]);
    } elseif (!empty($identity['student_identifier'])) {
        $stmt = $pdo->prepare(
            'SELECT COUNT(*) AS attempt_count, MAX(score) AS best_score
             FROM quiz_attempts
             WHERE quiz_id IN (' . $idFilter['sql'] . ')
               AND student_identifier = :student_identifier'
        );
        $stmt->execute($idFilter['params'] + [
            'student_identifier' => $identity['student_identifier'],
        ]);
    } else {
        return ['attempt_count' => 0, 'best_score' => null];
    }

    $row = $stmt->fetch() ?: [];
    return [
        'attempt_count' => (int) ($row['attempt_count'] ?? 0),
        'best_score' => ($row['best_score'] ?? null) === null ? null : (float) $row['best_score'],
    ];
}

function dsm_sync_canvas_grade(array $canvas, array $identity, string $postedGrade): array
{
    $baseUrl = rtrim((string) $canvas['base_url'], '/');
    $path = sprintf(
        '/api/v1/courses/%s/assignments/%s/submissions/%s',
        rawurlencode((string) $identity['canvas_course_id']),
        rawurlencode((string) $identity['canvas_assignment_id']),
        rawurlencode((string) $identity['canvas_user_id'])
    );

    $ch = curl_init($baseUrl . $path);
    curl_setopt_array($ch, [
        CURLOPT_CUSTOMREQUEST => 'PUT',
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_TIMEOUT => 20,
        CURLOPT_HTTPHEADER => [
            'Authorization: Bearer ' . $canvas['access_token'],
        ],
        CURLOPT_POSTFIELDS => http_build_query([
            'submission' => ['posted_grade' => $postedGrade],
            'comment' => ['text_comment' => 'DSM quiz score synced automatically.'],
        ]),
    ]);

    $body = curl_exec($ch);
    $error = curl_error($ch);
    $status = (int) curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
    curl_close($ch);

    if ($body !== false && $status >= 200 && $status < 300) {
        return [
            'status' => 'synced',
            'error' => null,
            'synced_at' => gmdate('Y-m-d H:i:s'),
        ];
    }

    return [
        'status' => 'failed',
        'error' => $error !== '' ? $error : 'Canvas returned HTTP ' . $status,
        'synced_at' => null,
    ];
}

function dsm_list_attempts(PDO $pdo, int $limit = 200): array
{
    $stmt = $pdo->prepare(
        'SELECT id, quiz_id, chapter, assignment_slug, canvas_course_id, canvas_assignment_id,
                canvas_user_id, lti_deployment_id, lti_context_id, lti_resource_link_id,
                lti_lineitem_url, student_identifier, score, max_score, answers_json,
                canvas_sync_status, canvas_sync_error, synced_to_canvas_at, submitted_at
         FROM quiz_attempts
         ORDER BY submitted_at DESC, id DESC
         LIMIT :limit'
    );
    $stmt->bindValue(':limit', $limit, PDO::PARAM_INT);
    $stmt->execute();
    return $stmt->fetchAll();
}

function dsm_list_student_attempts(PDO $pdo, int $studentUserId, int $limit = 200): array
{
    $stmt = $pdo->prepare(
        'SELECT id, quiz_id, chapter, assignment_slug, score, max_score,
                canvas_sync_status, submitted_at
         FROM quiz_attempts
         WHERE student_user_id = :student_user_id
         ORDER BY submitted_at DESC, id DESC
         LIMIT :limit'
    );
    $stmt->bindValue(':student_user_id', $studentUserId, PDO::PARAM_INT);
    $stmt->bindValue(':limit', $limit, PDO::PARAM_INT);
    $stmt->execute();
    return $stmt->fetchAll();
}

function dsm_list_student_score_summary(PDO $pdo, int $studentUserId): array
{
    $stmt = $pdo->prepare(
        'SELECT quiz_id, assignment_slug, score, max_score, submitted_at
         FROM quiz_attempts
         WHERE student_user_id = :student_user_id
         ORDER BY quiz_id ASC, submitted_at ASC'
    );
    $stmt->execute(['student_user_id' => $studentUserId]);
    $summary = [];

    foreach ($stmt->fetchAll() as $row) {
        $quizId = dsm_canonical_assignment_id((string) ($row['quiz_id'] ?? ''));
        $assignmentSlug = (string) ($row['assignment_slug'] ?? '');
        $key = $quizId . "\0" . $assignmentSlug;

        if (!isset($summary[$key])) {
            $summary[$key] = [
                'quiz_id' => $quizId,
                'assignment_slug' => $assignmentSlug,
                'attempt_count' => 0,
                'best_score' => null,
                'max_score' => null,
                'last_submitted_at' => null,
            ];
        }

        $summary[$key]['attempt_count']++;
        $score = (float) ($row['score'] ?? 0);
        $maxScore = (float) ($row['max_score'] ?? 0);
        $summary[$key]['best_score'] = $summary[$key]['best_score'] === null
            ? $score
            : max((float) $summary[$key]['best_score'], $score);
        $summary[$key]['max_score'] = $summary[$key]['max_score'] === null
            ? $maxScore
            : max((float) $summary[$key]['max_score'], $maxScore);
        if (
            $summary[$key]['last_submitted_at'] === null
            || (string) $row['submitted_at'] > (string) $summary[$key]['last_submitted_at']
        ) {
            $summary[$key]['last_submitted_at'] = $row['submitted_at'];
        }
    }

    $rows = array_values($summary);
    usort($rows, static fn (array $a, array $b): int => strcmp((string) $a['quiz_id'], (string) $b['quiz_id']));
    return $rows;
}

function dsm_list_admin_report_assignments(PDO $pdo): array
{
    $assignments = [];
    foreach (dsm_all_assignment_definitions() as $assignmentId => $definition) {
        $chapter = trim((string) ($definition['chapter'] ?? ''));
        $slug = trim((string) ($definition['assignment_slug'] ?? ''));
        $labelParts = array_filter([$chapter, $slug], static fn(string $part): bool => $part !== '');
        $assignments[$assignmentId] = [
            'assignment_id' => $assignmentId,
            'label' => $assignmentId . (count($labelParts) > 0 ? ' - ' . implode(' ', $labelParts) : ''),
        ];
    }

    $stmt = $pdo->query(
        'SELECT DISTINCT quiz_id
         FROM quiz_attempts
         WHERE quiz_id IS NOT NULL AND quiz_id <> \'\'
         ORDER BY quiz_id ASC'
    );
    foreach ($stmt->fetchAll() as $row) {
        $assignmentId = dsm_canonical_assignment_id((string) ($row['quiz_id'] ?? ''));
        if ($assignmentId !== '' && !isset($assignments[$assignmentId])) {
            $assignments[$assignmentId] = [
                'assignment_id' => $assignmentId,
                'label' => $assignmentId,
            ];
        }
    }

    uasort($assignments, static function (array $a, array $b): int {
        return strnatcasecmp((string) $a['assignment_id'], (string) $b['assignment_id']);
    });
    return array_values($assignments);
}

function dsm_list_admin_report_assignment_numbers(PDO $pdo): array
{
    $numbers = [];
    foreach (array_keys(dsm_all_assignment_definitions()) as $assignmentId) {
        if (preg_match('/^(ch\d{2})-/', $assignmentId, $matches) === 1) {
            $numbers[$matches[1]] = $matches[1];
        }
    }

    $stmt = $pdo->query(
        'SELECT DISTINCT quiz_id
         FROM quiz_attempts
         WHERE quiz_id IS NOT NULL AND quiz_id <> \'\'
         ORDER BY quiz_id ASC'
    );
    foreach ($stmt->fetchAll() as $row) {
        $assignmentId = dsm_canonical_assignment_id((string) ($row['quiz_id'] ?? ''));
        if (preg_match('/^(ch\d{2})-/', $assignmentId, $matches) === 1) {
            $numbers[$matches[1]] = $matches[1];
        }
    }

    natcasesort($numbers);
    return array_values($numbers);
}

function dsm_report_excluded_student_identifiers(PDO $pdo): array
{
    $adminIdentifiers = [];
    foreach (['tchen', 'tcn85', 'ms6q3', 'mysql-smoke', 'lti-live-smoke'] as $identifier) {
        $adminIdentifiers[dsm_normalize_student_identifier($identifier)] = true;
    }

    $adminRows = $pdo->query(
        'SELECT email, student_identifier, canvas_user_id
         FROM quiz_users
         WHERE role = \'admin\''
    )->fetchAll();
    foreach ($adminRows as $adminRow) {
        foreach (['email', 'student_identifier', 'canvas_user_id'] as $field) {
            $identifier = dsm_normalize_student_identifier((string) ($adminRow[$field] ?? ''));
            if ($identifier !== '') {
                $adminIdentifiers[$identifier] = true;
            }
        }
    }

    return $adminIdentifiers;
}

function dsm_is_report_excluded_student(PDO $pdo, ?string $studentIdentifier, ?string $canvasUserId = null): bool
{
    $excluded = dsm_report_excluded_student_identifiers($pdo);
    foreach ([$studentIdentifier, $canvasUserId] as $identifier) {
        $normalized = dsm_normalize_student_identifier($identifier);
        if ($normalized !== '' && isset($excluded[$normalized])) {
            return true;
        }
    }
    return false;
}

function dsm_list_admin_report_students(PDO $pdo): array
{
    $adminIdentifiers = dsm_report_excluded_student_identifiers($pdo);

    $users = $pdo->query(
        'SELECT display_name, role, status, student_identifier, email, canvas_user_id
         FROM quiz_users
         WHERE role = \'student\' AND status = \'active\'
         ORDER BY display_name ASC, student_identifier ASC, email ASC'
    )->fetchAll();

    $students = [];
    foreach ($users as $user) {
        if (($user['role'] ?? null) === 'admin') {
            continue;
        }

        $identifier = dsm_normalize_student_identifier((string) ($user['student_identifier'] ?? ''));
        if ($identifier === '') {
            $identifier = dsm_normalize_student_identifier((string) ($user['email'] ?? ''));
        }
        if ($identifier === '') {
            $identifier = dsm_normalize_student_identifier((string) ($user['canvas_user_id'] ?? ''));
        }
        if ($identifier === '') {
            continue;
        }
        if (
            isset($adminIdentifiers[$identifier])
            || isset($adminIdentifiers[dsm_normalize_student_identifier((string) ($user['email'] ?? ''))])
            || isset($adminIdentifiers[dsm_normalize_student_identifier((string) ($user['canvas_user_id'] ?? ''))])
        ) {
            continue;
        }

        $displayName = trim((string) ($user['display_name'] ?? ''));
        $label = $displayName !== '' && dsm_normalize_student_identifier($displayName) !== $identifier
            ? $displayName . ' (' . $identifier . ')'
            : $identifier;

        if (!isset($students[$identifier]) || $students[$identifier]['label'] === $identifier) {
            $students[$identifier] = [
                'student_identifier' => $identifier,
                'display_name' => $displayName,
                'label' => $label,
            ];
        }
    }

    uasort($students, static function (array $a, array $b): int {
        return strnatcasecmp((string) $a['label'], (string) $b['label']);
    });
    return array_values($students);
}

function dsm_list_admin_score_report(
    PDO $pdo,
    ?string $assignmentTypeFilter = null,
    ?string $assignmentNumberFilter = null,
    ?string $studentFilter = null,
    string $scoreMode = 'best'
): array
{
    $assignmentTypeFilter = $assignmentTypeFilter !== null ? trim(strtolower($assignmentTypeFilter)) : null;
    $assignmentNumberFilter = $assignmentNumberFilter !== null ? trim(strtolower($assignmentNumberFilter)) : null;
    $studentFilter = $studentFilter !== null ? dsm_normalize_student_identifier($studentFilter) : null;
    $scoreMode = $scoreMode === 'all' ? 'all' : 'best';

    $users = $pdo->query(
        'SELECT id, email, display_name, role, student_identifier, canvas_user_id
         FROM quiz_users'
    )->fetchAll();
    $usersById = [];
    $usersByIdentifier = [];
    $usersByEmail = [];
    $usersByCanvasId = [];
    foreach ($users as $user) {
        $usersById[(int) $user['id']] = $user;

        $identifier = dsm_normalize_student_identifier((string) ($user['student_identifier'] ?? ''));
        if ($identifier !== '' && !isset($usersByIdentifier[$identifier])) {
            $usersByIdentifier[$identifier] = $user;
        }

        $email = strtolower(trim((string) ($user['email'] ?? '')));
        if ($email !== '' && !isset($usersByEmail[$email])) {
            $usersByEmail[$email] = $user;
        }
        $emailLocal = dsm_normalize_student_identifier($email);
        if ($emailLocal !== '' && !isset($usersByIdentifier[$emailLocal])) {
            $usersByIdentifier[$emailLocal] = $user;
        }

        $canvasUserId = strtolower(trim((string) ($user['canvas_user_id'] ?? '')));
        if ($canvasUserId !== '' && !isset($usersByCanvasId[$canvasUserId])) {
            $usersByCanvasId[$canvasUserId] = $user;
        }
    }

    $stmt = $pdo->query(
        'SELECT student_user_id, canvas_user_id, student_identifier, quiz_id, assignment_slug,
                score, max_score, submitted_at
         FROM quiz_attempts
         ORDER BY student_identifier ASC, quiz_id ASC, submitted_at ASC'
    );
    $summary = [];
    $attemptRows = [];
    $attemptIndexes = [];

    foreach ($stmt->fetchAll() as $row) {
        $rawIdentifier = (string) ($row['student_identifier'] ?? '');
        $normalizedIdentifier = dsm_normalize_student_identifier($rawIdentifier);
        $rawCanvasUserId = strtolower(trim((string) ($row['canvas_user_id'] ?? '')));

        $user = null;
        $studentUserId = (int) ($row['student_user_id'] ?? 0);
        if ($studentUserId > 0 && isset($usersById[$studentUserId])) {
            $user = $usersById[$studentUserId];
        } elseif ($normalizedIdentifier !== '' && isset($usersByIdentifier[$normalizedIdentifier])) {
            $user = $usersByIdentifier[$normalizedIdentifier];
        } elseif (str_contains($rawIdentifier, '@') && isset($usersByEmail[strtolower(trim($rawIdentifier))])) {
            $user = $usersByEmail[strtolower(trim($rawIdentifier))];
        } elseif ($rawCanvasUserId !== '' && isset($usersByCanvasId[$rawCanvasUserId])) {
            $user = $usersByCanvasId[$rawCanvasUserId];
        }
        if (($user['role'] ?? null) === 'admin') {
            continue;
        }
        if (dsm_is_report_excluded_student($pdo, $rawIdentifier, $rawCanvasUserId)) {
            continue;
        }

        $studentIdentifier = $user
            ? dsm_normalize_student_identifier((string) ($user['student_identifier'] ?? $rawIdentifier))
            : $normalizedIdentifier;
        if ($studentIdentifier === '') {
            $studentIdentifier = $rawCanvasUserId !== '' ? $rawCanvasUserId : 'Unknown';
        }
        if (dsm_is_report_excluded_student($pdo, $studentIdentifier, $rawCanvasUserId)) {
            continue;
        }

        $displayName = $user ? trim((string) ($user['display_name'] ?? '')) : '';
        if (dsm_normalize_student_identifier($displayName) === $studentIdentifier) {
            $displayName = '';
        }

        $quizId = dsm_canonical_assignment_id((string) ($row['quiz_id'] ?? ''));
        $assignmentSlug = trim((string) ($row['assignment_slug'] ?? ''));
        if ($assignmentSlug === '' && str_contains($quizId, '-')) {
            $assignmentSlug = substr($quizId, (int) strrpos($quizId, '-') + 1);
        }
        $assignmentNumber = '';
        if (preg_match('/^(ch\d{2})-/', $quizId, $matches) === 1) {
            $assignmentNumber = strtolower($matches[1]);
        }

        if ($assignmentTypeFilter !== null && $assignmentTypeFilter !== '' && $assignmentSlug !== $assignmentTypeFilter) {
            continue;
        }
        if ($assignmentNumberFilter !== null && $assignmentNumberFilter !== '' && $assignmentNumber !== $assignmentNumberFilter) {
            continue;
        }
        if ($studentFilter !== null && $studentFilter !== '' && $studentIdentifier !== $studentFilter) {
            continue;
        }

        if ($scoreMode === 'all') {
            $attemptKey = $studentIdentifier . "\0" . $quizId;
            $attemptIndexes[$attemptKey] = ($attemptIndexes[$attemptKey] ?? 0) + 1;
            $score = (float) ($row['score'] ?? 0);
            $maxScore = (float) ($row['max_score'] ?? 0);
            $attemptRows[] = [
                'student_identifier' => $studentIdentifier,
                'display_name' => $displayName,
                'quiz_id' => $quizId,
                'assignment_slug' => $assignmentSlug,
                'attempt_count' => $attemptIndexes[$attemptKey],
                'best_score' => $score,
                'max_score' => $maxScore,
                'last_submitted_at' => $row['submitted_at'],
            ];
            continue;
        }

        $key = $studentIdentifier . "\0" . $quizId . "\0" . $assignmentSlug;

        if (!isset($summary[$key])) {
            $summary[$key] = [
                'student_identifier' => $studentIdentifier,
                'display_name' => $displayName,
                'quiz_id' => $quizId,
                'assignment_slug' => $assignmentSlug,
                'attempt_count' => 0,
                'best_score' => null,
                'max_score' => null,
                'last_submitted_at' => null,
            ];
        } elseif ($summary[$key]['display_name'] === '' && $displayName !== '') {
            $summary[$key]['display_name'] = $displayName;
        }

        $summary[$key]['attempt_count']++;
        $score = (float) ($row['score'] ?? 0);
        $maxScore = (float) ($row['max_score'] ?? 0);
        $summary[$key]['best_score'] = $summary[$key]['best_score'] === null
            ? $score
            : max((float) $summary[$key]['best_score'], $score);
        $summary[$key]['max_score'] = $summary[$key]['max_score'] === null
            ? $maxScore
            : max((float) $summary[$key]['max_score'], $maxScore);
        if (
            $summary[$key]['last_submitted_at'] === null
            || (string) $row['submitted_at'] > (string) $summary[$key]['last_submitted_at']
        ) {
            $summary[$key]['last_submitted_at'] = $row['submitted_at'];
        }
    }

    if ($scoreMode === 'all') {
        usort($attemptRows, static function (array $a, array $b): int {
            return strcmp(
                (string) $a['student_identifier'] . "\0" . (string) $a['quiz_id'] . "\0" . (string) $a['last_submitted_at'],
                (string) $b['student_identifier'] . "\0" . (string) $b['quiz_id'] . "\0" . (string) $b['last_submitted_at']
            );
        });
        return $attemptRows;
    }

    if (
        $assignmentTypeFilter !== null && $assignmentTypeFilter !== ''
        && $assignmentNumberFilter !== null && $assignmentNumberFilter !== ''
    ) {
        $quizId = dsm_canonical_assignment_id($assignmentNumberFilter . '-' . $assignmentTypeFilter);
        $definition = dsm_assignment_definition($quizId);
        $maxScore = (float) ($definition['max_score'] ?? 10);
        foreach (dsm_list_admin_report_students($pdo) as $student) {
            $studentIdentifier = (string) ($student['student_identifier'] ?? '');
            if ($studentFilter !== null && $studentFilter !== '' && $studentIdentifier !== $studentFilter) {
                continue;
            }
            $key = $studentIdentifier . "\0" . $quizId . "\0" . $assignmentTypeFilter;
            if (isset($summary[$key])) {
                continue;
            }
            $summary[$key] = [
                'student_identifier' => $studentIdentifier,
                'display_name' => (string) ($student['display_name'] ?? ''),
                'quiz_id' => $quizId,
                'assignment_slug' => $assignmentTypeFilter,
                'attempt_count' => 0,
                'best_score' => 0,
                'max_score' => $maxScore,
                'last_submitted_at' => '',
            ];
        }
    }

    $rows = array_values($summary);
    usort($rows, static function (array $a, array $b): int {
        return strcmp(
            (string) $a['student_identifier'] . "\0" . (string) $a['quiz_id'],
            (string) $b['student_identifier'] . "\0" . (string) $b['quiz_id']
        );
    });
    return $rows;
}

function dsm_sync_pending_attempts(PDO $pdo, array $config, int $limit = 100): array
{
    $stmt = $pdo->prepare(
        'SELECT id, quiz_id, canvas_course_id, canvas_assignment_id, canvas_user_id, student_identifier, score
         FROM quiz_attempts
         WHERE canvas_sync_status IN (\'pending\', \'failed\')
         ORDER BY submitted_at ASC, id ASC
         LIMIT :limit'
    );
    $stmt->bindValue(':limit', $limit, PDO::PARAM_INT);
    $stmt->execute();
    $attempts = $stmt->fetchAll();

    $summary = ['synced' => 0, 'failed' => 0, 'skipped' => 0, 'checked' => count($attempts)];
    foreach ($attempts as $attempt) {
        if (
            empty($attempt['canvas_course_id'])
            || empty($attempt['canvas_assignment_id'])
            || empty($attempt['canvas_user_id'])
        ) {
            dsm_update_sync_status($pdo, (int) $attempt['id'], [
                'status' => 'skipped',
                'error' => 'Missing Canvas course, assignment, or user ID.',
                'synced_at' => null,
            ]);
            $summary['skipped']++;
            continue;
        }

        if (!dsm_is_score_at_least_best($pdo, (string) $attempt['quiz_id'], $attempt, (float) $attempt['score'])) {
            dsm_update_sync_status($pdo, (int) $attempt['id'], [
                'status' => 'skipped',
                'error' => 'Lower than the student\'s highest attempt for this assignment.',
                'synced_at' => null,
            ]);
            $summary['skipped']++;
            continue;
        }

        if (empty($config['canvas']['enabled'])) {
            dsm_update_sync_status($pdo, (int) $attempt['id'], [
                'status' => 'failed',
                'error' => 'Canvas sync is not enabled.',
                'synced_at' => null,
            ]);
            $summary['failed']++;
            continue;
        }

        $result = dsm_sync_canvas_grade($config['canvas'], $attempt, (string) $attempt['score']);
        dsm_update_sync_status($pdo, (int) $attempt['id'], $result);
        $summary[$result['status'] === 'synced' ? 'synced' : 'failed']++;
    }

    return $summary;
}

function dsm_update_sync_status(PDO $pdo, int $attemptId, array $result): void
{
    $stmt = $pdo->prepare(
        'UPDATE quiz_attempts
         SET canvas_sync_status = :status,
             canvas_sync_error = :error,
             synced_to_canvas_at = :synced_at
         WHERE id = :id'
    );
    $stmt->execute([
        'status' => $result['status'],
        'error' => $result['error'],
        'synced_at' => $result['synced_at'],
        'id' => $attemptId,
    ]);
}

function dsm_start_admin_session(array $config): void
{
    session_name((string) $config['auth']['session_name']);
    session_set_cookie_params([
        'lifetime' => 0,
        'path' => '/',
        'secure' => true,
        'httponly' => true,
        'samesite' => 'Lax',
    ]);
    session_start();
}

function dsm_start_lti_session(array $config): void
{
    if (session_status() === PHP_SESSION_ACTIVE) {
        return;
    }
    session_name((string) $config['lti']['session_name']);
    session_set_cookie_params([
        'lifetime' => 0,
        'path' => '/',
        'secure' => true,
        'httponly' => true,
        'samesite' => 'None',
    ]);
    session_start();
}

function dsm_start_student_session(array $config): void
{
    if (session_status() === PHP_SESSION_ACTIVE) {
        return;
    }
    $sessionName = (string) ($config['student_auth']['session_name'] ?? 'dsm_student');
    session_name($sessionName);
    if (isset($_COOKIE[$sessionName]) && preg_match('/^[a-zA-Z0-9,-]{16,128}$/', (string) $_COOKIE[$sessionName])) {
        session_id((string) $_COOKIE[$sessionName]);
    }
    session_set_cookie_params([
        'lifetime' => 0,
        'path' => '/',
        'secure' => true,
        'httponly' => true,
        'samesite' => 'Lax',
    ]);
    session_start();
}

function dsm_start_fresh_student_session(array $config): void
{
    if (session_status() === PHP_SESSION_ACTIVE) {
        session_write_close();
        $_SESSION = [];
    }
    session_name((string) ($config['student_auth']['session_name'] ?? 'dsm_student'));
    session_set_cookie_params([
        'lifetime' => 0,
        'path' => '/',
        'secure' => true,
        'httponly' => true,
        'samesite' => 'Lax',
    ]);
    session_id(dsm_random_token());
    session_start();
}

function dsm_submission_auth_required(array $config): bool
{
    return !empty($config['student_auth']['require_authenticated_submissions']);
}

function dsm_student_email_verification_required(array $config): bool
{
    return !empty($config['student_auth']['require_university_email_verification']);
}

function dsm_find_student_for_login(PDO $pdo, string $identifier): ?array
{
    $normalized = dsm_normalize_student_identifier($identifier);
    if ($normalized === '') {
        return null;
    }

    $stmt = $pdo->prepare(
        'SELECT id, email, display_name, role, status, password_hash, student_identifier,
                email_verified_at, verification_code_hash, verification_code_expires_at
         FROM quiz_users
         WHERE role = \'student\'
           AND status = \'active\'
           AND (
                LOWER(email) = LOWER(:identifier)
                OR LOWER(student_identifier) = LOWER(:normalized_identifier)
           )
         LIMIT 1'
    );
    $stmt->execute([
        'identifier' => trim($identifier),
        'normalized_identifier' => $normalized,
    ]);
    $student = $stmt->fetch();
    return is_array($student) ? $student : null;
}

function dsm_university_email_allowed(array $config, string $studentIdentifier, string $email): bool
{
    $email = strtolower(trim($email));
    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        return false;
    }

    [$localPart, $domain] = explode('@', $email, 2);
    $allowedDomains = array_map('strtolower', array_map('strval', $config['student_auth']['allowed_email_domains'] ?? []));
    if ($allowedDomains !== [] && !in_array($domain, $allowedDomains, true)) {
        return false;
    }

    return dsm_normalize_student_identifier($localPart) === dsm_normalize_student_identifier($studentIdentifier);
}

function dsm_send_student_verification_code(PDO $pdo, array $config, string $identifier, string $email): bool
{
    $student = dsm_find_student_for_login($pdo, $identifier);
    if (!is_array($student)) {
        error_log('DSM student verification code failed: no active student matched the submitted identifier.');
        return false;
    }

    $studentIdentifier = (string) ($student['student_identifier'] ?: dsm_normalize_student_identifier((string) $student['email']));
    if (!dsm_university_email_allowed($config, $studentIdentifier, $email)) {
        error_log('DSM student verification code failed: university email did not match allowed domains or student identifier for user id ' . (int) $student['id']);
        return false;
    }

    $code = (string) random_int(100000, 999999);
    $minutes = max(5, (int) ($config['student_auth']['verification_code_minutes'] ?? 20));
    $expiresAt = date('Y-m-d H:i:s', time() + ($minutes * 60));

    $stmt = $pdo->prepare(
        'UPDATE quiz_users
         SET email = :email,
             verification_code_hash = :verification_code_hash,
             verification_code_expires_at = :verification_code_expires_at
         WHERE id = :id'
    );
    $stmt->execute([
        'email' => strtolower(trim($email)),
        'verification_code_hash' => password_hash($code, PASSWORD_DEFAULT),
        'verification_code_expires_at' => $expiresAt,
        'id' => (int) $student['id'],
    ]);

    $subject = 'Your ThinkDSM verification code';
    $body = "Your ThinkDSM verification code is {$code}.\n\nThis code expires in {$minutes} minutes.";
    if (!dsm_send_email($config, strtolower(trim($email)), $subject, $body)) {
        error_log('DSM student verification email failed for user id ' . (int) $student['id']);
        return false;
    }

    return true;
}

function dsm_verify_student_email_code(PDO $pdo, string $identifier, string $code, string $newPassword): bool
{
    $student = dsm_find_student_for_login($pdo, $identifier);
    if (!is_array($student)) {
        return false;
    }

    if (strlen($newPassword) < 10) {
        return false;
    }

    $hash = (string) ($student['verification_code_hash'] ?? '');
    $expiresAt = strtotime((string) ($student['verification_code_expires_at'] ?? ''));
    if ($hash === '' || $expiresAt === false || $expiresAt < time()) {
        return false;
    }

    if (!password_verify(trim($code), $hash)) {
        return false;
    }

    $stmt = $pdo->prepare(
        'UPDATE quiz_users
         SET email_verified_at = CURRENT_TIMESTAMP,
             password_hash = :password_hash,
             verification_code_hash = NULL,
             verification_code_expires_at = NULL
         WHERE id = :id'
    );
    $stmt->execute([
        'password_hash' => password_hash($newPassword, PASSWORD_DEFAULT),
        'id' => (int) $student['id'],
    ]);
    return true;
}

function dsm_send_student_verification_link(PDO $pdo, array $config, string $email, string $target = '/'): bool
{
    $email = strtolower(trim($email));
    if ($email !== '' && !str_contains($email, '@')) {
        $email .= '@umsystem.edu';
    }
    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        error_log('DSM student verification link failed: submitted email or identifier was not a valid university email.');
        return false;
    }

    [$localPart] = explode('@', $email, 2);
    $identifier = dsm_normalize_student_identifier($localPart);
    $student = dsm_find_student_for_login($pdo, $identifier);
    if (!is_array($student)) {
        error_log('DSM student verification link failed: no active student matched the submitted email local part.');
        return false;
    }

    $studentIdentifier = (string) ($student['student_identifier'] ?: dsm_normalize_student_identifier((string) $student['email']));
    if (!dsm_university_email_allowed($config, $studentIdentifier, $email)) {
        error_log('DSM student verification link failed: university email did not match allowed domains or student identifier for user id ' . (int) $student['id']);
        return false;
    }

    $previousStmt = $pdo->prepare(
        'SELECT email, verification_code_hash, verification_code_expires_at
         FROM quiz_users
         WHERE id = :id'
    );
    $previousStmt->execute(['id' => (int) $student['id']]);
    $previous = $previousStmt->fetch(PDO::FETCH_ASSOC) ?: [];

    $token = bin2hex(random_bytes(16));
    $minutes = max(5, (int) ($config['student_auth']['verification_code_minutes'] ?? 20));
    $expiresAt = date('Y-m-d H:i:s', time() + ($minutes * 60));

    $stmt = $pdo->prepare(
        'UPDATE quiz_users
         SET email = :email,
             verification_code_hash = :verification_code_hash,
             verification_code_expires_at = :verification_code_expires_at
         WHERE id = :id'
    );
    $stmt->execute([
        'email' => $email,
        'verification_code_hash' => dsm_token_fingerprint($token),
        'verification_code_expires_at' => $expiresAt,
        'id' => (int) $student['id'],
    ]);

    $link = 'https://thinkdsm.org/api/student/create-password.php?uid=' . rawurlencode((string) $student['id'])
        . '&token=' . rawurlencode($token)
        . '&next=' . rawurlencode(dsm_safe_target($target));
    $subject = 'Create your ThinkDSM password';
    $body = "Use this link to create or reset your ThinkDSM password:\n\n{$link}\n\nThis link expires in {$minutes} minutes.";
    if (!dsm_send_email($config, $email, $subject, $body)) {
        $restore = $pdo->prepare(
            'UPDATE quiz_users
             SET email = :email,
                 verification_code_hash = :verification_code_hash,
                 verification_code_expires_at = :verification_code_expires_at
             WHERE id = :id'
        );
        $restore->execute([
            'email' => (string) ($previous['email'] ?? $student['email']),
            'verification_code_hash' => $previous['verification_code_hash'] ?? null,
            'verification_code_expires_at' => $previous['verification_code_expires_at'] ?? null,
            'id' => (int) $student['id'],
        ]);
        error_log('DSM student verification link email failed for user id ' . (int) $student['id']);
        return false;
    }

    return true;
}

function dsm_verify_student_email_token(PDO $pdo, string $token, string $newPassword, ?int $userId = null): ?string
{
    $token = trim($token);
    if ($token === '' || strlen($newPassword) < 10) {
        return null;
    }

    if ($userId !== null && $userId > 0) {
        $stmt = $pdo->prepare(
            'SELECT id, student_identifier, email, verification_code_hash, verification_code_expires_at
             FROM quiz_users
             WHERE id = :id
               AND role = \'student\'
               AND status = \'active\'
               AND verification_code_hash IS NOT NULL
               AND verification_code_expires_at IS NOT NULL'
        );
        $stmt->execute(['id' => $userId]);
    } else {
        $stmt = $pdo->query(
            'SELECT id, student_identifier, email, verification_code_hash, verification_code_expires_at
             FROM quiz_users
             WHERE role = \'student\'
               AND status = \'active\'
               AND verification_code_hash IS NOT NULL
               AND verification_code_expires_at IS NOT NULL'
        );
    }

    foreach ($stmt as $student) {
        $expiresAt = strtotime((string) ($student['verification_code_expires_at'] ?? ''));
        if ($expiresAt === false || $expiresAt < time()) {
            continue;
        }
        if (!dsm_token_matches($token, (string) ($student['verification_code_hash'] ?? ''))) {
            continue;
        }

        $update = $pdo->prepare(
            'UPDATE quiz_users
             SET email_verified_at = CURRENT_TIMESTAMP,
                 password_hash = :password_hash,
                 verification_code_hash = NULL,
                 verification_code_expires_at = NULL
             WHERE id = :id'
        );
        $update->execute([
            'password_hash' => password_hash($newPassword, PASSWORD_DEFAULT),
            'id' => (int) $student['id'],
        ]);

        return (string) ($student['student_identifier'] ?: dsm_normalize_student_identifier((string) $student['email']));
    }

    return null;
}

function dsm_safe_target(string $target): string
{
    if ($target === '' || $target[0] !== '/' || str_starts_with($target, '//')) {
        return '/';
    }
    return $target;
}

function dsm_token_fingerprint(string $token): string
{
    return 'sha256:' . hash('sha256', $token);
}

function dsm_token_matches(string $token, string $storedHash): bool
{
    if (str_starts_with($storedHash, 'sha256:')) {
        return hash_equals($storedHash, dsm_token_fingerprint($token));
    }
    return password_verify($token, $storedHash);
}

function dsm_send_email(array $config, string $to, string $subject, string $body): bool
{
    $from = (string) ($config['student_auth']['email_from'] ?? 'no-reply@thinkdsm.org');
    $smtp = $config['student_auth']['smtp'] ?? [];
    if (is_array($smtp) && !empty($smtp['host']) && !empty($smtp['username']) && !empty($smtp['password'])) {
        return dsm_send_smtp_email($smtp, $from, $to, $subject, $body);
    }

    $headers = "From: {$from}\r\nContent-Type: text/plain; charset=UTF-8";
    $sent = mail($to, $subject, $body, $headers);
    if (!$sent) {
        error_log('DSM mail() send failed for message subject: ' . $subject);
    }
    return $sent;
}

function dsm_send_smtp_email(array $smtp, string $from, string $to, string $subject, string $body): bool
{
    if (!filter_var($from, FILTER_VALIDATE_EMAIL) || !filter_var($to, FILTER_VALIDATE_EMAIL)) {
        return false;
    }

    $host = (string) $smtp['host'];
    $port = (int) ($smtp['port'] ?? 587);
    $secure = strtolower((string) ($smtp['secure'] ?? 'tls'));
    $username = (string) $smtp['username'];
    $password = (string) $smtp['password'];
    $remote = ($secure === 'ssl' ? 'ssl://' : '') . $host . ':' . $port;
    $errno = 0;
    $errstr = '';
    $socket = stream_socket_client($remote, $errno, $errstr, 20, STREAM_CLIENT_CONNECT);
    if (!is_resource($socket)) {
        error_log('DSM SMTP connect failed: ' . $errstr);
        return false;
    }
    stream_set_timeout($socket, 20);

    try {
        dsm_smtp_expect($socket, [220]);
        dsm_smtp_command($socket, 'EHLO thinkdsm.org', [250]);
        if ($secure === 'tls') {
            dsm_smtp_command($socket, 'STARTTLS', [220]);
            if (!stream_socket_enable_crypto($socket, true, STREAM_CRYPTO_METHOD_TLS_CLIENT)) {
                throw new RuntimeException('SMTP STARTTLS failed.');
            }
            dsm_smtp_command($socket, 'EHLO thinkdsm.org', [250]);
        }
        dsm_smtp_command($socket, 'AUTH LOGIN', [334]);
        dsm_smtp_command($socket, base64_encode($username), [334]);
        dsm_smtp_command($socket, base64_encode($password), [235]);
        dsm_smtp_command($socket, 'MAIL FROM:<' . $from . '>', [250]);
        dsm_smtp_command($socket, 'RCPT TO:<' . $to . '>', [250, 251]);
        dsm_smtp_command($socket, 'DATA', [354]);

        $message = dsm_smtp_message($from, $to, $subject, $body);
        fwrite($socket, $message . "\r\n.\r\n");
        dsm_smtp_expect($socket, [250]);
        dsm_smtp_command($socket, 'QUIT', [221]);
        fclose($socket);
        return true;
    } catch (Throwable $exception) {
        error_log('DSM SMTP send failed: ' . $exception->getMessage());
        if (is_resource($socket)) {
            fclose($socket);
        }
        return false;
    }
}

function dsm_smtp_message(string $from, string $to, string $subject, string $body): string
{
    $headers = [
        'Date: ' . date(DATE_RFC2822),
        'From: ' . $from,
        'To: ' . $to,
        'Subject: ' . str_replace(["\r", "\n"], '', $subject),
        'MIME-Version: 1.0',
        'Content-Type: text/plain; charset=UTF-8',
    ];
    $normalizedBody = preg_replace("/\r\n|\r|\n/", "\r\n", $body) ?? $body;
    $normalizedBody = preg_replace('/^\./m', '..', $normalizedBody) ?? $normalizedBody;
    return implode("\r\n", $headers) . "\r\n\r\n" . $normalizedBody;
}

function dsm_smtp_command(mixed $socket, string $command, array $expectedCodes): string
{
    fwrite($socket, $command . "\r\n");
    return dsm_smtp_expect($socket, $expectedCodes);
}

function dsm_smtp_expect(mixed $socket, array $expectedCodes): string
{
    $response = '';
    do {
        $line = fgets($socket, 515);
        if ($line === false) {
            throw new RuntimeException('SMTP server closed the connection.');
        }
        $response .= $line;
    } while (isset($line[3]) && $line[3] === '-');

    $code = (int) substr($response, 0, 3);
    if (!in_array($code, $expectedCodes, true)) {
        throw new RuntimeException('Unexpected SMTP response: ' . trim($response));
    }
    return $response;
}

function dsm_lti_claim(array $claims, string $name, mixed $default = null): mixed
{
    return $claims[$name] ?? $default;
}

function dsm_lti_nested_claim(array $claims, string $name, string $key, mixed $default = null): mixed
{
    $value = $claims[$name] ?? null;
    return is_array($value) ? ($value[$key] ?? $default) : $default;
}

function dsm_lti_login_redirect(array $config, array $request): never
{
    if (empty($config['lti']['enabled'])) {
        http_response_code(503);
        exit('LTI is not enabled.');
    }

    foreach (['iss', 'login_hint', 'client_id'] as $required) {
        if (empty($request[$required])) {
            http_response_code(400);
            exit('Missing LTI login parameter: ' . dsm_h($required));
        }
    }

    if ((string) $request['iss'] !== (string) $config['lti']['issuer']) {
        http_response_code(400);
        exit('Unexpected LTI issuer.');
    }

    if ((string) $request['client_id'] !== (string) $config['lti']['client_id']) {
        http_response_code(400);
        exit('Unexpected LTI client ID.');
    }

    dsm_start_lti_session($config);

    $state = dsm_random_token();
    $nonce = dsm_random_token();
    $target = (string) ($request['target_link_uri'] ?? $config['lti']['default_target_link_uri']);

    $_SESSION['lti_state'][$state] = [
        'nonce' => $nonce,
        'target_link_uri' => $target,
        'created_at' => time(),
    ];

    $query = http_build_query([
        'scope' => 'openid',
        'response_type' => 'id_token',
        'response_mode' => 'form_post',
        'prompt' => 'none',
        'client_id' => $config['lti']['client_id'],
        'redirect_uri' => $config['lti']['redirect_uri'],
        'login_hint' => $request['login_hint'],
        'state' => $state,
        'nonce' => $nonce,
        'lti_message_hint' => $request['lti_message_hint'] ?? '',
    ]);

    header('Location: ' . rtrim((string) $config['lti']['auth_login_url'], '?') . '?' . $query);
    exit;
}

function dsm_lti_handle_launch(PDO $pdo, array $config, array $post): string
{
    if (empty($config['lti']['enabled'])) {
        throw new RuntimeException('LTI is not enabled.');
    }

    dsm_start_lti_session($config);

    $state = (string) ($post['state'] ?? '');
    $launchState = $_SESSION['lti_state'][$state] ?? null;
    unset($_SESSION['lti_state'][$state]);

    if (!is_array($launchState) || time() - (int) ($launchState['created_at'] ?? 0) > 600) {
        throw new RuntimeException('Invalid or expired LTI launch state.');
    }

    $claims = dsm_verify_lti_id_token((string) ($post['id_token'] ?? ''), $config, (string) $launchState['nonce']);
    $userId = dsm_upsert_lti_user($pdo, $claims);
    if ($userId !== null) {
        $pdo->prepare('UPDATE quiz_users SET last_login_at = CURRENT_TIMESTAMP WHERE id = :id')
            ->execute(['id' => $userId]);
        dsm_record_login_event($pdo, $userId, 'lti');
    }

    $contextClaim = 'https://purl.imsglobal.org/spec/lti/claim/context';
    $resourceClaim = 'https://purl.imsglobal.org/spec/lti/claim/resource_link';
    $deploymentClaim = 'https://purl.imsglobal.org/spec/lti/claim/deployment_id';
    $agsClaim = 'https://purl.imsglobal.org/spec/lti-ags/claim/endpoint';

    $lineitem = dsm_lti_nested_claim($claims, $agsClaim, 'lineitem');
    $_SESSION['lti_user'] = [
        'authenticated' => true,
        'student_user_id' => $userId,
        'canvas_user_id' => (string) ($claims['sub'] ?? ''),
        'student_identifier' => (string) ($claims['email'] ?? $claims['sub'] ?? ''),
        'display_name' => (string) ($claims['name'] ?? $claims['email'] ?? ''),
        'email' => (string) ($claims['email'] ?? ''),
        'lti_deployment_id' => (string) dsm_lti_claim($claims, $deploymentClaim, ''),
        'lti_context_id' => (string) dsm_lti_nested_claim($claims, $contextClaim, 'id', ''),
        'lti_resource_link_id' => (string) dsm_lti_nested_claim($claims, $resourceClaim, 'id', ''),
        'lti_lineitem_url' => is_string($lineitem) ? $lineitem : '',
    ];

    return (string) ($claims['https://purl.imsglobal.org/spec/lti/claim/target_link_uri']
        ?? $launchState['target_link_uri']
        ?? $config['lti']['default_target_link_uri']);
}

function dsm_current_lti_user(array $config): ?array
{
    dsm_start_lti_session($config);
    $user = $_SESSION['lti_user'] ?? null;
    return is_array($user) && !empty($user['authenticated']) ? $user : null;
}

function dsm_current_student_user(PDO $pdo, array $config): ?array
{
    $ltiUser = dsm_current_lti_user($config);
    if (is_array($ltiUser)) {
        return $ltiUser + ['auth_source' => 'lti'];
    }
    if (session_status() === PHP_SESSION_ACTIVE) {
        session_write_close();
        $_SESSION = [];
        session_id('');
    }

    dsm_start_student_session($config);
    $id = $_SESSION['student_user_id'] ?? null;
    if (!is_int($id) && !ctype_digit((string) $id)) {
        return null;
    }

    $stmt = $pdo->prepare(
        'SELECT id, email, display_name, role, status, canvas_user_id, student_identifier
         FROM quiz_users
         WHERE id = :id AND role = \'student\' AND status = \'active\'
         LIMIT 1'
    );
    $stmt->execute(['id' => (int) $id]);
    $student = $stmt->fetch();
    if (!is_array($student)) {
        return null;
    }

    return [
        'authenticated' => true,
        'student_user_id' => (int) $student['id'],
        'canvas_user_id' => (string) ($student['canvas_user_id'] ?? ''),
        'student_identifier' => (string) ($student['student_identifier'] ?: dsm_normalize_student_identifier((string) $student['email'])),
        'display_name' => (string) ($student['display_name'] ?? ''),
        'email' => (string) ($student['email'] ?? ''),
        'lti_deployment_id' => '',
        'lti_context_id' => '',
        'lti_resource_link_id' => '',
        'lti_lineitem_url' => '',
        'auth_source' => 'password',
    ];
}

function dsm_login_student(PDO $pdo, array $config, string $identifier, string $password): bool
{
    $identifier = trim($identifier);
    if ($identifier === '' || $password === '') {
        return false;
    }

    $student = dsm_find_student_for_login($pdo, $identifier);
    if (!is_array($student) || !password_verify($password, (string) $student['password_hash'])) {
        return false;
    }
    if (dsm_student_email_verification_required($config) && empty($student['email_verified_at'])) {
        return false;
    }

    dsm_start_fresh_student_session($config);
    $_SESSION['student_user_id'] = (int) $student['id'];
    $pdo->prepare('UPDATE quiz_users SET last_login_at = CURRENT_TIMESTAMP WHERE id = :id')
        ->execute(['id' => (int) $student['id']]);
    dsm_record_login_event($pdo, (int) $student['id'], 'password');
    return true;
}

function dsm_upsert_lti_user(PDO $pdo, array $claims): ?int
{
    $canvasUserId = (string) ($claims['sub'] ?? '');
    $email = trim((string) ($claims['email'] ?? ''));
    $studentIdentifier = dsm_normalize_student_identifier($email !== '' ? $email : $canvasUserId);
    $displayName = trim((string) ($claims['name'] ?? $email ?: $canvasUserId));

    if ($email === '' && $canvasUserId === '') {
        return null;
    }

    $where = $email !== ''
        ? '(LOWER(email) = LOWER(:email) OR LOWER(student_identifier) = LOWER(:student_identifier))'
        : '(canvas_user_id = :canvas_user_id OR LOWER(student_identifier) = LOWER(:student_identifier))';
    $stmt = $pdo->prepare('SELECT id, role FROM quiz_users WHERE ' . $where . ' LIMIT 1');
    $stmt->execute($email !== ''
        ? ['email' => $email, 'student_identifier' => $studentIdentifier]
        : ['canvas_user_id' => $canvasUserId, 'student_identifier' => $studentIdentifier]);
    $existing = $stmt->fetch();

    if (is_array($existing)) {
        if (($existing['role'] ?? '') === 'admin') {
            return null;
        }

        $update = $pdo->prepare(
            'UPDATE quiz_users
             SET display_name = :display_name,
                 canvas_user_id = :canvas_user_id,
                 student_identifier = :student_identifier,
                 status = \'active\'
             WHERE id = :id'
        );
        $update->execute([
            'display_name' => $displayName,
            'canvas_user_id' => $canvasUserId !== '' ? $canvasUserId : null,
            'student_identifier' => $studentIdentifier !== '' ? $studentIdentifier : null,
            'id' => (int) $existing['id'],
        ]);
        return (int) $existing['id'];
    }

    $insert = $pdo->prepare(
        'INSERT INTO quiz_users (email, display_name, role, password_hash, status, canvas_user_id, student_identifier)
         VALUES (:email, :display_name, \'student\', NULL, \'active\', :canvas_user_id, :student_identifier)'
    );
    $insert->execute([
        'email' => $email !== '' ? $email : $canvasUserId . '@lti.local',
        'display_name' => $displayName,
        'canvas_user_id' => $canvasUserId !== '' ? $canvasUserId : null,
        'student_identifier' => $studentIdentifier !== '' ? $studentIdentifier : null,
    ]);

    return (int) $pdo->lastInsertId();
}

function dsm_verify_lti_id_token(string $jwt, array $config, string $expectedNonce): array
{
    $parts = explode('.', $jwt);
    if (count($parts) !== 3) {
        throw new RuntimeException('Invalid LTI token shape.');
    }

    $header = dsm_json_decode_assoc(dsm_base64url_decode($parts[0]));
    $claims = dsm_json_decode_assoc(dsm_base64url_decode($parts[1]));
    if (($header['alg'] ?? '') !== 'RS256') {
        throw new RuntimeException('Unsupported LTI token algorithm.');
    }

    $publicKey = dsm_lti_public_key((string) ($header['kid'] ?? ''), (string) $config['lti']['jwks_url']);
    $signed = $parts[0] . '.' . $parts[1];
    $signature = dsm_base64url_decode($parts[2]);
    if (openssl_verify($signed, $signature, $publicKey, OPENSSL_ALGO_SHA256) !== 1) {
        throw new RuntimeException('Invalid LTI token signature.');
    }

    $now = time();
    if ((string) ($claims['iss'] ?? '') !== (string) $config['lti']['issuer']) {
        throw new RuntimeException('Invalid LTI token issuer.');
    }
    $aud = $claims['aud'] ?? null;
    $audiences = is_array($aud) ? $aud : [$aud];
    if (!in_array((string) $config['lti']['client_id'], array_map('strval', $audiences), true)) {
        throw new RuntimeException('Invalid LTI token audience.');
    }
    if ((int) ($claims['exp'] ?? 0) < $now) {
        throw new RuntimeException('Expired LTI token.');
    }
    if ((int) ($claims['iat'] ?? 0) > $now + 300) {
        throw new RuntimeException('Invalid LTI token issued-at time.');
    }
    if ((string) ($claims['nonce'] ?? '') !== $expectedNonce) {
        throw new RuntimeException('Invalid LTI token nonce.');
    }

    $deploymentId = (string) ($claims['https://purl.imsglobal.org/spec/lti/claim/deployment_id'] ?? '');
    $allowedDeployments = array_filter(array_map('strval', $config['lti']['deployment_ids'] ?? []));
    if ($allowedDeployments !== [] && !in_array($deploymentId, $allowedDeployments, true)) {
        throw new RuntimeException('Unexpected LTI deployment.');
    }

    return $claims;
}

function dsm_lti_public_key(string $kid, string $jwksUrl): string
{
    $jwks = dsm_fetch_jwks($jwksUrl);
    foreach (($jwks['keys'] ?? []) as $key) {
        if (($key['kid'] ?? '') === $kid && ($key['kty'] ?? '') === 'RSA') {
            return dsm_rsa_jwk_to_pem($key);
        }
    }
    throw new RuntimeException('LTI public key not found.');
}

function dsm_fetch_jwks(string $jwksUrl): array
{
    $cachePath = sys_get_temp_dir() . '/dsm_canvas_jwks_' . sha1($jwksUrl) . '.json';
    if (is_readable($cachePath) && filemtime($cachePath) !== false && filemtime($cachePath) > time() - 3600) {
        return dsm_json_decode_assoc((string) file_get_contents($cachePath));
    }

    $ch = curl_init($jwksUrl);
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_TIMEOUT => 15,
    ]);
    $body = curl_exec($ch);
    $status = (int) curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
    $error = curl_error($ch);
    curl_close($ch);

    if ($body === false || $status < 200 || $status >= 300) {
        throw new RuntimeException($error !== '' ? $error : 'Could not fetch Canvas JWKS.');
    }
    file_put_contents($cachePath, $body, LOCK_EX);
    return dsm_json_decode_assoc((string) $body);
}

function dsm_rsa_jwk_to_pem(array $jwk): string
{
    $modulus = dsm_base64url_decode((string) $jwk['n']);
    $exponent = dsm_base64url_decode((string) $jwk['e']);
    $rsaPublicKey = dsm_asn1_sequence(
        dsm_asn1_integer($modulus)
        . dsm_asn1_integer($exponent)
    );
    $publicKeyInfo = dsm_asn1_sequence(
        dsm_asn1_sequence(dsm_asn1_oid('1.2.840.113549.1.1.1') . dsm_asn1_null())
        . dsm_asn1_bit_string($rsaPublicKey)
    );
    return "-----BEGIN PUBLIC KEY-----\n"
        . chunk_split(base64_encode($publicKeyInfo), 64, "\n")
        . "-----END PUBLIC KEY-----\n";
}

function dsm_base64url_decode(string $value): string
{
    $decoded = base64_decode(strtr($value, '-_', '+/') . str_repeat('=', (4 - strlen($value) % 4) % 4), true);
    if ($decoded === false) {
        throw new RuntimeException('Invalid base64url value.');
    }
    return $decoded;
}

function dsm_json_decode_assoc(string $json): array
{
    $decoded = json_decode($json, true);
    if (!is_array($decoded)) {
        throw new RuntimeException('Invalid JSON.');
    }
    return $decoded;
}

function dsm_random_token(): string
{
    return bin2hex(random_bytes(24));
}

function dsm_asn1_length(int $length): string
{
    if ($length < 128) {
        return chr($length);
    }
    $out = '';
    while ($length > 0) {
        $out = chr($length & 0xff) . $out;
        $length >>= 8;
    }
    return chr(0x80 | strlen($out)) . $out;
}

function dsm_asn1_sequence(string $value): string
{
    return "\x30" . dsm_asn1_length(strlen($value)) . $value;
}

function dsm_asn1_integer(string $value): string
{
    if ($value !== '' && (ord($value[0]) & 0x80)) {
        $value = "\x00" . $value;
    }
    return "\x02" . dsm_asn1_length(strlen($value)) . $value;
}

function dsm_asn1_oid(string $oid): string
{
    $parts = array_map('intval', explode('.', $oid));
    $body = chr(40 * $parts[0] + $parts[1]);
    for ($i = 2; $i < count($parts); $i++) {
        $value = $parts[$i];
        $bytes = chr($value & 0x7f);
        while ($value >>= 7) {
            $bytes = chr(($value & 0x7f) | 0x80) . $bytes;
        }
        $body .= $bytes;
    }
    return "\x06" . dsm_asn1_length(strlen($body)) . $body;
}

function dsm_asn1_null(): string
{
    return "\x05\x00";
}

function dsm_asn1_bit_string(string $value): string
{
    return "\x03" . dsm_asn1_length(strlen($value) + 1) . "\x00" . $value;
}

function dsm_current_admin(PDO $pdo): ?array
{
    $id = $_SESSION['admin_user_id'] ?? null;
    if (!is_int($id) && !ctype_digit((string) $id)) {
        return null;
    }

    $stmt = $pdo->prepare(
        'SELECT id, email, display_name, role, status
         FROM quiz_users
         WHERE id = :id AND role = \'admin\' AND status = \'active\'
         LIMIT 1'
    );
    $stmt->execute(['id' => (int) $id]);
    $admin = $stmt->fetch();
    return is_array($admin) ? $admin : null;
}

function dsm_login_admin(PDO $pdo, string $email, string $password): bool
{
    $stmt = $pdo->prepare(
        'SELECT id, password_hash
         FROM quiz_users
         WHERE LOWER(email) = LOWER(:email) AND role = \'admin\' AND status = \'active\'
         LIMIT 1'
    );
    $stmt->execute(['email' => trim($email)]);
    $admin = $stmt->fetch();
    if (!is_array($admin) || !password_verify($password, (string) $admin['password_hash'])) {
        return false;
    }

    $_SESSION['admin_user_id'] = (int) $admin['id'];
    $pdo->prepare('UPDATE quiz_users SET last_login_at = CURRENT_TIMESTAMP WHERE id = :id')
        ->execute(['id' => (int) $admin['id']]);
    dsm_record_login_event($pdo, (int) $admin['id'], 'admin');
    return true;
}

function dsm_h(mixed $value): string
{
    return htmlspecialchars((string) $value, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
}

function dsm_admin_nav(string $active): string
{
    $items = [
        'attempts' => ['/api/admin/', 'Attempts'],
        'report' => ['/api/admin/report.php', 'Score Report'],
        'users' => ['/api/admin/users.php', 'Users'],
        'assignments' => ['/api/admin/assignments.php', 'Assignments'],
        'export' => ['/api/admin/export.csv.php', 'Export CSV'],
        'logout' => ['/api/admin/logout.php', 'Log out'],
    ];

    $links = '';
    foreach ($items as $key => [$href, $label]) {
        $class = 'admin-topnav-link' . ($key === $active ? ' active' : '');
        if ($key === 'logout') {
            $links .= '<a class="' . dsm_h($class . ' icon-link') . '" href="' . dsm_h($href) . '" aria-label="Log out" title="Log out">'
                . '<svg class="account-icon" aria-hidden="true" viewBox="0 0 24 24" focusable="false">'
                . '<path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4Z"></path>'
                . '<path d="M4 20c0-3.31 3.58-6 8-6s8 2.69 8 6v1H4v-1Z"></path>'
                . '</svg>'
                . '<span class="sr-only">Log out</span></a>';
            continue;
        }
        $links .= '<a class="' . dsm_h($class) . '" href="' . dsm_h($href) . '">' . dsm_h($label) . '</a>';
    }

    return '<header class="admin-topnav"><div class="admin-topnav-inner">'
        . '<a class="admin-topnav-brand" href="/api/admin/">DSM Admin</a>'
        . '<nav aria-label="Admin">' . $links . '</nav>'
        . '</div></header>';
}

function dsm_admin_nav_css(): string
{
    return '
.admin-topnav { position: sticky; top: 0; z-index: 100; background: #fff; border-bottom: 1px solid #d8dee4; box-shadow: 0 1px 2px rgba(31, 35, 40, 0.04); }
.admin-topnav-inner { max-width: 1180px; margin: 0 auto; padding: 10px 32px; display: flex; align-items: center; justify-content: space-between; gap: 16px; }
.admin-topnav-brand { color: #24292f; font-weight: 800; text-decoration: none; white-space: nowrap; }
.admin-topnav nav { display: flex; flex-wrap: wrap; gap: 6px; justify-content: flex-end; }
.admin-topnav-link { display: inline-flex; align-items: center; min-height: 34px; padding: 6px 10px; border-radius: 6px; color: #0969da; font-weight: 700; text-decoration: none; }
.admin-topnav-link.icon-link { justify-content: center; width: 34px; padding: 6px; }
.account-icon { width: 20px; height: 20px; fill: currentColor; }
.sr-only { position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0, 0, 0, 0); white-space: nowrap; border: 0; }
.admin-topnav-link:hover, .admin-topnav-link:focus { background: #f6f8fa; outline: none; }
.admin-topnav-link.active { background: #0969da; color: #fff; }
@media (max-width: 760px) { .admin-topnav-inner { align-items: flex-start; flex-direction: column; padding: 10px 16px; } .admin-topnav nav { justify-content: flex-start; } }
';
}
