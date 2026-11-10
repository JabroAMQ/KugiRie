import os
import secrets

import discord

from Code.Anilist.query import Query
from Code.Anilist.Users.catalog import Users
from Code.Anilist.Animes.catalog import Animes
from Code.Anilist.Functions.anime import anime
from Code.Anilist.Functions.random_planned import random_planned
from Code.Anilist.Functions.compare_ptw import compare_ptw
from Code.Utilities.error_handler import error_handler_decorator

class Controller:

    _instance = None
    def __new__(cls) -> 'Controller':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._set_data()
        return cls._instance

    def _set_data(self) -> None:
        # Retrieve all lists from Anilist
        QUERY_GET_USER_ANIME_LIST = """
            query ($user_id: Int) {
                MediaListCollection(userId: $user_id, type: ANIME) {
                    lists {
                        entries {
                            mediaId
                            score
                            status
                            progress
                            media {
                                title {
                                    romaji
                                }
                                status
                            }
                        }
                    }
                }
            }
            """

        query = Query()
        for user in Users().get_users_data():
            # Obtain the user's anime list from Anilist
            user_list_raw = query.execute(QUERY_GET_USER_ANIME_LIST, variables={'user_id': user.anilist_id})

            # Extract the entries from the response and store them into the catalog
            animes = Animes()
            user_list_entries = user_list_raw['MediaListCollection']['lists']
            for list_data in user_list_entries:
                for media_data in list_data['entries']:
                    media_data['discordId'] = user.discord_id
                    media_data['userStatus'] = media_data['status']
                    media_data['title'] = media_data['media']['title']['romaji']
                    media_data['mediaStatus'] = media_data['media']['status']
                    del media_data['status']
                    del media_data['media']
                    animes.add(media_data)

    @error_handler_decorator()
    async def anime(self, interaction: discord.Interaction, anime_info: str):
        try:
            await interaction.response.defer(thinking=True)
            embed = anime(anime_info)
            await interaction.followup.send(embed=embed)
    
        except Exception as e:
            await interaction.followup.send(e)

    @error_handler_decorator()
    async def random_planned(self, interaction: discord.Interaction):
        try:
            await interaction.response.defer(thinking=True)
            content, embed = random_planned(interaction.user.id)
            await interaction.followup.send(content=content, embed=embed)
    
        except Exception as e:
            await interaction.followup.send(e)

    @error_handler_decorator()
    async def compare_ptw(self, interaction: discord.Interaction, discord_id_1: int, discord_id_2: int):
        random_string = secrets.token_hex(nbytes=8)
        file_name = f'{random_string}.txt'

        try:
            await interaction.response.defer(thinking=True)
            response, shared_animes = compare_ptw(discord_id_1, discord_id_2)
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write(shared_animes)

            await interaction.followup.send(response, file=discord.File(file_name))
    
        except Exception as e:
            await interaction.followup.send(e)

        finally:
            if os.path.exists(file_name):
                os.remove(file_name)