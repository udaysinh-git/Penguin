import nextcord
from nextcord.ext import commands
from utils.validators import is_authorized
from services.port_service import PortService
import asyncio

TEST_GUILD_ID = 1383698902942748762  # Replace with your test guild/server ID

class PenguinCommands(commands.Cog):
    """Cog for Penguin bot slash commands."""

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="ports",
        description="Show running services and their ports",
        guild_ids=[TEST_GUILD_ID]
    )
    async def ports(self, interaction: nextcord.Interaction):
        if not is_authorized(interaction):
            await interaction.response.send_message("You are not authorized to use this command.", ephemeral=True)
            return

        ports = PortService.get_ports_info()
        local_ip = PortService.get_local_ip()
        if not ports:
            await interaction.response.send_message("No listening services found.", ephemeral=True)
            return

        embed = nextcord.Embed(
            title="Running Services and Ports",
            description="Click the button to open the service in your browser.",
            color=nextcord.Color.blue()
        )
        for entry in ports:
            name = entry['name']
            port = entry['port']
            url = f"http://{local_ip}:{port}"
            embed.add_field(name=name, value=f"Port: `{port}`\n[Open]({url})", inline=False)

        class PortsView(nextcord.ui.View):
            def __init__(self):
                super().__init__()
                for entry in ports[:25]:
                    port = entry['port']
                    url = f"http://{local_ip}:{port}"
                    label = f"{entry['name']} ({port})"
                    self.add_item(nextcord.ui.Button(label=label, url=url))

        # Find the "ports" channel in the "mypc" guild and send the embed there
        guild = nextcord.utils.get(self.bot.guilds, name="mypc")
        if guild:
            channel = nextcord.utils.get(guild.text_channels, name="ports")
            if channel:
                await channel.send(embed=embed, view=PortsView())
                await interaction.response.send_message("Ports info sent to #ports channel.", ephemeral=True)
                return

        await interaction.response.send_message("Could not find 'ports' channel in 'mypc' guild.", ephemeral=True)

    @nextcord.slash_command(
        name="purge",
        description="Purge all messages in this channel",
        guild_ids=[TEST_GUILD_ID]
    )
    async def purge(self, interaction: nextcord.Interaction):
        if not is_authorized(interaction):
            await interaction.response.send_message("You are not authorized to use this command.", ephemeral=True)
            return
        channel = interaction.channel
        await interaction.response.send_message("Purging messages...", ephemeral=True)
        deleted = await channel.purge()
        msg = await interaction.followup.send(f"Purged {len(deleted)} messages.")
        await asyncio.sleep(3)
        await msg.delete()

def setup(bot):
    bot.add_cog(PenguinCommands(bot))
