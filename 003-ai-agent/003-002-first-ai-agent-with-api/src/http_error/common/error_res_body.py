from typing import Any

class CommonErrorResBody(dict[str, Any]):
  def __init__(self, status_code: int, message: str) -> None:
    super().__init__(status_code=status_code, message=message)