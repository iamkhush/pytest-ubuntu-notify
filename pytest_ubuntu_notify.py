# -*- coding: utf-8 -*-

import pytest
import subprocess


def pytest_addoption(parser):
    group = parser.getgroup('ubuntu-notify')
    group.addoption(
        '--ubuntu-notify',
        dest='ubuntu_notification',
        default='True',
        help='Enable notifications on Ubuntu'
    )


def pytest_sessionstart(session):
    if session.config.option.ubuntu_notification:
        subprocess.run(["notify-send", 'py.test', 'Running tests...', '-t', '10'])


def pytest_terminal_summary(terminalreporter):
    if not terminalreporter.config.option.ubuntu_notification:
        return
    tr = terminalreporter
    passes = len(tr.stats.get('passed', []))
    fails = len(tr.stats.get('failed', []))
    skips = len(tr.stats.get('deselected', []))
    errors = len(tr.stats.get('error', []))
    if errors + passes + fails + skips == 0:
        msg = 'No tests ran'
    elif passes and not (fails or errors):
        msg = 'Success - %i Passed' % passes
    elif not (skips or errors):
        msg = '%s Passed %s Failed' % (passes, fails)
    else:
        msg = '%s Passed %s Failed %s Errors %s Skipped' % (
            passes, fails, errors, skips
        )
    subprocess.run(["notify-send", 'py.test', msg, '-t', '10'])


