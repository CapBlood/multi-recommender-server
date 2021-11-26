import random

from loguru import logger
from pywebio.output import *
from pywebio.pin import *
from pywebio.session import info as session_info

from hybrid_rs.utils import get_id_from_path
from hybrid_rs.outputs import put_similar_animes, put_anime
from hybrid_rs.error_views import redirect_anime_error
from hybrid_rs.exceptions import NotInitializedData, NotFoundItem


class Data:
    DATASET = "dataset"
    MODEL = "model"

    data = dict()

    @classmethod
    def add_data(cls, namespace, name_obj, obj):
        if namespace not in cls.data:
            cls.data[namespace] = dict()
        cls.data[namespace][name_obj] = obj

    @classmethod
    def get_data(cls, namespace, name_obj):
        if namespace not in cls.data and name_obj not in cls.data[namespace]:
            raise NotInitializedData()
        return cls.data[namespace][name_obj]


class AnimeHandler:
    # TODO: Убрать put_link и многостраничность и переходить между страницами через вызовы функций
    #  (вызывать clean, а затем саму функцию).

    NAMESPACE = "anime"

    @staticmethod
    async def action_button_search(scroll_area, dataset):
        name = await pin.search_line

        if len(name) < 3:
            popup("Недопустимо название с 2 символами и меньше")
            return

        AnimeHandler.update_scroll_area(scroll_area, dataset.get_id_with_names(name))

    @staticmethod
    def update_scroll_area(scroll_area, item_list):
        scroll_area.reset()
        for link in item_list:
            label = item_list[link]
            scroll_area.append(put_link(f"{label}\n", f"{AnimeHandler.NAMESPACE}/{link}"))
            scroll_area.append(put_text())

    @staticmethod
    async def random_anime():
        dataset = Data.get_data(AnimeHandler.NAMESPACE, Data.DATASET)
        anime_id = random.choice(dataset.dataset.index)
        clear()
        await AnimeHandler.get_anime(anime_id)

    @staticmethod
    async def main():
        dataset = Data.get_data(AnimeHandler.NAMESPACE, Data.DATASET)
        scroll_area = output()

        put_markdown("# AnimeRecommender")
        put_input("search_line", label="Поиск", datalist=dataset.get_names())

        put_row([
            put_button(
                'Искать',
                onclick=lambda: AnimeHandler.action_button_search(scroll_area, dataset)),
            put_button(
                'Мне повезет',
                onclick=lambda: AnimeHandler.random_anime())
        ], size="10% 20%")

        put_text()
        put_scrollable(scroll_area, height=800, keep_bottom=True)

    @staticmethod
    # @redirect_anime_error
    async def anime():
        path = session_info['request'].path
        anime_id = get_id_from_path(path)

        await AnimeHandler.get_anime(anime_id)


    @staticmethod
    async def get_anime(anime_id):
        dataset = Data.get_data(AnimeHandler.NAMESPACE, Data.DATASET)
        model = Data.get_data(AnimeHandler.NAMESPACE, Data.MODEL)

        try:
            anime_info = dataset.get_item_info_by_id(anime_id)
        except NotFoundItem:
            # TODO: Не возвращает 404.
            logger.error(f"Аниме с идентификатором {anime_id} нет в базе данных.")
            return

        pred_animes = model.predict(anime_id)
        animes = pred_animes, dataset.dataset.loc[pred_animes]["Name"].values.tolist()

        put_anime(anime_info)
        put_similar_animes(animes)
