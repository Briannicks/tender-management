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

