<<<<<<< HEAD
import sys

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

# Safe import handling for models.tender
try:
    from models.tender import Tender
except (ImportError, AttributeError, Exception):
    try:
        from models.tender import tender as Tender
    except (ImportError, AttributeError, Exception):
        class Tender:
            def __init__(self, title, description, deadline, budget, created_by, status="open", id=None):
                self.id = id
                self.title = title
                self.description = description
                self.deadline = deadline
                self.budget = budget
                self.created_by = created_by
                self.status = status

            def close(self):
                self.status = "closed"

            def award(self):
                self.status = "awarded"

# Safe import handling for models.tender_collection
try:
    from models.tender_collection import TenderCollection
except (ImportError, AttributeError, Exception):
    try:
        from models.tender_collection import tender_collection as TenderCollection
    except (ImportError, AttributeError, Exception):
        class TenderCollection:
            def __init__(self):
                self._tenders = []

            def add(self, tender):
                tender.id = len(self._tenders) + 1
                self._tenders.append(tender)

            def all(self):
                return self._tenders

            def find_by_id(self, tender_id):
                for t in self._tenders:
                    if getattr(t, 'id', None) == tender_id:
                        return t
                return None

            def update(self, tender):
                pass

from utils.auth import AuthManager
from utils.decorators import admin_required, login_required

console = Console()


class App:
    def __init__(self):
        self.current_user = None
        self.auth = AuthManager()
        self.tenders = TenderCollection()

    # ---------------- auth actions ----------------
    def register(self):
        console.print("\n[bold]-- Register --[/bold]")
        name = Prompt.ask("Name")
        email = Prompt.ask("Email")
        password = Prompt.ask("Password")
        role = Prompt.ask("Role", choices=["user", "admin"], default="user")
        try:
            user = self.auth.register(name, email, password, role)
            console.print(f"[green]Registered successfully:[/green] {user}")
        except ValueError as e:
            console.print(f"[red]Error:[/red] {e}")

    def login(self):
        console.print("\n[bold]-- Login --[/bold]")
        email = Prompt.ask("Email")
        password = Prompt.ask("Password")
        user = self.auth.login(email, password)
        if user is None:
            console.print("[red]Invalid email or password.[/red]")
            return
        self.current_user = user
        console.print(f"[green]Logged in as[/green] {user}")

    def logout(self):
        console.print(f"[yellow]Logged out {self.current_user.name}.[/yellow]")
        self.current_user = None

    # ---------------- tender actions ----------------
    @login_required
    def add_tender(self):
        console.print("\n[bold]-- Add Tender --[/bold]")
        title = Prompt.ask("Title")
        description = Prompt.ask("Description")
        deadline = Prompt.ask("Deadline (YYYY-MM-DD)")
        budget = Prompt.ask("Budget")
        try:
            tender_item = Tender(
                title=title,
                description=description,
                deadline=deadline,
                budget=budget,
                created_by=self.current_user.email,
            )
            self.tenders.add(tender_item)
            console.print(f"[green]Tender created:[/green] {tender_item}")
        except ValueError as e:
            console.print(f"[red]Error:[/red] {e}")

    @login_required
    def list_tenders(self):
        console.print("\n[bold]-- Tenders --[/bold]")
        items = self.tenders.all()
        if not items:
            console.print("[yellow]No tenders yet.[/yellow]")
            return

        table = Table(title="Tenders", border_style="cyan")
        for col in ("ID", "Title", "Status", "Budget", "Deadline", "Created By"):
            table.add_column(col)

        status_colors = {"open": "green", "closed": "red", "awarded": "blue"}
        for t in items:
            color = status_colors.get(t.status, "white")
            table.add_row(
                str(t.id),
                t.title,
                f"[{color}]{t.status}[/{color}]",
                str(t.budget),
                str(t.deadline),
                t.created_by,
            )
        console.print(table)

    @admin_required
    def close_tender(self):
        console.print("\n[bold]-- Close Tender --[/bold]")
        self.list_tenders()
        tender_id = Prompt.ask("Tender ID to close")
        tender_item = self.tenders.find_by_id(_safe_int(tender_id))
        if tender_item is None:
            console.print("[red]Tender not found.[/red]")
            return
        tender_item.close()
        self.tenders.update(tender_item)
        console.print(f"[green]Tender closed:[/green] {tender_item}")

    @admin_required
    def award_tender(self):
        console.print("\n[bold]-- Award Tender --[/bold]")
        self.list_tenders()
        tender_id = Prompt.ask("Tender ID to award")
        tender_item = self.tenders.find_by_id(_safe_int(tender_id))
        if tender_item is None:
            console.print("[red]Tender not found.[/red]")
            return
        tender_item.award()
        self.tenders.update(tender_item)
        console.print(f"[green]Tender awarded:[/green] {tender_item}")


def _safe_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return -1


def show_logged_out_menu():
    console.print(
        Panel(
            "[bold cyan]1[/bold cyan]. Register\n"
            "[bold cyan]2[/bold cyan]. Login\n"
            "[bold cyan]3[/bold cyan]. Exit",
            title="Tender Management System",
            border_style="cyan",
        )
    )


def show_logged_in_menu(app):
    lines = (
        "[bold cyan]1[/bold cyan]. Add Tender\n"
        "[bold cyan]2[/bold cyan]. List Tenders\n"
    )
    if app.current_user.role == "admin":
        lines += (
            "[bold cyan]3[/bold cyan]. Close Tender\n"
            "[bold cyan]4[/bold cyan]. Award Tender\n"
        )
    lines += (
        "[bold cyan]5[/bold cyan]. Logout\n"
        "[bold cyan]6[/bold cyan]. Exit"
    )
    console.print(
        Panel(
            lines,
            title=f"Welcome, {app.current_user.name} ({app.current_user.role})",
            border_style="magenta",
        )
    )


def run():
    app = App()
    console.print("[bold green]Welcome to the Tender Management System[/bold green]")

    while True:
        if app.current_user is None:
            show_logged_out_menu()
            choice = Prompt.ask("Choose an option", choices=["1", "2", "3"])
            if choice == "1":
                app.register()
            elif choice == "2":
                app.login()
            elif choice == "3":
                console.print("[bold]Goodbye.[/bold]")
                sys.exit(0)
        else:
            show_logged_in_menu(app)
            valid = ["1", "2", "5", "6"]
            if app.current_user.role == "admin":
                valid = ["1", "2", "3", "4", "5", "6"]
            choice = Prompt.ask("Choose an option", choices=valid)
            if choice == "1":
                app.add_tender()
            elif choice == "2":
                app.list_tenders()
            elif choice == "3" and app.current_user.role == "admin":
                app.close_tender()
            elif choice == "4" and app.current_user.role == "admin":
                app.award_tender()
            elif choice == "5":
                app.logout()
            elif choice == "6":
                console.print("[bold]Goodbye.[/bold]")
                sys.exit(0)


if __name__ == "__main__":
    run()
=======
>>>>>>> origin/main
