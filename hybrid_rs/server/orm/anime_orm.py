from mongoengine import (
    Document, StringField, ListField, IntField,
    FloatField, ReferenceField, connect)

from hybrid_rs.server.config import config


connect(
    db=config["MongoDB"]['db'],
    host=config['MongoDB']['address'],
    port=config['MongoDB']['port']
)

class Anime(Document):
    anime_id = IntField(required=True, db_field="_id", primary_key=True)
    name = StringField(required=True, db_field='Name')
    num_episodes = IntField(db_field='Episodes', null=True)
    studio = StringField(db_field='Studio', null=True)
    rating = FloatField(db_field='Rating', null=True)
    description = StringField(db_field='Description', null=True)
    related_manga = StringField(db_field='Related_Mange', null=True)
    recommendations = ListField(ReferenceField('self'), db_field='recommendations', null=True)

    meta = {
        'collection': 'anime'
    }


if __name__ == "__main__":
    # ids = [5, 10, 3]
    # animes: List[Anime] = Anime.objects(anime_id__in=ids)
    anime: Anime = Anime.objects().first()

    print(anime.name)
    print(anime.recommendations[0].name)

    # for anime in animes[:10]:
    #     print(anime.name)
