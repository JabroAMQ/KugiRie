import discord

from Code.Anilist.query import Query
from Code.Anilist.Users.catalog import Users
from Code.Anilist.Animes.catalog import Animes
from Code.Anilist.Functions.random_planned import generate_embed

def _search_anime_by_name(anime_name) -> dict:
    QUERY_GET_ANIME_DETAILS = """
        query ($media_name: String) {
            Media(search: $media_name, type: ANIME) {
                id
                title {
                    romaji
                }
                type
                format
                status
                description
                status
                season
                seasonYear
                episodes
                duration
                coverImage {
                    extraLarge
                }
                genres
                meanScore
                popularity
                favourites
                siteUrl
            }
        }
    """

    query = Query()
    anime_details = query.execute(QUERY_GET_ANIME_DETAILS, variables={'media_name': anime_name})
    return anime_details['Media']

def _search_anime_by_id(anime_id) -> dict:
    QUERY_GET_ANIME_DETAILS = """
        query ($media_id: Int) {
            Media(id: $media_id, type: ANIME) {
                id
                title {
                    romaji
                }
                type
                format
                status
                description
                status
                season
                seasonYear
                episodes
                duration
                coverImage {
                    extraLarge
                }
                genres
                meanScore
                popularity
                favourites
                siteUrl
            }
        }
    """
    query = Query()
    anime_details = query.execute(QUERY_GET_ANIME_DETAILS, variables={'media_id': anime_id})
    return anime_details['Media']


def _represent_default():
    return f"**Not On List:** {(' | ').join(Users().get_all_users_names())}"


def anime(anime_info: str) -> discord.Embed:
    # Get anime data from Anilist
    anime_data = _search_anime_by_name(anime_info) if not anime_info.isdigit() else _search_anime_by_id(int(anime_info))

    # Get anime data from Catalog
    anime = Animes().get_anime(anime_data['id'])
    user_data = anime.represent_users_data() if anime is not None else _represent_default()

    return generate_embed(anime_data, user_data, discord.Colour.pink())