from pywebio.output import put_markdown, put_link, put_text


def put_similar_animes(animes):
    put_markdown("## Рекомендуемые аниме")
    for id_anime, anime in zip(animes[0], animes[1]):
        put_link(anime, f"/anime/{id_anime}")
        put_text()


def put_anime(anime_info):
    put_link("<< На главную страницу", "/")
    put_markdown(f"# {anime_info['name']}")
    put_markdown(f"{anime_info['desc']}")
