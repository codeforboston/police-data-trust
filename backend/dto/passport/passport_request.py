from ...database.models import UserRole

class PassportRequestDTO:
  user_id: int
  role: UserRole
