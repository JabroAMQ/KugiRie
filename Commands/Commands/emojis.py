import discord

from Commands.base import Commands
from Code.Emojis.controller import Emojis_Controller

class Emojis_Commands(Commands):

    def __init__(self) -> None:
        super().__init__()

    def load_commands(self, client: discord.Client) -> None:
        @client.tree.command(name='emojis', description='Lista todos los emojis KugiRie disponibles')
        async def emojis(interaction: discord.Interaction):
            await Emojis_Controller().print_all_emojis(interaction)