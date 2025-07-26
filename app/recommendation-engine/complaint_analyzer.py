import json
import re
from typing import Dict, Any
import spacy

# Extract product and issue from sentence
def extract_product_and_issue(sentence: str) -> Dict[str, str]:
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(sentence)
    product = None
    # Try to extract product as the first noun or entity
    for ent in doc.ents:
        if ent.label_ in ["PRODUCT", "ORG", "FAC", "WORK_OF_ART"]:
            product = ent.text
            break
    if not product:
        for token in doc:
            if token.pos_ == "NOUN":
                product = token.text
                break
    # Remove product from sentence to get issue
    issue = sentence
    if product:
        issue = sentence.replace(product, "").strip()
    return {"product": product, "issue": issue}


# Map issue to reason and reasonType from reason_type_mapping.json
def map_issue_to_reason_and_type(issue: str, reason_json_path: str) -> Dict[str, str]:
    with open(reason_json_path, "r") as f:
        reason_data = json.load(f)
    best_match = {"reason": None, "reasonType": None}
    max_score = 0
    for reason_type_obj in reason_data.get("businessIncidentReasonTypes", []):
        reason_type = reason_type_obj["reasonType"]
        for reason_obj in reason_type_obj.get("businessIncidentReasons", []):
            reason = reason_obj["reason"]
            # Simple matching: check if any word in reason is in issue
            score = sum(1 for word in reason.lower().split() if word in issue)
            if score > max_score:
                max_score = score
                best_match = {"reason": reason, "reasonType": reason_type}
    if best_match["reason"]:
        return best_match
    return {"reason": "Other reasons", "reasonType": "Other reasonType"}


def analyze_complaint(sentence: str, reason_json_path: str) -> Dict[str, Any]:
    result = extract_product_and_issue(sentence)
    reason_info = map_issue_to_reason_and_type(result["issue"], reason_json_path)
    return {
        "product": result["product"],
        "reason": reason_info["reason"],
        "reasonType": reason_info["reasonType"],
    }
