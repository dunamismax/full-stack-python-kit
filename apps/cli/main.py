#!/usr/bin/env python3
"""
Full-Stack Python Kit CLI Application

A comprehensive command-line interface demonstrating the capabilities
of the Full-Stack Python Kit monorepo.
"""

import json
import asyncio
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.syntax import Syntax
from rich.tree import Tree
import httpx

app = typer.Typer(
    name="fspk-cli",
    help="Full-Stack Python Kit CLI - A comprehensive command-line toolkit",
    rich_markup_mode="rich",
)

console = Console()

# Subcommands
file_app = typer.Typer(name="file", help="File operations")
api_app = typer.Typer(name="api", help="API testing utilities")
system_app = typer.Typer(name="system", help="System information")

app.add_typer(file_app, name="file")
app.add_typer(api_app, name="api")
app.add_typer(system_app, name="system")


@app.command()
def hello(
    name: str = typer.Argument("World", help="Name to greet"),
    count: int = typer.Option(1, "--count", "-c", help="Number of greetings"),
    uppercase: bool = typer.Option(False, "--uppercase", "-u", help="Uppercase output"),
) -> None:
    """Say hello to someone with style! 🎉"""
    
    greeting = f"Hello {name}!"
    if uppercase:
        greeting = greeting.upper()
    
    for i in range(count):
        if count > 1:
            console.print(f"[bold cyan]{i+1}.[/bold cyan] {greeting}")
        else:
            console.print(Panel(greeting, style="bold green"))


@file_app.command("list")
def list_files(
    path: Path = typer.Argument(Path("."), help="Directory to list"),
    show_hidden: bool = typer.Option(False, "--hidden", "-h", help="Show hidden files"),
    details: bool = typer.Option(False, "--details", "-d", help="Show file details"),
) -> None:
    """List files in a directory with optional details."""
    
    if not path.exists():
        console.print(f"[bold red]Error:[/bold red] Path '{path}' does not exist")
        raise typer.Exit(1)
    
    if not path.is_dir():
        console.print(f"[bold red]Error:[/bold red] '{path}' is not a directory")
        raise typer.Exit(1)
    
    files = []
    for item in path.iterdir():
        if not show_hidden and item.name.startswith('.'):
            continue
        files.append(item)
    
    if not files:
        console.print("[yellow]No files found[/yellow]")
        return
    
    if details:
        table = Table(title=f"Files in {path}")
        table.add_column("Name", style="cyan")
        table.add_column("Type", style="magenta")
        table.add_column("Size", style="green")
        table.add_column("Modified", style="blue")
        
        for file in sorted(files):
            stat = file.stat()
            file_type = "Directory" if file.is_dir() else "File"
            size = f"{stat.st_size:,} bytes" if file.is_file() else "-"
            modified = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M")
            
            table.add_row(file.name, file_type, size, modified)
        
        console.print(table)
    else:
        tree = Tree(f"📁 {path}")
        for file in sorted(files):
            icon = "📁" if file.is_dir() else "📄"
            tree.add(f"{icon} {file.name}")
        
        console.print(tree)


@file_app.command("read")
def read_file(
    path: Path = typer.Argument(..., help="File to read"),
    lines: Optional[int] = typer.Option(None, "--lines", "-n", help="Number of lines to show"),
    syntax: bool = typer.Option(True, "--syntax/--no-syntax", help="Enable syntax highlighting"),
) -> None:
    """Read and display file contents with syntax highlighting."""
    
    if not path.exists():
        console.print(f"[bold red]Error:[/bold red] File '{path}' does not exist")
        raise typer.Exit(1)
    
    if not path.is_file():
        console.print(f"[bold red]Error:[/bold red] '{path}' is not a file")
        raise typer.Exit(1)
    
    try:
        content = path.read_text()
        
        if lines:
            content = '\n'.join(content.split('\n')[:lines])
        
        if syntax and path.suffix:
            # Map file extensions to lexer names
            lexer_map = {
                '.py': 'python',
                '.js': 'javascript',
                '.ts': 'typescript',
                '.json': 'json',
                '.yaml': 'yaml',
                '.yml': 'yaml',
                '.toml': 'toml',
                '.md': 'markdown',
                '.html': 'html',
                '.css': 'css',
                '.sql': 'sql',
            }
            
            lexer = lexer_map.get(path.suffix.lower(), 'text')
            syntax_obj = Syntax(content, lexer, theme="monokai", line_numbers=True)
            console.print(syntax_obj)
        else:
            console.print(content)
            
    except UnicodeDecodeError:
        console.print(f"[bold red]Error:[/bold red] Cannot read '{path}' - binary file or encoding issue")
        raise typer.Exit(1)


