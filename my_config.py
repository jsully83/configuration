from datetime import datetime
from pathlib import Path

from simple_config import Logger, Configuration
# from configuration import Logger

conf_path = Path.cwd().joinpath('conf/config.yaml')

Configuration.get_config(conf_path)
Configuration.print_config()

cfg = Configuration()

Logger.configure(cfg)
logger = Logger.get_logger()


cfg.now = datetime.now()

logger.info(f"The time is now {cfg.now.strftime('%Y-%m-%d @ %H:%M:%S')}")