import configparser


class Config:
    _config = None

    @classmethod
    def config(cls):
        return cls._config

    @classmethod
    def load_config(cls, path):
        config = configparser.ConfigParser()
        config.read(path)
        cls._config = config
