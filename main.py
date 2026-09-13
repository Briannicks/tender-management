import sys

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

# Try importing Tender, with fallback if models/tender.py is still empty
try:
    from models.tender import Tender
except ImportError:
    try:
        from models.tender import tender as Tender
    except ImportError:
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

from models.tender_collection import TenderCollection
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
        password = Prompt.ask("Password", password=True)
        role = Prompt.ask("Role", choices=["user", "admin"], default="user")
        try:
            user = self.auth.register(name, email, password, role)
            console.print(f"[green]Registered successfully:[/green] {user}")
        except ValueError as e:
            console.print(f"[red]Error:[/red] {e}")

    def login(self):
        console.print("\n[bold]-- Login --[/bold]")
        email = Prompt.ask("Email")
        password = Prompt.ask("Password", password=True)
        user = self.auth.login(email, password)
        if user is None:
            console.print("[red]Invalid email or password.[/red]")
            return
        self.current_user = user
        console.print(f"[green]Logged in as[/green] {user}")

    def logout(self):
        console.print(f"[yellow]Logged out {self.current_user.name}.[/yellow]")
        self.current_user = None
  #---------------- tender actions ----------------
@login_required
def create_tender(self): 
    console.print("\n[bold]-- Create Tender --[/bold]")    
        