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