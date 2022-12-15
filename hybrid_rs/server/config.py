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

    def __setitem__(self, key: str, value: Union[str, list, int, float]) -> None:
        return self.__config.__setitem__(key, value)


config = Config()


if __name__ == "__main__":    
    print(config["MongoDB"]["port"])
