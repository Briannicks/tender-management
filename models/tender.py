class Tender:
    """A single tender entry."""

    _next_id = 1  
    STATUSES = ("open", "closed", "awarded")

    def __init__(self, title, description, deadline, budget, created_by,
                 status="open", tender_id=None):
        if tender_id is None:
            tender_id = Tender._next_id
            Tender._next_id += 1
        else:
            Tender._next_id = max(Tender._next_id, tender_id + 1)

        self._id = tender_id
        self._title = title
        self._description = description
        self._deadline = deadline
        self._budget = budget
        self._created_by = created_by
        self.status = status 
    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not value or not value.strip():
            raise ValueError("Tender title cannot be empty.")
        self._title = value.strip()

    @property
    def created_by(self):
        return self._created_by

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value or ""

    @property
    def deadline(self):
        return self._deadline

    @deadline.setter
    def deadline(self, value):
        self._deadline = value

    @property
    def budget(self):
        return self._budget

    @budget.setter
    def budget(self, value):
        self._budget = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if value not in Tender.STATUSES:
            raise ValueError(f"Status must be one of {Tender.STATUSES}.")
        self._status = value

    def close(self):
        self._status = "closed"

    def award(self):
        self._status = "awarded"
    def to_dict(self):
        return {
            "id": self._id,
            "title": self._title,
            "description": self._description,
            "deadline": self._deadline,
            "budget": self._budget,
            "created_by": self._created_by,
            "status": self._status,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            title=data["title"],
            description=data.get("description", ""),
            deadline=data.get("deadline"),
            budget=data.get("budget"),
            created_by=data["created_by"],
            status=data.get("status", "open"),
            tender_id=data["id"],
        )

    def __str__(self):
        return f"[{self._id}] {self._title} - {self._status} (budget: {self._budget}, deadline: {self._deadline})"

