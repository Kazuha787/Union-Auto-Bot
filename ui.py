import time
from rich.console import Console

# Initialize rich console
console = Console()

def display_banner():
    banner_text = """
██╗   ██╗    ███╗   ██╗    ██╗     ██████╗     ███╗   ██╗
██║   ██║    ████╗  ██║    ██║    ██╔═══██╗    ████╗  ██║
██║   ██║    ██╔██╗ ██║    ██║    ██║   ██║    ██╔██╗ ██║
██║   ██║    ██║╚██╗██║    ██║    ██║   ██║    ██║╚██╗██║
╚██████╔╝    ██║ ╚████║    ██║    ╚██████╔╝    ██║ ╚████║
 ╚═════╝     ╚═╝  ╚═══╝    ╚═╝     ╚═════╝     ╚═╝  ╚═══╝
"""
    console.print(f"[bold cyan]{banner_text}[/bold cyan]", justify="center")
    console.print(f"[bold green]UNION AUTO SWAP[/bold green]", justify="center")
    console.print("-" * 50, style="green", justify="center")
    for _ in range(3):
        console.print(f"[yellow]Initializing{'.' * (_ % 4)}[/yellow]", justify="center", end="\r")
        time.sleep(0.3)
    console.print(" " * 50, end="\r")
    console.print(f"[green]+ Union AUTO BIY - CREATED BY KAZUHA & UPDATED BY CryptoExplor[/green]", justify="center")
    console.print("-" * 50, style="green", justify="center")

def logger_info(msg):
    console.print(f"[bold magenta]{msg}[/bold magenta]", justify="center")

def logger_warn(msg):
    console.print(f"[bold yellow]⚠️ {msg}[/bold yellow]", justify="center")

def logger_error(msg):
    console.print(f"[bold red]❌ {msg}[/bold red]", justify="center")

def logger_success(msg):
    console.print(f"[bold green]✅ {msg}[/bold green]", justify="center")

def logger_loading(msg):
    console.print(f"[bold cyan]⏳ {msg}[/bold cyan]", justify="center")

def logger_step(msg):
    console.print(f"[bold white]👉 {msg}[/bold white]", justify="center")
