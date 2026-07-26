from __future__ import annotations

import platform
import sqlite3
import sys
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table
from sqlalchemy import inspect, select

from ekb import __version__
from ekb.core.config import get_settings
from ekb.core.logging import configure_logging
from ekb.db.models import Collection
from ekb.db.session import build_engine, build_session_factory
from ekb.services.database import init_database, seed_collections

app = typer.Typer(help="EURLEX Knowledge DB — base réglementaire Banque & Finance")
db_app = typer.Typer(help="Gestion de la base SQLite")
collection_app = typer.Typer(help="Gestion des collections réglementaires")
app.add_typer(db_app, name="db")
app.add_typer(collection_app, name="collection")
console = Console()


def version_callback(value: bool) -> None:
    if value:
        console.print(f"ekb {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        False, "--version", callback=version_callback, is_eager=True, help="Afficher la version"
    )
) -> None:
    settings = get_settings()
    configure_logging(settings.app.log_level)


@app.command()
def doctor() -> None:
    """Vérifie la configuration et l'environnement local."""
    settings = get_settings()
    settings.ensure_directories()

    checks = [
        ("Python", platform.python_version(), sys.version_info >= (3, 11)),
        ("Configuration", "config/settings.toml", Path("config/settings.toml").exists()),
        ("Répertoire raw", str(settings.storage.raw_dir), settings.storage.raw_dir.exists()),
        ("Répertoire exports", str(settings.storage.exports_dir), settings.storage.exports_dir.exists()),
        ("SQLite", sqlite3.sqlite_version, True),
    ]

    table = Table(title="Diagnostic EKB")
    table.add_column("Contrôle")
    table.add_column("Valeur")
    table.add_column("État")
    for label, value, ok in checks:
        table.add_row(label, value, "[green]OK[/green]" if ok else "[red]À corriger[/red]")
    console.print(table)
    if not all(item[2] for item in checks):
        raise typer.Exit(code=1)


@db_app.command("init")
def db_init() -> None:
    """Crée les tables initiales."""
    tables = init_database(get_settings())
    console.print(f"[green]Base initialisée.[/green] Tables: {', '.join(sorted(tables))}")


@db_app.command("status")
def db_status() -> None:
    """Affiche l'état du schéma local."""
    engine = build_engine(get_settings())
    tables = inspect(engine).get_table_names()
    if not tables:
        console.print("[yellow]Base non initialisée.[/yellow]")
        raise typer.Exit(code=1)
    console.print("Tables présentes:")
    for name in sorted(tables):
        console.print(f"  • {name}")


@collection_app.command("seed")
def collection_seed() -> None:
    """Ajoute les collections Banque & Finance initiales."""
    init_database(get_settings())
    created = seed_collections(get_settings())
    console.print(f"[green]{created} collection(s) créée(s).[/green]")


@collection_app.command("list")
def collection_list() -> None:
    """Liste les collections enregistrées."""
    engine = build_engine(get_settings())
    factory = build_session_factory(engine)
    with factory() as session:
        rows = session.scalars(select(Collection).order_by(Collection.code)).all()
    if not rows:
        console.print("Aucune collection. Lance: ekb collection seed")
        return
    table = Table(title="Collections réglementaires")
    table.add_column("Code")
    table.add_column("Nom")
    table.add_column("Description")
    for row in rows:
        table.add_row(row.code, row.name, row.description or "")
    console.print(table)
