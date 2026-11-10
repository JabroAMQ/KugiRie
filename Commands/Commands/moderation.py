import discord
from discord import app_commands

from Commands.base import Commands
import Code.Others.moderation as interactions

class Moderation_Commands(Commands):

    def __init__(self) -> None:
        super().__init__()

    def load_commands(self, client: discord.Client) -> None:
        @client.tree.command(name='reset_data', description='Actualiza la información almacenada en memoria')
        @app_commands.describe(force_anilist='Si se deben solicitar de nuevo las listas de anilist de los usuarios')
        @app_commands.guild_only
        @app_commands.check(self.is_user_owner)
        async def reset_data(interaction: discord.Interaction, force_anilist: bool = False):
            await interactions.reset_data(interaction, client, force_anilist)