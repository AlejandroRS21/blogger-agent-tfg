"""
Utility functions for the blogger agent.
"""

import json
import re
import logging

logger = logging.getLogger(__name__)

def parse_json_from_text(text: str) -> dict:
    """
    Extracts and parses JSON from a string, handling markdown blocks.
    """
    if not text:
        return {}
    
    # Try to find JSON block
    json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.DOTALL)
    if json_match:
        text = json_match.group(1)
    else:
        # Try to find just anything between curly braces
        json_match = re.search(r'(\{.*\})', text, re.DOTALL)
        if json_match:
            text = json_match.group(1)
            
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON: {e}. Text: {text[:100]}...")
        raise
