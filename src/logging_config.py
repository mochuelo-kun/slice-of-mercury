import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

class ColorCodes:
    grey = "\x1b[38;21m"
    green = "\x1b[1;32m"
    yellow = "\x1b[33;21m"
    red = "\x1b[31;21m"
    bold_red = "\x1b[31;1m"
    blue = "\x1b[1;34m"
    light_blue = "\x1b[1;36m"
    purple = "\x1b[1;35m"
    reset = "\x1b[0m"


class ColorizedArgsFormatter(logging.Formatter):
    arg_colors = [ColorCodes.purple, ColorCodes.light_blue]
    level_fields = ["levelname", "levelno"]
    level_to_color = {
        logging.DEBUG: ColorCodes.blue,
        logging.INFO: ColorCodes.green,
        logging.WARNING: ColorCodes.yellow,
        logging.ERROR: ColorCodes.red,
        logging.CRITICAL: ColorCodes.bold_red,
    }

    def __init__(self, fmt: str, datefmt: Optional[str] = None):
        super().__init__()
        self.level_to_formatter = {}

        def add_color_format(level: int):
            color = ColorizedArgsFormatter.level_to_color[level]
            _format = fmt
            for fld in ColorizedArgsFormatter.level_fields:
                search = "(%\(" + fld + "\).*?s)"
                _format = re.sub(search, f"{color}\\1{ColorCodes.reset}", _format)
            formatter = logging.Formatter(_format, datefmt=datefmt)
            self.level_to_formatter[level] = formatter

        add_color_format(logging.DEBUG)
        add_color_format(logging.INFO)
        add_color_format(logging.WARNING)
        add_color_format(logging.ERROR)
        add_color_format(logging.CRITICAL)

    def format(self, record):
        orig_msg = record.msg
        orig_args = record.args
        formatter = self.level_to_formatter.get(record.levelno)
        formatted = formatter.format(record)
        record.msg = orig_msg
        record.args = orig_args
        return formatted

# separate log streams to console and file
run_timestamp = datetime.now()
minute_timestamp = run_timestamp.strftime("%Y%m%d_%H%M")

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

log_dir = Path(__file__).parent.resolve() / "../logs"
Path(log_dir).mkdir(parents=True, exist_ok=True)
log_filepath = log_dir / f"{minute_timestamp}.md"
file_handler = logging.FileHandler(log_filepath)
file_handler.setLevel(logging.INFO)

date_format = '%Y-%m-%d %H:%M:%S'
file_format = '\n---\n`--%(asctime)s %(levelname)s--`\n%(message)s\n'
console_format = "[%(asctime)s %(levelname)-8s] %(message)s"
file_formatter = logging.Formatter(file_format, datefmt=date_format)
console_handler.setFormatter(ColorizedArgsFormatter(console_format, datefmt=date_format))
file_handler.setFormatter(file_formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)
