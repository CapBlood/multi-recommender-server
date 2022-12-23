import os
from typing import Union

import toml


class Config:
    __config: dict = None
    
    NAME_CONFIG: str = "config.toml"

    def __init__(self) -> None:
        if self.__config is not None:
            return

        path_config = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), self.NAME_CONFIG)
        self.__config = toml.load(path_config)
        
    def __getitem__(self, key: str) -> Union[str, list, int, float]:
        return self.__config.__getitem__(key)


class EnvConfig(Config):
    def __init__(self) -> None:
        super().__init__()
        
    def __getitem__(self, key: str) -> Union[str, list, int, float]:
        if key not in os.environ:
            return super().__getitem__(key)

        return self.cast(os.environ[key])

    @staticmethod
    def cast(value: str) -> Union[int, bool, str]:
        if value == 'true':
            return True
        elif value == 'false':
            return False
        elif value.isdigit():
            return int(value)
        else:
            return value


config = EnvConfig()


if __name__ == "__main__":    
    print(config["DB_ADDRESS"])
    print(type(config["DB_ADDRESS"]))
