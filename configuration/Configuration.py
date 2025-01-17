from datetime import datetime
from pathlib import Path

import yaml
from loguru import logger
from munch import Munch
# from tqdm import tqdm

class Configuration():
    """
    A class used to load and manage configuration settings from a YAML file.
    Meant to be called after configuring Logger.
    Class Attributes:
    -----------------
    _cfg : Munch
        A Munch object containing the configuration settings.
    Methods:
    --------
    load(config_file):
        Loads the configuration settings from the specified YAML file.
    get_config():
        Returns the loaded configuration settings.
    """
    
    _cfg = None 
    
    @classmethod
    def load(cls, config_file):
        config_file = Path(config_file)
        
        if not config_file.exists():
            raise FileExistsError(f"{config_file} doesn't exists. Please pass a valid file path.")
        
        if config_file.suffix != '.yaml':
            raise ValueError(f"Invalid file type: {config_file}. Expected a .yaml file.")
        
        try:
            with open(config_file) as f:
                cfg_yaml = yaml.load(f, yaml.FullLoader)
        
        except Exception as e:
            raise ValueError(f'Error loading configuration file {config_file}')
        
        # store config as a Munch
        cls._cfg = Munch.fromDict(cfg_yaml)
        cls._cfg.now = datetime.now()
        logger.info(f'Loaded configuration from {config_file}. \nConfiguration.now timestamped at {cls._cfg.now.strftime('%Y-%m-%d_%H:%M:%S')}.')
        # print(f'Loaded configuration from {config_file}. \nConfiguration.now timestamped at {cls._cfg.now.strftime('%Y-%m-%d_%H:%M:%S')}.')
        
    @classmethod
    def get_config(cls, config_path=None):
        if cls._cfg is None and config_path is not None:
            cls.load(config_path)

        return cls._cfg

    @classmethod
    def print_config(cls):
        logger.info(f'{yaml.dump(cls._cfg)}')
        # print(f'{yaml.dump(cls._cfg)}')

    @classmethod
    def validate_config(cls):
        if cls._cfg is None:
            raise ValueError("Configuration has not been loaded yet.")
    
    @classmethod
    def __call__(cls):
        return cls._cfg
    
    @classmethod
    def __getattr__(cls, name):
        cls.validate_config()
        return getattr(cls._cfg, name)
    
class Logger():
    """
    Logger class for configuring and managing log files and logging output.
    The default useage is to configure Logger in your main function then use 
    Logger.<method> everywhere else.
    
    Attributes:
        log_dir (Path): Directory where log files will be stored.
    Methods:
        configure(test_name):
            Configures the logger to write logs to a file specific to the given test name.
        configure_tqdm():
            Configures the logger to integrate with tqdm for progress bar logging.
        get_logger():
            Returns the logger instance.
    """
    
    _logger_instance = None
    
    @property
    def save_dir(cls):
        return cls.log_dir
    
    @classmethod
    def configure(cls, cfg):
        logger.remove()
        
        log_dir = Path.cwd().joinpath(cfg.logger.path) # logs/
        log_dir.mkdir(parents=True, exist_ok=True)
        
        log_group = log_dir.joinpath(cfg.settings.group, cfg.now.strftime('%Y-%m-%d'))
        log_group.mkdir(parents=True, exist_ok=True) #logs/group/day
        
        log_testdir = log_group.joinpath(cfg.settings.name)
        cfg.logger.log_testpath = log_testdir
        
        if cfg.settings.group == 'dev':
            log_file = log_testdir.joinpath(f"{cfg.settings.name}.log")
        else:
            log_file = log_testdir.joinpath(f"{cfg.settings.name}_{cfg.now.strftime('%Y-%m-%d_%H:%M:%S')}.log")
        
        cls._logger_instance = logger
        cls._logger_instance.add(log_file, format="{time} {level} {message}",rotation="50 MB", )
        cls._logger_instance.info(f'Added log handler for {log_file}')
        cls._logger_instance.info(f'Logging started at {cfg.now.strftime('%Y-%m-%d @ %H:%M:%S')}')
        
    # @classmethod
    # def configure_tqdm(cls):
    #     cls._logger_instance.add(lambda msg: tqdm.write(msg, end=""), colorize=True)
    #     cls._logger_instance.info("Initializing logger with tqdm...")

    @classmethod
    def get_logger(cls):
        if cls._logger_instance is None:
            raise ValueError("Logger is not configured. Call `Logger.configure` first.")
        return cls._logger_instance
    
    @classmethod
    def __getattr__(cls, name):
        """Delegate calls to the underlying logger instance."""
        if cls._logger_instance is None:
            raise ValueError("Logger is not configured. Call `Logger.configure` first.")
        return getattr(cls._logger_instance, name)
    
    @classmethod
    def __call__(cls):
        return cls.get_logger()