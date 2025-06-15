from config.settings import SERVER_ID, ADMIN_ID

def is_authorized(interaction):
    """
    Returns True if the interaction is from the configured admin in the correct server.
    """
    return (
        interaction.guild
        and interaction.guild.id == SERVER_ID
        and interaction.user.id == ADMIN_ID
    )
