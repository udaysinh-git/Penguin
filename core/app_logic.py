import asyncio
import nextcord
from config.settings import DISCORD_BOT_TOKEN
from utils.error_handler import print_error, print_warning, print_info, print_success
from data.data_loader import get_logs_channel_id, set_logs_channel_id
from utils.system_stats import get_system_stats_embed
from pathlib import Path
from services.port_service import PortService
from utils.service_filter import get_service_filter

LOGS_CATEGORY_NAME = "🖥️ My PC"
LOGS_CHANNEL_NAME = "📋-logs"
PORTS_CHANNEL_NAME = "ports"

def load_ascii_banner():
    banner_path = Path(__file__).parent.parent / "data" / "ascii_banner.txt"
    if banner_path.exists():
        with open(banner_path, "r", encoding="utf-8") as f:
            return f.read()
    return "Penguin Discord Bot"

class MyBot(nextcord.Client):
    async def on_ready(self):
        if self.user is not None:
            print_success(f"Logged in as {self.user} (ID: {self.user.id})")
        else:
            print_warning("Bot user is None. Could not retrieve user information.")
        print_info("------")
        # Ensure logs channel exists and send stats
        await self.ensure_logs_channel_and_send_stats()
        # Ensure ports channel exists and send ports info
        await self.ensure_ports_channel_and_send_ports()

    async def ensure_logs_channel_and_send_stats(self):
        guild = nextcord.utils.get(self.guilds)
        if not guild:
            print_error("No guilds found for this bot.")
            return

        # Try to get channel by stored ID
        channel_id = get_logs_channel_id()
        channel = None
        if channel_id:
            channel = guild.get_channel(channel_id)
        # If not found, create category/channel as needed
        if not channel:
            # Find or create category
            category = nextcord.utils.get(guild.categories, name=LOGS_CATEGORY_NAME)
            if not category:
                category = await guild.create_category(LOGS_CATEGORY_NAME)
            # Find or create channel
            channel = nextcord.utils.get(category.channels, name=LOGS_CHANNEL_NAME)
            if not channel:
                channel = await guild.create_text_channel(LOGS_CHANNEL_NAME, category=category)
            set_logs_channel_id(channel.id)
        # Send system stats embed
        embed = get_system_stats_embed()
        if isinstance(channel, nextcord.TextChannel):
            await channel.send(embed=embed)
        else:
            print_error("Logs channel is not a TextChannel. Cannot send embed.")

    async def ensure_ports_channel_and_send_ports(self):
        """
        Ensures a 'ports' channel exists under the 'my-pc' category and sends the filtered ports/services embed there.
        Only sends if the filter file contains at least one service name and there are matches.
        """
        guild = nextcord.utils.get(self.guilds)
        if not guild:
            print_error("No guilds found for this bot.")
            return

        # Find or create category
        category = nextcord.utils.get(guild.categories, name=LOGS_CATEGORY_NAME)
        if not category:
            category = await guild.create_category(LOGS_CATEGORY_NAME)
        # Find or create ports channel
        channel = nextcord.utils.get(category.channels, name=PORTS_CHANNEL_NAME)
        if not channel:
            channel = await guild.create_text_channel(PORTS_CHANNEL_NAME, category=category)

        service_filter = get_service_filter()
        if not service_filter:
            return

        ports = PortService.get_ports_info()
        filtered_ports = [
            entry for entry in ports
            if entry['name'].lower() in {name.lower() for name in service_filter}
        ]
        if not filtered_ports:
            return

        local_ip = PortService.get_local_ip()
        embed = nextcord.Embed(
            title="Filtered Services and Ports",
            description="Click the button to open the service in your browser.",
            color=nextcord.Color.blue()
        )
        for entry in filtered_ports:
            name = entry['name']
            port = entry['port']
            url = f"http://{local_ip}:{port}"
            embed.add_field(name=name, value=f"Port: `{port}`\n[Open]({url})", inline=False)

        class PortsView(nextcord.ui.View):
            def __init__(self):
                super().__init__()
                for entry in filtered_ports[:25]:
                    port = entry['port']
                    url = f"http://{local_ip}:{port}"
                    label = f"{entry['name']} ({port})"
                    self.add_item(nextcord.ui.Button(label=label, url=url))

        if isinstance(channel, nextcord.TextChannel):
            await channel.send(embed=embed, view=PortsView())
        else:
            print_error("Ports channel is not a TextChannel. Cannot send embed.")

async def send_ports_info_to_channel(bot: nextcord.Client):
    """
    Sends the filtered service/port info as an embed to the #ports channel in the 'mypc' guild.
    Only sends if the filter file contains at least one service name and there are matches.
    """
    service_filter = get_service_filter()
    if not service_filter:
        return

    ports = PortService.get_ports_info()
    # Only match exact names from the filter (case-insensitive)
    filtered_ports = [
        entry for entry in ports
        if entry['name'].lower() in {name.lower() for name in service_filter}
    ]
    if not filtered_ports:
        return

    local_ip = PortService.get_local_ip()
    embed = nextcord.Embed(
        title="Filtered Services and Ports",
        description="Click the button to open the service in your browser.",
        color=nextcord.Color.blue()
    )
    for entry in filtered_ports:
        name = entry['name']
        port = entry['port']
        url = f"http://{local_ip}:{port}"
        embed.add_field(name=name, value=f"Port: `{port}`\n[Open]({url})", inline=False)

    class PortsView(nextcord.ui.View):
        def __init__(self):
            super().__init__()
            for entry in filtered_ports[:25]:
                port = entry['port']
                url = f"http://{local_ip}:{port}"
                label = f"{entry['name']} ({port})"
                self.add_item(nextcord.ui.Button(label=label, url=url))

    await bot.wait_until_ready()
    guild = nextcord.utils.get(bot.guilds, name="mypc")
    if guild:
        channel = nextcord.utils.get(guild.text_channels, name="ports")
        if channel:
            await channel.send(embed=embed, view=PortsView())

def print_startup():
    ascii_banner = load_ascii_banner()
    print_info(ascii_banner)
    print_warning("Starting Penguin Discord Bot...")

async def run_bot():
    print_startup()
    bot = MyBot(intents=nextcord.Intents.default())
    if not isinstance(DISCORD_BOT_TOKEN, str) or not DISCORD_BOT_TOKEN:
        print_error("DISCORD_BOT_TOKEN is not set or is not a valid string.")
        return
    while True:
        try:
            await bot.start(DISCORD_BOT_TOKEN)
        except (nextcord.errors.LoginFailure, KeyboardInterrupt):
            raise
        except Exception as e:
            print_error(f"Network error or disconnect: {e}")
            print_warning("Retrying in 10 seconds...")
            await asyncio.sleep(10)

def start():
    asyncio.run(run_bot())
