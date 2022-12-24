import io
from typing import List, Union

import pandas as pd

from hybrid_rs.server.orm.anime_orm import Anime


def process_recommendations(recommendations: str) -> List[int]:
    return recommendations.replace("[", '').replace(']', '').split(',')


def load_anime_csv_to_orm(path_or_buffer: Union[str, io.TextIOWrapper]) -> List[Anime]:
    df: pd.DataFrame = pd.read_csv(path_or_buffer)
    for _, row in df.iterrows():
        fields = dict()
        # mongoengine doesn't know np.nan
        for idx, col in row.items():
            fields[idx] = col if pd.notnull(col) else None

        # This field is string by default in csv
        if fields["recommendations"] is not None:
            fields["recommendations"] = process_recommendations(fields["recommendations"])

        anime: Anime = Anime(
            anime_id=fields['_id'],
            name=fields['Name'],
            num_episodes=fields['Episodes'],
            studio=fields["Studio"],
            rating=fields["Rating"],
            description=fields["Description"],
            related_manga=fields["Related_Mange"],
            recommendations=fields["recommendations"]
        )
        
        anime.save()


if __name__ == "__main__":
    Anime.drop_collection()
    with open(
        "notes/anime_with_recommendations.csv"
    ) as f:
        load_anime_csv_to_orm(f)
    
    animes: List[Anime] = Anime.objects()[:10]
    for anime in animes:
        print(anime.name)
