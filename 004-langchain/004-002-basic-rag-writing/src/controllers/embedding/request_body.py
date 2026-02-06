from pydantic import BaseModel, field_validator


class CreateEmbeddingRequestBody(BaseModel):
  text: str

  @field_validator('text')
  @classmethod
  def validate_text(cls, text: str):
    if not text.isalnum():
      raise ValueError('Text must contain only letters and numbers')
    return text
