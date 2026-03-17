import json
import re
from pydantic import BaseModel, ValidationError


def parse_and_validate(content: str, model: type[BaseModel]) -> dict:
    """Parse LLM response and validate against Pydantic model.

    Tries to extract JSON from the response, validates it,
    and returns a clean dict. If validation fails, returns
    error details so you know exactly what went wrong.
    """
    # Extract JSON from response (LLM sometimes wraps it in markdown)
    json_str = _extract_json(content)

    try:
        raw_data = json.loads(json_str)
    except json.JSONDecodeError as e:
        return {
            "validation_error": True,
            "error_type": "json_parse_error",
            "message": f"LLM returned invalid JSON: {e}",
            "raw": content,
        }

    try:
        validated = model.model_validate(raw_data)
        return validated.model_dump()
    except ValidationError as e:
        return {
            "validation_error": True,
            "error_type": "schema_validation_error",
            "message": str(e),
            "raw_data": raw_data,
        }


def _extract_json(text: str) -> str:
    """Extract JSON from LLM response that may contain markdown code blocks."""
    # Try to find JSON inside ```json ... ``` blocks
    match = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
    if match:
        return match.group(1).strip()

    # Try to find raw JSON object/array
    match = re.search(r"(\{[\s\S]*\}|\[[\s\S]*\])", text)
    if match:
        return match.group(1).strip()

    return text.strip()
