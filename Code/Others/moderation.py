import discord

from Code.Anilist.Users.catalog import Users
from Code.Anilist.controller import Controller
from Code.Emojis.controller import Emojis_Controller
from Code.Others.easter_eggs import Easter_Eggs
from Code.Utilities.error_handler import error_handler_decorator

@error_handler_decorator()
async def reset_data(interaction: discord.Interaction, client: discord.Client, force_anilist: bool = False):
    await interaction.response.defer(ephemeral=True)
    
    Users()._set_data()
    Emojis_Controller()._set_data(client)
    Easter_Eggs()._set_data()

    if force_anilist:
        Controller()._set_data()

    await interaction.followup.send(content='Información actualizada con éxito!', ephemeral=True)