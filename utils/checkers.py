from nextcord import Interaction
from config.settings import SERVER_ID, ADMIN_ID

def admin_and_server_only():
    """
    Decorator for Nextcord slash commands to allow only the configured admin in the configured server.
    """
    def predicate(interaction: Interaction):
        return (
            interaction.guild
            and interaction.guild.id == SERVER_ID
            and interaction.user is not None
            and interaction.user.id == ADMIN_ID
        )
    return predicate
