import discord
from discord.ext import commands
from discord.ui import View, button

#currently broken
class MyMenu(View):
    def __init__(self):
        super().__init__()

    @button(label="Left hand")
    async def button1(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.send_message("Button 1 clicked!")

    @button(label="Right hand")
    async def button2(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.send_message("Button 2 clicked!")


async def show_menu(ctx):
    menu = MyMenu()
    await ctx.channel.send("Decide your fate", view=menu)