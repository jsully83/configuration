from pathlib import Path

from configuration.Configuration import Configuration

conf_path = Path.cwd().joinpath('conf/config.yaml')

Configuration.get_config(conf_path)
Configuration.print_config()

cfg = Configuration()

print(cfg.now)