################################################################
# Header

__package_name__ = "UniConfig"
__version__ = "v1.0"
__license__ = "Unlicense"

__author__ = "mkow04"
__email__ = "maciejkowalski04@proton.me"

__all__ = ["Config"]


################################################################
# Imports

import toml
from pathlib import Path


################################################################
# Exceptions

class BaseUniConfigException(Exception):
    """Base exception inherited by all other UniConfig exceptions"""
    pass


class ConfigNotEditedException(BaseUniConfigException):
    """Exception which is thrown when config is the same as the default one and is_comparing_with_default == True"""
    pass


class ConfigFreshlyCreatedException(ConfigNotEditedException):
    """Exception inheriting from ConfigNotEditedException, thrown when config was freshly created from default_config while is_comparing_with_default == True"""
    pass


class ConfigKeysDontMatchException(BaseUniConfigException):
    """Exception thrown when dictionary keys of the config don't match the keys of the default config"""
    pass


################################################################
# Config class

class Config:
    def __init__(self, config_file_path: str,
                 default_config: dict = None,
                 is_creating_new_config: bool = True,
                 is_comparing_with_default: bool = True,
                 is_checking_keys_on_load: bool = True):

        self.is_creating_new_config = is_creating_new_config
        self.is_comparing_with_default = is_comparing_with_default
        self.is_checking_keys_on_load = is_checking_keys_on_load

        if default_config is not None:
            self.default_config = default_config
        else:
            self.default_config = {}

        self.config_file_path = Path(config_file_path).expanduser()

        self.load()

    def check_keys(self):
        if self.config.keys() == self.default_config.keys():
            return True
        else:
            return False

    def create_default(self):
        self.config_file_path.parent.mkdir(parents=True, exist_ok=True)

        with self.config_file_path.open("w", errors="ignore") as config_file:
            toml.dump(self.default_config, config_file)

    def load(self):
        was_default_created = False

        try:
            with self.config_file_path.open("r", errors="ignore") as config_file:
                self.config = toml.load(config_file)
        except FileNotFoundError as e:
            if self.is_creating_new_config:
                self.create_default()
                self.config = self.default_config.copy()
                was_default_created = True
            else:
                raise e

        if self.is_comparing_with_default and self.config == self.default_config:
            if was_default_created:
                raise ConfigFreshlyCreatedException
            else:
                raise ConfigNotEditedException

        if self.is_checking_keys_on_load:
            if not self.check_keys():
                raise ConfigKeysDontMatchException


################################################################
# Interactive run

def main():
    print()
    print("-"*48)
    print(f" {__package_name__.capitalize()} '{__version__}'")
    print(f" Author: '{__author__} <{__email__}>'")
    print("-"*48)
    print()


if __name__ == "__main__":
    main()
