# Auto Runner

![badge](https://img.shields.io/github/v/tag/AndreGraca98/auto-runner?logo=python&logoColor=yellow&label=version)

The `auto-runner` script allows you to run a command on a schedule using cron notation. This is especially useful if you have a recurring task that you need to run without manually triggering it.

## Requirements

- Python 3 (tested with Python 3.11)
- cron-converter package `pip install cron-converter`
- console animations package `pip install git+https://github.com/AndreGraca98/console-animations.git` ([Check this repo](https://github.com/AndreGraca98/console-animations))

## Installation

```bash
pip install git+https://github.com/AndreGraca98/auto-runner.git
```

## Usage

To use the `auto-runner` script, simply specify the command to run and the time schedule in crontab format. You can also choose to output the command's output to a log file.

### Examples

Run `make coverage` every hour and output the log to `my-log-file.log`.

```bash
auto-runner 'make coverage' --tab '0 * * * *' --log my-log-file.log --quiet 
```

Run `pytest` every 5 minutes

```bash
auto-runner 'pytest' --tab '*/5 * * * *' 
```

## Command-line arguments

```bash
usage: auto-runner [-h] [-t TAB] [-l [LOGFILE]] [-e] [-q] cmd

Auto runner

positional arguments:
  cmd                   Command to run

optional arguments:
  -h, --help            show this help message and exit
  -t TAB, --tab TAB     The time schedule in crontab format
                        (default: */10 * * * *)
  -l [LOGFILE], --log [LOGFILE]
                        Log file to write the output. (default: None)
  -e, --example, --examples
                        Show some examples of how to run and exit
  -q, --quiet           Run in quiet mode (default: False)
```
