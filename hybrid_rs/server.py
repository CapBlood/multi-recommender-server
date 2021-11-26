import pathlib
import atexit
import os

import tornado.ioloop
import tornado.web
from loguru import logger
from pywebio.platform import config
from pywebio.platform.tornado import webio_handler

from hybrid_rs.views import AnimeHandler, Data
from hybrid_rs.dataset import Dataset
from hybrid_rs.model import DictModel, ItemModel, GeneralModel
from hybrid_rs.config import Config
from hybrid_rs.data import download
from hybrid_rs.utils import get_resource


def atexit_server():
    logger.info("Сервер завершил работу.")


def load_dataset():
    path_to_dataset = Config.config().get("Anime", "content_dataset")
    path_to_dataset = get_resource(path_to_dataset)
    dataset = Dataset(path_to_dataset, "Name", "synopsis")
    Data.add_data(AnimeHandler.NAMESPACE, Data.DATASET, dataset)


def load_config():
    path_to_config = get_resource("config.ini")
    Config.load_config(path_to_config)


def init_pywebio():
    css_path = Config.config().get("Server", "css_path")
    css_path = get_resource(css_path)
    with open(css_path, 'r') as file:
        css = file.read()
    config(title="AnimeRecommender", css_style=css)


def load_models():
    path = Config.config().get("Anime", "content_model")
    path = get_resource(path)
    content_model = DictModel.from_dict(path)

    path_to_ratings = Config.config().get("Anime", "rating_npz")
    path_to_ratings = get_resource(path_to_ratings)
    if not pathlib.Path(path_to_ratings).exists():
        file_id = Config.config().get("Anime", "google_rating_npz")
        download(file_id, path_to_ratings)

    item_model = ItemModel.from_npz(path_to_ratings)

    # path_to_item = Config.config().get("Anime", "item_model")
    # path_to_item = get_resource(path_to_item)
    # item_model = DictModel.from_dict(path_to_item)

    common_model = GeneralModel(content_model, item_model)
    Data.add_data(AnimeHandler.NAMESPACE, Data.MODEL, common_model)


if __name__ == "__main__":
    logger.info("Загрузка конфигурации...")
    load_config()
    init_pywebio()
    logger.info("Конфигурация загружена.")

    logger.info("Загрузка датасетов...")
    load_dataset()
    logger.info("Датасеты загружены.")

    logger.info("Загрузка моделей...")
    load_models()
    logger.info("Модели загружены.")

    atexit.register(atexit_server)

    try:
        application = tornado.web.Application([
            (r"/", webio_handler(AnimeHandler.main)),
            (f"/{AnimeHandler.NAMESPACE}/" + r"([0-9]+)", webio_handler(AnimeHandler.anime))
        ])

        if "PORT" in os.environ:
            port = os.environ["PORT"]
        else:
            port = Config.config().getint('Server', 'port')
        address = Config.config().get('Server', 'address')
        application.listen(port=port, address=address)
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        pass
