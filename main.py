import discord
from discord.ext import commands
from discord.ui import Button, TextInput
from discord import app_commands,Interaction,ui,ButtonStyle,SelectOption, SyncWebhook
import json
import os
from enum import Enum
import sys
import numpy
import pandas as pd
import csv
from os import walk
from modules import CONFIG, addjson
from modules.modalclass import TCInputModal, loadsave, makeinfo

def serverpath(id: str):
      return os.path.abspath(os.path.join(os.path.join(os.path.join(os.path.curdir, "bc_saves"), "servers"), id))

def srvmemberpath(srvid: str, memid: str):
      return os.path.abspath(os.path.join(os.path.join(os.path.join(os.path.join(os.path.curdir, "bc_saves"), "servers"), srvid), memid))

def loadsrvset_all():
  with open(os.path.join(os.path.join(os.path.curdir, "modules"), "serversettings.json"), "r", encoding="utf-8") as setreader:
    setreader_str = setreader.read()
  setobj = json.loads(setreader_str)
  return setobj
  
def savesrvset_all(data):
  open(os.path.join(os.path.join(os.path.curdir, "modules"), "serversettings.json"), "w+", encoding="utf-8").write(json.dumps(data))

def loadsrvset(srvid: str):
  with open(os.path.join(os.path.join(os.path.curdir, "modules"), "serversettings.json"), "r", encoding="utf-8") as setreader:
    setreader_str = setreader.read()
  setobj = json.loads(setreader_str)
  return setobj[srvid]
  
def savesrvset(srvid: str, newset):
  with open(os.path.join(os.path.join(os.path.curdir, "modules"), "serversettings.json"), "r", encoding="utf-8") as setreader:
    setreader_str = setreader.read()
  setobj = json.loads(setreader_str)
  setobj[srvid] = newset
  open(os.path.join(os.path.join(os.path.curdir, "modules"), "serversettings.json"), "w+", encoding="utf-8").write(json.dumps(setobj))

class MyClient(discord.Client):
  async def on_ready(self):
    await self.wait_until_ready()
    await tree.sync()
    if not os.path.exists(os.path.abspath(os.path.join(os.path.curdir, "bc_saves"))):
      os.mkdir(os.path.abspath(os.path.join(os.path.curdir, "bc_saves")))
      os.mkdir(os.path.abspath(os.path.join(os.path.join(os.path.curdir, "bc_saves"), "servers")))
    print(f"{self.user} logged in!")
intents= discord.Intents.all()
client = MyClient(intents=intents)
tree = app_commands.CommandTree(client)

