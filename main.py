import sys
import subprocess
import os
from pathlib import Path
from nextcord.ext import commands
import warnings
from nextcord.ext.commands.bot import MissingMessageContentIntentWarning
from config.settings import SERVER_ID, ADMIN_ID, get_missing_config_warnings
from rich.console import Console

warnings.filterwarnings("ignore", category=MissingMessageContentIntentWarning)

console = Console()
DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

def ensure_env_and_requirements():
    # Check if running inside a venv
    if sys.prefix == sys.base_prefix:
        venv_dir = Path("venv")
        if not venv_dir.exists():
            console.print("[bold yellow]Creating virtual environment...[/bold yellow]")
            subprocess.check_call([sys.executable, "-m", "venv", "venv"])
        # Activate venv for this process
        activate_script = venv_dir / "Scripts" / "activate_this.py" if os.name == "nt" else venv_dir / "bin" / "activate_this.py"
        exec(open(activate_script).read(), dict(__file__=str(activate_script)))
    # Install requirements if needed
    req_file = Path("requirements.txt")
    if req_file.exists():
        console.print("[bold yellow]Installing requirements...[/bold yellow]")
        result = subprocess.call([sys.executable, "-m", "pip", "install", "-r", str(req_file)])
        if result == 0:
            clear_screen()
        else:
            console.print("[red]Error installing requirements. Please check the output above.[/red]")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Run setup before importing app
ensure_env_and_requirements()

bot = commands.Bot(command_prefix="!")

# Load the PenguinCommands cog
from api.routes import setup as setup_penguin_commands
setup_penguin_commands(bot)

def print_config_checks():
    messages = []
    if DISCORD_TOKEN:
        messages.append("[green]Found Discord token.[/green]")
    else:
        messages.append("[red][CONFIG WARNING] Discord token not found (DISCORD_BOT_TOKEN missing in .env).[/red]")
    if ADMIN_ID:
        messages.append("[green]Found admin id.[/green]")
    else:
        messages.append("[red][CONFIG WARNING] Admin ID not found.[/red]")
    if SERVER_ID:
        messages.append("[green]Found server id.[/green]")
    else:
        messages.append("[red][CONFIG WARNING] Server ID not found.[/red]")
    console.print("\n".join(messages))

def get_startup_banner():
    banner_path = Path(__file__).parent / "data" / "ascii_banner.txt"
    if banner_path.exists():
        with open(banner_path, "r", encoding="utf-8") as f:
            banner = f.read()
        return f"[bold cyan]{banner}[/bold cyan]\nWarning: Starting Penguin Discord Bot..."
    return "[bold cyan]Penguin Discord Bot[/bold cyan]\nWarning: Starting Penguin Discord Bot..."

@bot.event
async def on_ready():
    if bot.user is not None:
        login_msg = f"[bold green]Logged in as {bot.user} (ID: {bot.user.id})[/bold green]"
    else:
        login_msg = "[bold yellow]Logged in, but bot user is None.[/bold yellow]"
    console.print(login_msg)
    warnings = get_missing_config_warnings()
    if warnings:
        console.print("\n".join(f"[yellow]{w}[/yellow]" for w in warnings))
    else:
        console.print("[bold green]All required config values are set.[/bold green]")
    # Show loaded cogs
    if bot.cogs:
        console.print("[bold blue]Loaded cogs:[/bold blue]")
        for cog_name in bot.cogs:
            console.print(f" - [cyan]{cog_name}[/cyan]")
    else:
        console.print("[yellow]No cogs loaded.[/yellow]")

if __name__ == "__main__":
    print_config_checks()
    console.print(get_startup_banner())
    bot.run(DISCORD_TOKEN)