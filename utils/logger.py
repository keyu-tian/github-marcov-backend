import sys
import logging


def create_logger(logger_name, log_path, level=logging.WARN, to_stdout=True):
    l = logging.getLogger(logger_name)
    formatter = logging.Formatter(
        fmt='[%(asctime)s][%(filename)10s][line:%(lineno)4d][%(levelname)4s] %(message)s',
        datefmt='%m-%d %H:%M:%S'
    )
    fh = logging.FileHandler(log_path)
    fh.setFormatter(formatter)
    l.setLevel(level)
    l.addHandler(fh)
    if to_stdout:
        sh = logging.StreamHandler(stream=sys.stdout)
        sh.setFormatter(formatter)
        l.addHandler(sh)
    return l
