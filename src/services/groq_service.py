import requests
import json
import logging
from src.core.config import (
    REQUIRED_FIELDS,
    GROQ_API_KEY,
    GROQ_API_URL,
    LLMMODEL
)

def build_invoice_prompt(file_text):
    return {
        "function": "extract",
        "extract": [
            "invoice_number (string)",
            "invoice_date (string, format: DD-MMM-YYYY if possible)",
            "vendor_name (string)",
            "vendor_address (string or null)",
            "port_name (string or null)",
            "port_address (string or null)",
            "customer_name (string or null)",
            "customer_address (string or null)",
            "excl_tax_amount (number)",
            "tax_amount (number)",
            "discount_amount (number)",
            "total_amount (number)",
            "currency (string, e.g. USD, INR)",
            "line_items (array of {description, quantity, unit_price, excl_tax_amount, tax_amount, discount_amount, total_amount})"
        ],
        "file_text": file_text,
        "instruction": (
            "The following is raw text extracted from an invoice. "
            "If amounts are already included in line items and also shown in a summary, do not double-count them. "
            "Focus only on the final summary block if available. "
            "Respond with only valid JSON. No explanation or extra text. "
            "For fields with 'must be one of', return only an exact match or null."
        )
    }

def strip_json_codeblock(response_text):
    if response_text.startswith("```json") and response_text.endswith("```"):
        return response_text.strip("```json").strip("```").strip()
    return response_text

def safe_json_parse(response_text, task_log):
    try:
        return json.loads(response_text)
    except json.JSONDecodeError as e:
        task_log["groq_response"] = response_text
        task_log["groq_error"] = str(e)
        logging.error(f"[Groq JSON Parse Error] {e}")
        return None

def parse_invoice_with_groq(file_text, task_log):
    prompt = build_invoice_prompt(file_text)

    payload = {
        "model": LLMMODEL,
        "messages": [{"role": "user", "content": json.dumps(prompt)}],
        "temperature": 0.2
    }

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        task_log["groq_payload"] = payload
        response = requests.post(
            GROQ_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        task_log["groq_error"] = str(e)
        logging.error(f"Error calling Groq API: {e}")
        return None

def filter_required_fields(parsed_data):
    """
    Returns a new dict containing only the required fields from parsed_data.
    """
    return {k: v for k, v in parsed_data.items() if k in REQUIRED_FIELDS}

def validate_invoice_json(invoice_json, task_log):
    if not invoice_json or "choices" not in invoice_json or not invoice_json["choices"]:
        logging.error("Invalid response from Groq API")
        logging.error(f"Raw response: {invoice_json}")
        return None

    response_text = invoice_json["choices"][0]["message"]["content"].strip()

    cleaned_text = strip_json_codeblock(response_text)
    parsed_data = safe_json_parse(cleaned_text, task_log)
    if not parsed_data:
        return None

    print(f"Parsed JSON data: {json.dumps(parsed_data, indent=2)}")
    # Filter to only required fields
    filtered_data = filter_required_fields(parsed_data)

    # Optionally, check if all required fields are present
    # for key in REQUIRED_FIELDS:
    #     if key not in filtered_data:
    #         logging.error(f"Missing key in JSON response: {key}")
    #         return None

    task_log["groq_response"] = filtered_data
    return filtered_data

# Usage example for invoice extraction:
# invoice_json = parse_invoice_with_groq(file_text, task_log)
# validated_invoice = validate_invoice_json(invoice_json, task_log)
