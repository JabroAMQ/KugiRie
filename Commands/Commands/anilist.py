import discord
from discord import app_commands

from Commands.base import Commands
from Code.Anilist.controller import Controller

class Anilist_Commands(Commands):

    def __init__(self) -> None:
        super().__init__()

    def load_commands(self, client: discord.Client) -> None:
        @client.tree.command(name='anime', description='Muestra información sobre un anime determinado')
        @app_commands.describe(anime='Título o ID del anime a buscar')
        @app_commands.guild_only
        async def anime(interaction: discord.Interaction, anime: str):
            await Controller().anime(interaction, anime)

        @client.tree.command(name='random_planned', description='Rollea un anime aleatorio de tu PTW')
        @app_commands.guild_only
        async def random_planned(interaction: discord.Interaction):
            await Controller().random_planned(interaction)

        @client.tree.command(name='compare_ptw', description='Compara dos listas de PTW de Anilist y muestra las coincidencias')
        @app_commands.describe(user_1='Usuario 1 a comparar (mención)', user_2='Usuario 2 a comparar (mención)')
        @app_commands.guild_only
        async def compare_ptw(interaction: discord.Interaction, user_1: discord.Member, user_2: discord.Member):
            await Controller().compare_ptw(interaction, user_1.id, user_2.id)