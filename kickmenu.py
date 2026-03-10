import discord
from discord.ext import commands
from discord.ui import View, Button
from datetime import timedelta
import random

class TimeoutMenu(View):
    async def on_timeout(self):
        # if nobody clicked inside the timeout period, penalty applies
        if not self.clicked:
            try:
                current_time = discord.utils.utcnow()
                await self.target_member.timeout(current_time + timedelta(seconds=7), reason="Timeout game expired")
                await self.message.channel.send(f"{self.target_member.name} took too long and has been timed out for 7 seconds!")
            except Exception:
                pass
            # disable buttons visually
            for item in self.children:
                item.disabled = True
            try:
                await self.message.edit(view=self)
            except Exception:
                pass
    def __init__(self, target_member: discord.Member, timeout: float = 180.0):
        # timeout in seconds (3 minutes default)
        super().__init__(timeout=timeout)
        self.target_member = target_member
        
        # Randomly decide which button causes timeout (0 or 1)
        self.timeout_button = random.randint(0, 1)
        self.clicked = False
        
        # Create buttons with random labels
        labels = ["Left hand", "Right hand"]
        random.shuffle(labels)
        
        btn1 = Button(label=labels[0], style=discord.ButtonStyle.primary)
        btn2 = Button(label=labels[1], style=discord.ButtonStyle.primary)
        
        btn1.callback = self.button_callback(0)
        btn2.callback = self.button_callback(1)
        
        self.add_item(btn1)
        self.add_item(btn2)
    
    def button_callback(self, button_index: int):
        async def callback(interaction: discord.Interaction):
            # this handler must always send a response or defer before doing anything that could take time
            if interaction.user.id != self.target_member.id:
                # immediate reply for unauthorized users
                await interaction.response.send_message("Only the tagged member can choose.", ephemeral=True)
                return
            
            if self.clicked:
                await interaction.response.send_message("The game is already decided.", ephemeral=True)
                return
            
            # mark that a choice has been made and ack quickly
            self.clicked = True
            await interaction.response.defer()
            
            if button_index == self.timeout_button:
                current_time = discord.utils.utcnow()
                timeout_duration = timedelta(seconds=7)
                try:
                    await self.target_member.timeout(current_time + timeout_duration, reason="Lost the game")
                except Exception:
                    pass
                await interaction.followup.send(f"UNLUCKY! {self.target_member.name} has been timed out for 7 seconds!")
            else:
                await interaction.followup.send(f"LUCKY! {self.target_member.name} survives!")
            
            # disable buttons visually
            for item in self.children:
                item.disabled = True
            try:
                await interaction.message.edit(view=self)
            except Exception:
                pass
        
        return callback


async def show_timeout_menu(ctx, target_member: discord.Member):
    """Show the timeout game menu."""
    menu = TimeoutMenu(target_member)
    # use ctx.send so the interaction is acknowledged
    await ctx.send(f"{target_member.name}, pick your fate!", view=menu)