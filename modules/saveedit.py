import discord
from discord.ext import commands
from discord.ui import Button, TextInput
from discord import app_commands,Interaction,ui,ButtonStyle,SelectOption
import json
import datetime
import os
import sys
import BCSFE_Python_Discord as BCSFE_Python
from BCSFE_Python_Discord import *

def uploadsave(save_stats, path):
    edits.save_management.save.save_save1(save_stats, path)
    save_data = BCSFE_Python.serialise_save.start_serialize(save_stats)
    save_data = BCSFE_Python.helper.write_save_data(
        save_data, save_stats["version"], path, False
    )
    upload_data = BCSFE_Python.server_handler.upload_handler(save_stats, path)
    transfer_code = upload_data['transferCode']
    confirmation_code = upload_data['pin']
    return transfer_code, confirmation_code

async def main_cb(interaction: Interaction, save_stats, path):
	tccode, cccode = uploadsave(save_stats, path)
	await interaction.user.send(content=f"Success.\nEnter this codes in game.\n{tccode}\n{cccode}")