@api_app.command("get")
def api_get(
    url: str = typer.Argument(..., help="URL to fetch"),
    headers: Optional[List[str]] = typer.Option(None, "--header", "-H", help="HTTP headers (key:value)"),
    timeout: float = typer.Option(30.0, "--timeout", "-t", help="Request timeout in seconds"),
    pretty: bool = typer.Option(True, "--pretty/--no-pretty", help="Pretty print JSON response"),
) -> None:
    """Make HTTP GET requests and display responses."""
    
    async def fetch_url():
        headers_dict = {}
        if headers:
            for header in headers:
                if ':' in header:
                    key, value = header.split(':', 1)
                    headers_dict[key.strip()] = value.strip()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task(f"Fetching {url}...", total=None)
            
            try:
                async with httpx.AsyncClient(timeout=timeout) as client:
                    response = await client.get(url, headers=headers_dict)
                
                progress.update(task, completed=100)
                
                # Display response info
                status_color = "green" if 200 <= response.status_code < 300 else "red"
                console.print(f"\n[bold {status_color}]Status:[/bold {status_color}] {response.status_code}")
                console.print(f"[bold blue]Content-Type:[/bold blue] {response.headers.get('content-type', 'unknown')}")
                console.print(f"[bold yellow]Content-Length:[/bold yellow] {len(response.content)} bytes\n")
                
                # Display response body
                content_type = response.headers.get('content-type', '').lower()
                
                if 'application/json' in content_type:
                    try:
                        json_data = response.json()
                        if pretty:
                            formatted_json = json.dumps(json_data, indent=2)
                            syntax_obj = Syntax(formatted_json, "json", theme="monokai")
                            console.print(syntax_obj)
                        else:
                            console.print(json_data)
                    except json.JSONDecodeError:
                        console.print(response.text)
                else:
                    console.print(response.text)
                    
            except httpx.TimeoutException:
                console.print(f"[bold red]Error:[/bold red] Request timed out after {timeout} seconds")
                raise typer.Exit(1)
            except httpx.RequestError as e:
                console.print(f"[bold red]Error:[/bold red] Request failed: {e}")
                raise typer.Exit(1)
    
    asyncio.run(fetch_url())


@system_app.command("info")
def system_info() -> None:
    """Display system information."""
    
    import platform
    import sys
    import os
    from datetime import datetime
    
    table = Table(title="System Information")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")
    
    # System info
    table.add_row("Platform", platform.platform())
    table.add_row("System", platform.system())
    table.add_row("Release", platform.release())
    table.add_row("Version", platform.version())
    table.add_row("Machine", platform.machine())
    table.add_row("Processor", platform.processor())
    
    # Python info
    table.add_row("Python Version", sys.version.split()[0])
    table.add_row("Python Implementation", platform.python_implementation())
    table.add_row("Python Executable", sys.executable)
    
    # Current info
    table.add_row("Current Directory", os.getcwd())
    table.add_row("Current Time", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    table.add_row("User", os.getenv("USER", "unknown"))
    
    console.print(table)


@system_app.command("env")
def show_env(
    filter_var: Optional[str] = typer.Option(None, "--filter", "-f", help="Filter by variable name"),
) -> None:
    """Display environment variables."""
    
    import os
    
    env_vars = dict(os.environ)
    
    if filter_var:
        env_vars = {k: v for k, v in env_vars.items() if filter_var.lower() in k.lower()}
    
    if not env_vars:
        console.print("[yellow]No environment variables found[/yellow]")
        return
    
    table = Table(title="Environment Variables")
    table.add_column("Variable", style="cyan")
    table.add_column("Value", style="green", overflow="fold")
    
    for key, value in sorted(env_vars.items()):
        # Mask potentially sensitive values
        if any(sensitive in key.upper() for sensitive in ['PASSWORD', 'SECRET', 'KEY', 'TOKEN']):
            value = '*' * len(value) if len(value) <= 20 else '*' * 20 + '...'
        
        table.add_row(key, value)
    
    console.print(table)


@app.command()
def version() -> None:
    """Show version information."""
    
    version_info = {
        "Full-Stack Python Kit CLI": "0.1.0",
        "Python": f"{sys.version.split()[0]}",
        "Typer": "Latest",
        "Rich": "Latest",
    }
    
    panel_content = "\n".join([f"[bold cyan]{k}:[/bold cyan] {v}" for k, v in version_info.items()])
    console.print(Panel(panel_content, title="Version Information", style="blue"))


@app.callback()
def main(
    ctx: typer.Context,
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
) -> None:
    """
    Full-Stack Python Kit CLI - A comprehensive command-line toolkit
    
    This CLI demonstrates various capabilities including file operations,
    API testing, system information, and more.
    """
    
    if verbose:
        console.print(f"[dim]Verbose mode enabled[/dim]")
        console.print(f"[dim]Command: {' '.join(ctx.params.get('args', []))}[/dim]")


if __name__ == "__main__":
    app()