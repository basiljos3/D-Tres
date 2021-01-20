from typing import List


class UserProfile:
    def __init__(
        self, stud_details: str = None, list_save: List[str] = None, student_id: int = None
    ):
        self.stud_details: str = stud_details
        self.student_id: int = student_id
        self.list_save: List[str] = list_save
