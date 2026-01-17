from fastapi import HTTPException
from http_error.common.error_res_body import CommonErrorResBody

class BadRequestException(HTTPException):
  def __init__(self, message: str | None) -> None:
    print(f'message: {message}')
    
    super().__init__(
      status_code=400,
      detail=CommonErrorResBody(
        status_code=400,
        message=message or 'Bad request.'
      ),
      headers={}
    )