@tree.command(name="sendp", description="send button")
@app_commands.checks.has_permissions(administrator=True)
async def sendbtn(interaction:Interaction):
  button = ui.Button(style=ButtonStyle.green,label="Start",disabled=False)
  view = ui.View(timeout=None)
  view.add_item(button)
  embed = discord.Embed(title="BC Save Backup/Restore", description="Click button")
  async def loadfile_cb(interaction:Interaction):
    select = ui.Select(placeholder="Select save file")
    userid = str(interaction.user.id)
    serverid = str(interaction.guild_id)
    mypath = srvmemberpath(serverid, userid)
    i = -1
    num = 0
    filelist = ""
    text = ""
    filenames=os.listdir(mypath)
    filenamesnum=len(filenames)
    print(filenamesnum)
    while i <= filenamesnum:
      i += 1
      if i == filenamesnum or filenames[i] == None:
        print("i is None")
        text1 = "No Save Files.\nPlease use backup first."
        k = False
        break
      else:
        if not filenames[i] == "userdata.csv":
          k = True
          text1 = str(i+1) + ". " + filenames[i] + "\n"
          select.add_option(label=text1, value=str(i+1), description="Save file")
    view = ui.View()
    view.add_item(select)
    if k:
      await interaction.response.send_message(ephemeral=True, view=view, delete_after=120.0, content="Select file in 2 minutes")
    else:
      await interaction.response.send_message(ephemeral=True, content=text1, delete_after=30.0)
    async def loadfile_select_cb(interaction:Interaction):
      filenum = int(select.values[0])
      selectedfile = filenames[filenum-1]
      savefilepath = os.path.join(mypath, selectedfile)
      await loadsave(interaction, savefilepath)
    select.callback=loadfile_select_cb

  async def button_callback(interaction:Interaction):
    set = loadsrvset(str(interaction.guild_id))
    if 1 == 2: #i dont have tab btn now (ipad) so
	pass
    else:
      usr = int(interaction.user.id)
      userpath = os.path.join(srvmemberpath(str(interaction.guild_id), str(usr)), "userdata.csv")
      if not os.path.exists(userpath):
            embed = discord.Embed(title="", description="Not enrolled to serverdb\n`/userenroll` to enroll")
            await interaction.response.send_message(embed=embed, ephemeral=True)
      else:
            usr = int(interaction.user.id)
            userpath = os.path.join(srvmemberpath(str(interaction.guild_id), str(usr)), "userdata.csv")
            typeselect = ui.Select(placeholder="Select Menu")
            typeselect.add_option(label="Backup", value="tc", description="Backup with Transfer Code")
            typeselect.add_option(label="Restore", value="lf", description="Restore with backup")
            view_m = ui.View()
            view_m.add_item(typeselect)
            async def type_cb(interaction: Interaction):
              if typeselect.values[0] == "lf":
                await loadfile_cb(interaction)
              elif typeselect.values[0] == "tc":
                select = ui.Select(placeholder="Select Country Code")
                select.add_option(label="kr",value="kr",description="Korea")
                select.add_option(label="en",value="en",description="Global")
                select.add_option(label="jp",value="jp",description="Japan")
                select.add_option(label="tw",value="tw",description="Taiwan")
                view=ui.View()
                view.add_item(select)
                async def select_callback(interaction:Interaction):
                  country = select.values[0]
                  print(country)
                  await interaction.response.send_modal(TCInputModal(country))
                select.callback=select_callback
                await interaction.response.send_message(ephemeral=True,view=view,delete_after=30.0,content="Select Country code in 30 seconds")
            typeselect.callback=type_cb
            await interaction.response.send_message(view=view_m, delete_after=30.0, ephemeral=True, content="Select menu in 30 seconds")
  button.callback=button_callback
  await interaction.response.send_message(embed=embed, view=view)
  
@tree.command(name="userenroll", description="enroll user to serverdb")
async def RegisterMem(interaction: Interaction):
  srvid = str(interaction.guild_id)
  memid = str(interaction.user.id)
  if not os.path.exists(srvmemberpath(srvid, memid)):
    os.mkdir(srvmemberpath(srvid, memid))
    csvdata = makeinfo(memid)
    csvpath = os.path.join(srvmemberpath(srvid, memid), "userdata.csv")
    with open(csvpath, "w+", encoding="utf-8") as csvwriter:
      csvwriter.write(csvdata)
    embed = discord.Embed(title="Success", description="successfully enrolled")
  else:
    embed = discord.Embed(title="already enrolled to serverDB")
  await interaction.response.send_message(embed=embed)

@tree.command(name="srvenroll", description="enroll server")
@app_commands.checks.has_permissions(administrator=True)
async def RegisterSrv(interaction: Interaction):
  srvid = str(interaction.guild_id)
  if not os.path.exists(serverpath(srvid)):
    os.mkdir(serverpath(srvid))
    curset = loadsrvset_all()
    newdata = addjson.adddata(curset, srvid)
    savesrvset_all(newdata)
    embed = discord.Embed(title="success", description="enroll success")
  else:
    embed = discord.Embed(title="server is already enrolled")
  await interaction.response.send_message(embed=embed)

client.run(CONFIG.token)
