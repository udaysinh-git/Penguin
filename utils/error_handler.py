from rich.console import Console

console = Console()

def print_error(message: str):
    """Prints an error message in red."""
    console.print(f"[bold red]Error:[/bold red] {message}")

def print_warning(message: str):
    """Prints a warning message in yellow."""
    console.print(f"[yellow]Warning:[/yellow] {message}")

def print_info(message: str):
    """Prints an info message in cyan."""
    console.print(f"[cyan]{message}[/cyan]")

def print_success(message: str):
    """Prints a success message in green."""
    console.print(f"[bold green]{message}[/bold green]")
