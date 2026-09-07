console.log("Custom JS loaded!");

// ---- SINGLE DOMContentLoaded handler ----
document.addEventListener('DOMContentLoaded', function () {
    console.log("DOM ready!");

    // pydata-sphinx-theme renders two toggle buttons per side (a mobile
    // navbar icon and a desktop article-toolbar icon, sharing the same
    // classes), but its own click handler only binds to the first match
    // via document.querySelector(".primary-toggle" / ".secondary-toggle").
    // Whichever button is visible at the other breakpoint is dead.
    //
    // Past versions of this file reimplemented the toggle by hand
    // (flipping a #pst-*-sidebar-checkbox and a body class). A theme
    // upgrade replaced that checkbox+CSS mechanism with a <dialog>-based
    // modal (content is moved into the dialog and .showModal() is
    // called), so that checkbox no longer exists and the old override
    // silently did nothing. Reimplementing the new dialog mechanism by
    // hand would just rot again on the next theme upgrade. Instead,
    // forward clicks from every extra matching button to the one button
    // the theme already wired correctly, whatever its handler does.
    function proxyExtraToggleButtons(selector) {
        var buttons = document.querySelectorAll(selector);
        if (buttons.length < 2) return;
        var primary = buttons[0];
        for (var i = 1; i < buttons.length; i++) {
            buttons[i].addEventListener('click', function (event) {
                event.preventDefault();
                primary.click();
            });
        }
    }

    proxyExtraToggleButtons('button.sidebar-toggle.primary-toggle');
    proxyExtraToggleButtons('button.sidebar-toggle.secondary-toggle');

    // At 900-991.98px the theme falls back to opening the sidebar as a
    // full-viewport modal <dialog> (see shared.css's notes on this range)
    // instead of the plain show/hide it uses at >=992px -- there is no
    // collapsed state at this width without this intercept, only
    // "docked" or "modal open". Capture the click before the theme's own
    // capturing-phase listener (registration order decides the race;
    // this script runs after the theme's, per Sphinx's html_js_files
    // ordering, so registering our OWN capture listener here still wins
    // because it is attached in this same synchronous pass, ahead of
    // where the theme would otherwise intercept -- verified live with
    // real Chrome before shipping) and toggle the same
    // `.pst-sidebar-hidden` class the >=992px mechanism already uses,
    // so this width band gets a real collapse instead of a modal
    // takeover. See ai_shared/memory/projects/pst_sidebar_toggle_bug.md.
    function interceptHalfScreenPrimaryToggle() {
        document.querySelectorAll('button.sidebar-toggle.primary-toggle').forEach(function (button) {
            button.addEventListener('click', function (event) {
                var isHalfScreenDesktop = window.matchMedia('(min-width: 900px) and (max-width: 991.98px)').matches;
                if (!isHalfScreenDesktop) return;
                event.preventDefault();
                event.stopImmediatePropagation();
                var sidebar = document.getElementById('pst-primary-sidebar');
                if (sidebar) sidebar.classList.toggle('pst-sidebar-hidden');
            }, true);
        });
    }

    interceptHalfScreenPrimaryToggle();

    // Convert appendix chapter numbers to letters (A, B, C ...).
    function toAppendixLetter(n) {
        return String.fromCharCode(64 + parseInt(n, 10));
    }

    function convertAppendixNumber(text) {
        return text.replace(/^(\d+)(\.)/, function (_, n, dot) {
            return toAppendixLetter(n) + dot;
        });
    }

    // Sidebar links under the "Appendices" caption render as plain "1. Title".
    document.querySelectorAll('nav.bd-links .caption-text').forEach(function (caption) {
        if (caption.textContent.trim() !== 'Appendices') return;
        var ul = caption.closest('p').nextElementSibling;
        if (!ul) return;
        ul.querySelectorAll('a.reference').forEach(function (a) {
            a.childNodes.forEach(function (node) {
                if (node.nodeType === Node.TEXT_NODE) {
                    node.textContent = convertAppendixNumber(node.textContent);
                }
            });
        });
    });

    var onAppendixPage = false;
    document.querySelectorAll('nav.bd-links .caption-text').forEach(function (caption) {
        if (caption.textContent.trim() !== 'Appendices') return;
        var ul = caption.closest('p').nextElementSibling;
        if (ul && ul.classList.contains('current')) {
            onAppendixPage = true;
        }
    });

    if (onAppendixPage) {
        document.querySelectorAll('.section-number').forEach(function (span) {
            span.textContent = convertAppendixNumber(span.textContent);
        });

        var headingSectionNumber = document.querySelector('h1 .section-number');
        var appendixLetterMatch = headingSectionNumber && headingSectionNumber.textContent.match(/^([A-Z])\./);
        if (appendixLetterMatch) {
            var appendixLetter = appendixLetterMatch[1];
            var figureLabelsByHash = {};
            var figureCount = 0;

            document.querySelectorAll('figure[id] figcaption .caption-number').forEach(function (span) {
                if (!span.textContent.trim().match(/^Fig\./)) return;
                var figure = span.closest('figure[id]');
                if (!figure) return;

                figureCount += 1;
                var label = 'Fig. ' + appendixLetter + '.' + figureCount;
                span.textContent = label + ' ';
                figureLabelsByHash['#' + figure.id] = label;
            });

            document.querySelectorAll('a.reference.internal[href] .std-numref').forEach(function (span) {
                var link = span.closest('a.reference.internal[href]');
                var url;
                try {
                    url = new URL(link.getAttribute('href'), window.location.href);
                } catch (e) {
                    return;
                }
                if (url.pathname !== window.location.pathname) return;
                if (!figureLabelsByHash[url.hash]) return;
                span.textContent = figureLabelsByHash[url.hash];
            });
        }

        document.querySelectorAll('.left-prev[href], .right-next[href]').forEach(function (a) {
            if (!a.href.includes('/appendices/')) return;
            a.querySelectorAll('.section-number').forEach(function (span) {
                span.textContent = convertAppendixNumber(span.textContent);
            });
        });
    }

    // -----------------------------------------------------------
    // Aftermatter: promote Bibliography and Index sidebar entries
    // from toctree-l1 links to caption-level links (no nesting).
    // Replaces p.caption + ul pair with a single <a> element.
    // -----------------------------------------------------------
    ['Bibliography', 'Index'].forEach(function (name) {
        document.querySelectorAll('nav.bd-links .caption-text').forEach(function (span) {
            if (span.textContent.trim() !== name) return;
            var caption = span.closest('p.caption');
            if (!caption) return;
            var ul = caption.nextElementSibling;
            if (!ul) return;
            var link = ul.querySelector('li > a');
            if (!link) return;

            var a = document.createElement('a');
            a.href = link.href;
            a.textContent = name;
            a.className = 'bd-aftermatter-link';
            if (link.target) a.target = link.target;
            if (link.rel) a.rel = link.rel;

            caption.parentNode.insertBefore(a, caption);
            caption.remove();
            ul.remove();
        });
    });

    // Fix spacing: first aftermatter link gets separation; subsequent ones sit tight
    document.querySelectorAll('a.bd-aftermatter-link').forEach(function (link, i) {
        link.style.marginTop = i === 0 ? '0.5rem' : '0.1rem';
    });

    // -----------------------------------------------------------
    // Assignment answer locking
    //
    // Pages can include:
    //   <div data-assignment-answers="ch02-lab"></div>
    // The admin database setting controls whether hide-input answer
    // cells are visible. The old timestamp marker remains as a fallback.
    // -----------------------------------------------------------
    function answerLockMarker() {
        return document.querySelector('[data-assignment-answers]')
            || document.querySelector('[data-lab-answers-release-at]');
    }

    function assignmentIdFromPath() {
        var match = window.location.pathname.match(/\/chapters\/(\d+)-[^/]+\/assignments\/(preview|lab|homework)\.html$/);
        if (!match) return '';
        return 'ch' + match[1] + '-' + match[2];
    }

    function answerCells() {
        return document.querySelectorAll('.tag_hide-input');
    }

    function ensureAnswerLockNotice(marker, message) {
        var notice = document.querySelector('.lab-answer-lock-notice');
        if (!notice) {
            notice = document.createElement('div');
            notice.className = 'lab-answer-lock-notice';
            marker.after(notice);
        }
        notice.textContent = message;
    }

    function lockAnswerCells(marker, message) {
        document.body.classList.add('lab-answers-locked');
        ensureAnswerLockNotice(marker, message);
        answerCells().forEach(function (cell) {
            cell.classList.add('lab-answer-locked');
            cell.setAttribute('aria-disabled', 'true');
            cell.querySelectorAll('details').forEach(function (details) {
                details.removeAttribute('open');
            });
            cell.querySelectorAll('summary').forEach(function (summary) {
                summary.setAttribute('aria-disabled', 'true');
            });
        });
    }

    function unlockAnswerCells() {
        document.body.classList.remove('lab-answers-locked');
        var notice = document.querySelector('.lab-answer-lock-notice');
        if (notice) notice.remove();
        answerCells().forEach(function (cell) {
            cell.classList.remove('lab-answer-locked');
            cell.removeAttribute('aria-disabled');
            cell.querySelectorAll('summary').forEach(function (summary) {
                summary.removeAttribute('aria-disabled');
            });
        });
        answerCells().forEach(watchExerciseCell);
    }

    function applyTimestampGate(marker) {
        var releaseValue = marker.getAttribute('data-lab-answers-release-at');
        var releaseTime = Date.parse(releaseValue || '');
        if (!releaseTime || Number.isNaN(releaseTime)) return false;
        if (Date.now() >= releaseTime) return false;

        lockAnswerCells(marker, 'Answers unlock after the lab due date.');
        return true;
    }

    function applyAnswerUnlockGate() {
        var marker = answerLockMarker();
        if (!marker) return false;

        var assignmentId = marker.getAttribute('data-assignment-answers') || assignmentIdFromPath();
        if (assignmentId) {
            lockAnswerCells(marker, 'Checking answer availability.');
            fetch('/api/v1/assignment-settings.php?assignment_id=' + encodeURIComponent(assignmentId), {
                credentials: 'same-origin',
                cache: 'no-store',
            })
                .then(function (response) {
                    if (response.status === 404) return { ok: false, unknown_assignment: true };
                    if (!response.ok) throw new Error('settings unavailable');
                    return response.json();
                })
                .then(function (payload) {
                    if (payload && payload.ok && payload.answers_unlocked) {
                        unlockAnswerCells();
                    } else if (payload && payload.unknown_assignment) {
                        if (!applyTimestampGate(marker)) {
                            unlockAnswerCells();
                        }
                    } else {
                        lockAnswerCells(marker, 'Answers are locked by your instructor.');
                    }
                })
                .catch(function () {
                    if (marker.hasAttribute('data-lab-answers-release-at')) {
                        if (!applyTimestampGate(marker)) {
                            unlockAnswerCells();
                        }
                        return;
                    }
                    lockAnswerCells(marker, 'Answers are locked until your instructor unlocks them.');
                });
            return true;
        }

        return applyTimestampGate(marker);
    }

    var labAnswersLocked = applyAnswerUnlockGate();

    // -----------------------------------------------------------
    // FIX A: tag_hide-input (exercise answer) cells
    //
    // Thebe wraps the entire .thebelab-cell inside <details>, hiding
    // everything. We watch each cell and move the jp-OutputArea wrapper
    // outside <details> the instant Thebe creates it.
    // -----------------------------------------------------------
    // // Thebe activation detection: watch for .thebelab-cell to be created inside <details>, then move output.
    function moveOutputOutsideDetails(cell) {
        var details = cell.querySelector('details');
        if (!details) return;
        var thebelabCell = details.querySelector('.thebelab-cell');
        if (!thebelabCell) return;

        var outputWrapper = null;
        thebelabCell.querySelectorAll(':scope > div').forEach(function (div) {
            if (div.querySelector('.jp-OutputArea')) outputWrapper = div;
        });

        if (outputWrapper && !outputWrapper.dataset.movedOut) {
            outputWrapper.dataset.movedOut = '1';
            details.after(outputWrapper);
            console.log("[fix A] Moved output outside <details> for", cell.id);
        }
    }

    function watchExerciseCell(cell) {
        var details = cell.querySelector('details');
        if (!details) return;

        var observer = new MutationObserver(function () {
            var thebelabCell = details.querySelector('.thebelab-cell');
            if (!thebelabCell) return;

            var outputObserver = new MutationObserver(function () {
                var outputWrapper = null;
                thebelabCell.querySelectorAll(':scope > div').forEach(function (div) {
                    if (div.querySelector('.jp-OutputArea')) outputWrapper = div;
                });
                if (outputWrapper && !outputWrapper.dataset.movedOut) {
                    outputWrapper.dataset.movedOut = '1';
                    details.after(outputWrapper);
                    console.log("[fix A] (delayed) Moved output outside <details> for", cell.id);
                    outputObserver.disconnect();
                }
            });
            outputObserver.observe(thebelabCell, { childList: true, subtree: true });
            moveOutputOutsideDetails(cell);
            observer.disconnect();
        });

        observer.observe(details, { childList: true, subtree: true });
    }

    if (!labAnswersLocked) {
        document.querySelectorAll('.tag_hide-input').forEach(watchExerciseCell);
    }

    // -----------------------------------------------------------
    // FIX B: Demo cells — hide jp-OutputArea when Thebe activates.
    //
    // Since body.thebelab-active is never set by Thebe 0.8.2,
    // we detect activation by watching for the first
    // .thebelab-run-button to appear in the DOM, then add our own
    // class 'thebe-is-active' to body so CSS can target it.
    //
    // NOTE: thinkpy uses predefinedOutput: true (default), so
    // static outputs are visible. No Fix A needed — exercise cell
    // outputs are not hidden by Thebe in this config.
    // -----------------------------------------------------------

    var thebeActivated = false;

    var activationObserver = new MutationObserver(function () {
        if (thebeActivated) return;
        if (document.querySelector('.thebelab-run-button')) {
            thebeActivated = true;
            activationObserver.disconnect();
            document.body.classList.add('thebe-is-active');
            console.log("[fix B] Thebe detected — added thebe-is-active to body");

            // Bind directly to every run button now that they exist
            document.querySelectorAll('.thebelab-run-button').forEach(function (btn) {
                btn.addEventListener('click', function () {
                    var cell = btn.closest('.cell');
                    if (cell && !cell.classList.contains('tag_hide-input')) {
                        cell.classList.add('cell-has-run');
                        console.log("[fix B] Marked cell-has-run for", cell.id);
                    }
                });
            });
        }
    });
    activationObserver.observe(document.body, { childList: true, subtree: true });

    // Exercise counter labels
    const exercises = document.querySelectorAll('div.cell.tag_thebe-interactive');
    const total = exercises.length;

    exercises.forEach((exercise, index) => {
        // Skip if label already exists
        if (exercise.querySelector('.exercise-label')) return;

        const counter = index + 1;
        const isAssignmentPage = /\/assignments\/(homework|lab)\.html/.test(window.location.pathname);
        const sourceText = exercise.textContent || '';
        const questionMatch = sourceText.match(/###\s+(?:Question\s+)?(\d+)[.:]?\s*([^\n]*)/);
        const label = document.createElement('div');
        label.className = 'exercise-label';
        if (isAssignmentPage && questionMatch) {
            const questionTitle = questionMatch[2].trim();
            label.innerHTML = `<span class="exercise-question-title">${questionMatch[1]}. ${questionTitle}</span><br><span class="exercise-count">✏️ Interactive Exercise ${counter}/${total}</span>`;
        } else {
            label.innerHTML = `✏️ Interactive Exercise ${counter}/${total}`;
        }
        label.style.cssText = `
            display: block;
            margin-bottom: 8px;
        `;
        exercise.insertBefore(label, exercise.firstChild);
    });
});

// Same-page sign-in/sign-up modal. Links still work as normal pages without JS.
function ensureAuthModal() {
    var existing = document.querySelector('.bd-auth-modal');
    if (existing) return existing;

    var modal = document.createElement('div');
    modal.className = 'bd-auth-modal';
    modal.hidden = true;
    modal.innerHTML = [
        '<div class="bd-auth-modal-backdrop" data-auth-close></div>',
        '<div class="bd-auth-modal-dialog" role="dialog" aria-modal="true" aria-labelledby="bd-auth-modal-title">',
        '  <div class="bd-auth-modal-header">',
        '    <h2 id="bd-auth-modal-title">Course sign in</h2>',
        '    <button type="button" class="bd-auth-modal-close" data-auth-close aria-label="Close sign-in dialog">×</button>',
        '  </div>',
        '  <iframe class="bd-auth-modal-frame" title="Course sign-in form"></iframe>',
        '</div>'
    ].join('');
    document.body.appendChild(modal);

    modal.addEventListener('click', function (event) {
        if (event.target.hasAttribute('data-auth-close')) closeAuthModal();
    });

    return modal;
}

function closeAuthModal() {
    var modal = document.querySelector('.bd-auth-modal');
    if (!modal) return;
    modal.hidden = true;
    var frame = modal.querySelector('.bd-auth-modal-frame');
    if (frame) frame.removeAttribute('src');
    document.body.classList.remove('bd-auth-modal-open');
}

function openAuthModal(url, title) {
    var modal = ensureAuthModal();
    var heading = modal.querySelector('#bd-auth-modal-title');
    var frame = modal.querySelector('.bd-auth-modal-frame');
    var accountButton = document.querySelector('.bd-student-header');
    if (heading) heading.textContent = title || 'Course sign in';
    if (accountButton) {
        var rect = accountButton.getBoundingClientRect();
        modal.style.setProperty('--bd-auth-left', Math.max(8, rect.right + 8) + 'px');
        modal.style.setProperty('--bd-auth-bottom', Math.max(8, window.innerHeight - rect.bottom) + 'px');
    }
    if (frame) {
        var separator = url.indexOf('?') === -1 ? '?' : '&';
        frame.src = url + separator + 'modal=1';
    }
    modal.hidden = false;
    document.body.classList.add('bd-auth-modal-open');
}

function bindAuthModal(link, title) {
    link.addEventListener('click', function (event) {
        if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
        event.preventDefault();
        openAuthModal(link.href, title);
    });
}

window.addEventListener('message', function (event) {
    if (event.origin !== window.location.origin) return;
    var data = event.data || {};
    if (data.source !== 'think-book-auth' || data.type !== 'auth-success') return;
    closeAuthModal();
    window.location.reload();
});

document.addEventListener('keydown', function (event) {
    if (event.key === 'Escape') closeAuthModal();
});

// Add student account panel at the bottom of the left sidebar.
function getAccountInitials(identity) {
    var value = '';
    if (identity) {
        value = identity.display_name || identity.email || identity.student_identifier || '';
    }
    value = String(value).trim();
    if (!value) return '';

    if (value.indexOf('@') !== -1) {
        value = value.split('@')[0];
    }

    var parts = value
        .replace(/[^a-zA-Z0-9\s._-]/g, ' ')
        .split(/[\s._-]+/)
        .filter(Boolean);

    if (parts.length >= 2) {
        return (parts[0][0] + parts[1][0]).toUpperCase();
    }
    return value.slice(0, 2).toUpperCase();
}

function addStudentAccountPanel() {
    var nav = document.querySelector('nav.bd-links');
    if (!nav) return;
    if (nav.querySelector('.bd-student-links')) return;

    var currentPath = window.location.pathname + window.location.search + window.location.hash;
    var wrapper = document.createElement('div');
    wrapper.className = 'bd-student-links';

    var header = document.createElement('button');
    header.type = 'button';
    header.className = 'bd-student-header';
    header.setAttribute('aria-expanded', 'false');
    header.setAttribute('aria-label', 'Student account menu');

    var avatar = document.createElement('div');
    avatar.className = 'bd-student-avatar';

    header.appendChild(avatar);
    wrapper.appendChild(header);

    var actions = document.createElement('div');
    actions.className = 'bd-student-actions';

    var login = document.createElement('a');
    login.className = 'bd-student-button';
    login.href = '/api/student/login.php?next=' + encodeURIComponent(currentPath);
    login.textContent = 'Sign in';

    var signup = document.createElement('a');
    signup.className = 'bd-student-button';
    signup.href = '/api/student/login.php?next=' + encodeURIComponent(currentPath) + '&tab=signup';
    signup.textContent = 'Sign up';
    bindAuthModal(login, 'Course sign in');
    bindAuthModal(signup, 'Course sign up');

    actions.appendChild(login);
    actions.appendChild(signup);
    wrapper.appendChild(actions);

    header.addEventListener('click', function () {
        var isOpen = wrapper.classList.toggle('is-open');
        header.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });
    nav.appendChild(wrapper);

    fetch('/api/v1/session.php', { credentials: 'same-origin' })
        .then(function (response) { return response.ok ? response.json() : null; })
        .then(function (payload) {
            if (!payload || !payload.authenticated || !payload.identity) return;

            var initials = getAccountInitials(payload.identity);
            if (initials) {
                avatar.textContent = initials;
                avatar.classList.add('has-initials');
            }

            if (payload.role === 'admin') {
                var adminLogoutPath = '/api/admin/logout.php?next=' + encodeURIComponent(currentPath);
                var adminLinks = [
                    ['Attempts', '/api/admin/'],
                    ['Score Report', '/api/admin/report.php'],
                    ['Users', '/api/admin/users.php'],
                    ['Assignments', '/api/admin/assignments.php'],
                    ['Log out', adminLogoutPath, false],
                ].map(function (item) {
                    var link = document.createElement('a');
                    link.className = 'bd-student-button';
                    link.href = item[1];
                    link.textContent = item[0];
                    if (item[2] !== false) {
                        link.target = '_blank';
                        link.rel = 'noopener';
                    }
                    return link;
                });
                actions.replaceChildren.apply(actions, adminLinks);
                return;
            }

            var account = document.createElement('a');
            account.className = 'bd-student-button';
            account.href = '/api/student/account.php';
            account.target = '_blank';
            account.rel = 'noopener';
            account.textContent = 'Account';

            var scores = document.createElement('a');
            scores.className = 'bd-student-button';
            scores.href = '/api/student/scores.php';
            scores.target = '_blank';
            scores.rel = 'noopener';
            scores.textContent = 'My Scores';

            var logout = document.createElement('a');
            logout.className = 'bd-student-button';
            logout.href = '/api/student/logout.php?next=' + encodeURIComponent(currentPath);
            logout.textContent = 'Log out';

            actions.replaceChildren(account, scores, logout);
        })
        .catch(function () {});
}

function markExerciseQuestionCards() {
    const isAssignmentPage = /\/assignments\/(homework|lab)\.html/.test(window.location.pathname);
    const exerciseCells = document.querySelectorAll('.cell.tag_thebe-interactive');

    if (!isAssignmentPage && exerciseCells.length === 0) {
        return;
    }

    document.body.classList.add('bd-exercise-card-page');
    if (isAssignmentPage) {
        document.body.classList.add('bd-assignment-card-page');
    }

    function wrapQuestionElement(element) {
        if (element.parentElement && element.parentElement.classList.contains('bd-exercise-question-card')) {
            return;
        }

        var card = document.createElement('div');
        card.className = 'bd-exercise-question-card bd-assignment-question-card';
        element.parentNode.insertBefore(card, element);
        card.appendChild(element);

        var next = card.nextElementSibling;
        if (next && next.classList.contains('cell') && next.classList.contains('tag_hide-input')) {
            card.appendChild(next);
        }
    }

    function removeRenderedQuestionTitle(cell) {
        if (!isAssignmentPage) {
            return;
        }

        cell.querySelectorAll('.cell_input pre').forEach(function (pre) {
            if (pre.dataset.assignmentTitleRemoved === 'true') {
                return;
            }

            var lines = pre.textContent.split('\n');
            if (lines.length === 0 || !/^###\s+(?:Question\s+)?\d+[.:]?\s*/.test(lines[0])) {
                return;
            }

            pre.textContent = lines.slice(1).join('\n');
            pre.dataset.assignmentTitleRemoved = 'true';
        });
    }

    document.querySelectorAll('.tf-options').forEach(function (options) {
        if (!isAssignmentPage) {
            return;
        }
        var element = options.closest('.assignment-question-card') || options.closest('.cell');
        if (element) {
            wrapQuestionElement(element);
        }
    });

    exerciseCells.forEach(function (cell) {
        removeRenderedQuestionTitle(cell);
        wrapQuestionElement(cell);
    });
}

document.addEventListener('DOMContentLoaded', function () {
    markExerciseQuestionCards();
    addStudentAccountPanel();

    var sidebar = document.querySelector('.bd-sidebar-primary');
    if (!sidebar || sidebar.querySelector('.bd-student-links')) return;

    var accountObserver = new MutationObserver(function () {
        addStudentAccountPanel();
        if (sidebar.querySelector('.bd-student-links')) {
            accountObserver.disconnect();
        }
    });
    accountObserver.observe(sidebar, { childList: true, subtree: true });
});
