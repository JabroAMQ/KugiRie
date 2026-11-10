import random

import discord
import html2text

from Code.Anilist.query import Query
from Code.Anilist.Animes.catalog import Animes

def _get_random_anime(discord_id: int):
    planned_list = Animes().get_planned_list(discord_id)
    if not planned_list:
        raise ValueError('No planned animes found for the user.')
    
    return random.choice(planned_list)


def get_anime_details(media_id: int) -> dict:

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
    anime_details = query.execute(QUERY_GET_ANIME_DETAILS, variables={'media_id': media_id})
    return anime_details['Media']


def _generate_message_content() -> str:
    
    possible_contents = [
        'I wholeheartedly recommend that you watch this one. It\'s one of my clone\'s favourites.',
        'You totally should watch this. I heard that it\'s one of the best out there.',
        'I cannot believe that you never got to watch this...',
        'Why has nobody told you to watch this? It has such a reputation for a reason!',
        'The favourite count on this one is wrong. It\'s going to have +1 after you finish watching it.',
        'Go watch this right now. It\'s a classic for a reason.',
        'What have you been wasting your time on instead of this? Disgraceful.',
        'If you watch this, I will fullfil one of your deepest desires. 😘',
        'You better watch this one, or I\'m sending one of my clones after you.',
        'This is the next best thing after sliced bread and Shidou.'
    ]
    return random.choice(possible_contents)


def generate_embed(anime_details: dict, users_details: str, color: discord.Colour) -> discord.Embed:
    description = anime_details.get('description')
    if description is None:
        description = 'No description available.'
    else:
        # Clean the description from HTML tags and format it
        h = html2text.HTML2Text()
        h.ignore_links = False
        h.ignore_images = True
        h.body_width = 0  # No line wrapping
        description = h.handle(description).strip()
        
    embed = discord.Embed(
        title=anime_details['title']['romaji'],
        url=anime_details['siteUrl'],
        description=description,
        color=color
    )
    embed.set_thumbnail(url=anime_details['coverImage']['extraLarge'])

    # Formatting for display
    _type = anime_details['type'].capitalize()

    status = anime_details['status'].capitalize()

    season = anime_details['season']
    if season is None:
        season = '?'
    else:
        season = f"{anime_details['season'].capitalize()} {anime_details['seasonYear']}"

    score = anime_details['meanScore']
    score = f"{score}/100" if score is not None else '-'

    popularity = anime_details['popularity']

    favourites = f"{anime_details['favourites']} times"

    episodes = anime_details['episodes']
    episodes = episodes if episodes is not None else '?'

    duration = anime_details['duration']
    if duration is None:
        duration = '?'
    else:
        if isinstance(episodes, int) and episodes == 1:
            duration = f'{duration} minutes'
        else:
            duration = f'{duration} minutes per episode'

    format = anime_details['format']
    match format:
        case 'TV':
            format = 'TV'
        case 'TV_SHORT':
            format = 'TV Short'
        case 'MOVIE':
            format = 'Movie'
        case 'SPECIAL':
            format = 'Special'
        case 'OVA':
            format = 'OVA'
        case 'ONA':
            format = 'ONA'
        case 'MUSIC':
            format = 'Music'
        case _:
            format = format
        

    genres: list[str] = anime_details.get('genres', [])
    genres = [f'`{genre}`' for genre in genres]

    # Adding fields to the embed
    embed.add_field(name='Type', value=_type, inline=True)
    embed.add_field(name='Status', value=status, inline=True)
    embed.add_field(name='Season', value=season, inline=True)

    embed.add_field(name='Anilist Score', value=score, inline=True)
    embed.add_field(name='Popularity', value=popularity, inline=True)
    embed.add_field(name='Favourites', value=favourites, inline=True)
    
    embed.add_field(name='Episodes', value=episodes, inline=True)
    embed.add_field(name='Duration', value=duration, inline=True)
    embed.add_field(name='Format', value=format, inline=True)

    embed.add_field(name='Genres', value=' - '.join(genres), inline=False)

    embed.add_field(name='Users Scores', value=users_details, inline=False)

    return embed


def random_planned(discord_id: int) -> tuple[str, discord.Embed]:
    # Get a random anime from the user's planned list
    anime = _get_random_anime(discord_id)
    
    # Retrieve the anime's details from the Anilist API
    anime_details = get_anime_details(anime.media_id)
    
    # Retrieve the users data for the anime
    users_details = anime.represent_users_data()
    
    # Generate the message content and the embed with the anime's details
    content = _generate_message_content()
    embed = generate_embed(anime_details, users_details, discord.Colour.dark_purple())

    return content, embed