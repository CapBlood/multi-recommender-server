from typing import List, Tuple

from django.http import HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import redirect, render, HttpResponseRedirect

from hybrid_rs.server.orm.anime_orm import Anime
from hybrid_rs.server.config import config


def index(request) -> HttpResponseRedirect:
    return redirect("/anime")


def anime_search(request) -> HttpResponse:
    animes: List[Anime] = []
    search_param = request.GET.get('search', None)
    if search_param is not None:
        animes: List[Anime] = Anime.objects(name__istartswith=search_param)
        animes = Paginator(
            animes, config['Server']['pagination'])
        
        page_number = request.GET.get('page')
        animes = animes.get_page(page_number)

    return render(
        request, 'anime.html', {
            'items': animes,
            'request': request
        }
    )

def anime_description(request, anime_id: int) -> HttpResponse:
    anime: Anime = Anime.objects(anime_id=anime_id).first()
    if anime is None:
        pass

    name: str = anime.name
    desc: str = anime.description
    recommendations: List[Anime] = anime.recommendations
    recommendations_with_names: List[Tuple[int, str]] = list(map(
        lambda x: (x.anime_id, x.name), recommendations))

    return render(
        request,
        'description.html', {
            'name': name,
            'content': desc,
            'recommendations': recommendations_with_names
        }
    )
