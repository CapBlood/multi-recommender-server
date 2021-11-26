from pywebio.output import put_markdown

from hybrid_rs.exceptions import NotFoundItem


async def anime_not_found_error():
    put_markdown("# Ошибка 404 😈")
    put_markdown("Такого аниме нет в базе.")


def redirect_anime_error(handler):
    async def func():
        try:
            await handler()
        except NotFoundItem:
            await anime_not_found_error()
    return func
