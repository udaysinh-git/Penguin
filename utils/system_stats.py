import platform
import psutil
import socket
import nextcord

def get_system_stats_embed():
    uname = platform.uname()
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)

    embed = nextcord.Embed(
        title="🖥️ System Stats",
        color=0x00bfff,
        description=f"**Host:** `{hostname}`\n**IP:** `{ip}`"
    )
    embed.add_field(name="OS", value=f"{uname.system} {uname.release}", inline=True)
    embed.add_field(name="CPU Usage", value=f"{cpu}%", inline=True)
    embed.add_field(name="RAM Usage", value=f"{mem.percent}% ({mem.used // (1024**2)}MB/{mem.total // (1024**2)}MB)", inline=True)
    embed.add_field(name="Disk Usage", value=f"{disk.percent}% ({disk.used // (1024**3)}GB/{disk.total // (1024**3)}GB)", inline=True)
    embed.set_footer(text="Penguin Bot Startup Stats")
    return embed
