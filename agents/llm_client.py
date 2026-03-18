from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import time
import logging

load_dotenv()

logger = logging.getLogger(__name__)

MAX_RETRIES = 3
RETRY_DELAYS = [2, 5, 10]  # seconds - exponential backoff


def get_llm():

    return ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.5
    )


def call_llm_with_retry(chain, inputs: dict) -> str:
    """Call LLM chain with automatic retry on failure.

    Handles: rate limits, network errors, empty responses.
    Returns the response content string.
    """
    last_error = None

    for attempt in range(MAX_RETRIES):
        try:
            result = chain.invoke(inputs)

            if not result or not result.content or not result.content.strip():
                logger.warning(f"[Attempt {attempt + 1}] LLM returned empty response, retrying...")
                last_error = "LLM returned empty response"
                time.sleep(RETRY_DELAYS[attempt])
                continue

            return result.content

        except Exception as e:
            last_error = str(e)
            error_lower = last_error.lower()

            # Rate limit - wait longer
            if "rate_limit" in error_lower or "429" in error_lower:
                wait = RETRY_DELAYS[attempt] * 3
                logger.warning(f"[Attempt {attempt + 1}] Rate limited. Waiting {wait}s...")
                time.sleep(wait)

            # Network / timeout errors - standard retry
            elif any(word in error_lower for word in ["timeout", "connection", "network", "502", "503"]):
                wait = RETRY_DELAYS[attempt]
                logger.warning(f"[Attempt {attempt + 1}] Network error: {e}. Retrying in {wait}s...")
                time.sleep(wait)

            # Auth error - no point retrying
            elif "401" in error_lower or "auth" in error_lower or "api_key" in error_lower:
                logger.error(f"Authentication error: {e}")
                raise

            # Unknown error - retry with standard delay
            else:
                wait = RETRY_DELAYS[attempt]
                logger.warning(f"[Attempt {attempt + 1}] Error: {e}. Retrying in {wait}s...")
                time.sleep(wait)

    raise RuntimeError(f"LLM call failed after {MAX_RETRIES} attempts. Last error: {last_error}")
