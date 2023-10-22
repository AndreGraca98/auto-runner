#!/usr/bin/env python

import argparse
import subprocess
from datetime import datetime
from pathlib import Path

try:
    from animations import SimpleAnimation
except ImportError:
    import time
    import warnings

    _t = "Missing animations module. Please install it with: "
    _t += "pip install git+https://github.com/AndreGraca98/console-animations.git . "
    _t += "Running without loading animations..."
    warnings.warn(_t)

    class SimpleAnimation:
        def __init__(self, *args, **kwargs):
            pass

        def run(self, *args, **kwargs):
            return print(*args, kwargs, end="\r") or time.sleep(5)


try:
    from cron_converter import Cron
except ImportError as e:
    _t = "Missing crontab module https://pypi.org/project/cron-converter/ "
    _t += "Please install it with: pip install cron-converter"
    raise ImportError(_t) from e

CRONTAB = "*/10 * * * *"  # Every 10min
LOGFILE = str(Path.cwd() / ".auto-runner.log")
EXAMPLE = """
Example:
    auto-runner --tab '*/15 * * * *' --log my-log-file.log
    auto-runner -ql --cmd 'make coverage'
Cron time examples:
    Every 5 minutes: \t*/5 * * * *
    Hourly: \t\t0 * * * *
"""


def get_parser():
    parser = argparse.ArgumentParser(description="Auto runner")
    parser.add_argument("cmd", type=str, help="Command to run")
    parser.add_argument(
        "-t",
        "--tab",
        type=str,
        dest="tab",
        default=CRONTAB,
        help="The time schedule in crontab format",
    )
    parser.add_argument(
        "-l",
        "--log",
        nargs="?",
        type=str,
        dest="logfile",
        const=LOGFILE,
        default=None,
        help="Log file to write the output",
    )
    parser.add_argument(
        "-e",
        "--example",
        "--examples",
        action="store_true",
        dest="examples",
        help="Show some examples of how to run and exit",
    )
    parser.add_argument(
        "-q", "--quiet", action="store_true", dest="quiet", help="Run in quiet mode"
    )
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    if args.examples:
        print(EXAMPLE)
        return

    # Creates the cron object from the crontab string
    cron = Cron(args.tab)

    animation = SimpleAnimation(wait_time=0.25, chars=["|", "/", "-", "\\"])

    schedule = cron.schedule(datetime.now())
    next_time = schedule.next()

    while True:
        if datetime.now() < next_time:
            animation.run(post_text=f" Next run at: {next_time}")
            continue

        print(f"Running: {args.cmd!r}".ljust(120), end="\r")
        out = subprocess.run(args.cmd, shell=True, capture_output=args.quiet)

        if args.logfile is not None:
            with open(args.logfile, "a+") as logfile:
                logfile.write(f"{datetime.now()}: {args.cmd}\n")
                if out.stderr is not None:
                    logfile.write(out.stderr.decode())
                if out.stdout is not None:
                    logfile.write(out.stdout.decode())

        next_time = schedule.next()


if __name__ == "__main__":
    main()
