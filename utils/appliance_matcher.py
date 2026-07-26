"""
Smart Energy Advisor
Appliance Matcher

Responsibilities:
- Load appliance knowledge base
- Normalize appliance names
- Resolve synonyms
- Match exact appliance rules
- Match category keyword rules
- Provide deterministic fallback matching

No calculations.
No suggestions formatting.
No database access.
"""

import json
import re
from pathlib import Path
from typing import Dict, Any, Optional


BASE_DIR = Path(__file__).resolve().parent.parent

KNOWLEDGE_PATH = (
    BASE_DIR
    / "knowledge"
    / "appliance_rules.json"
)


def load_rules() -> Dict[str, Any]:
    """
    Loads appliance knowledge base JSON.
    """

    if not KNOWLEDGE_PATH.exists():
        raise FileNotFoundError(
            f"Knowledge base not found: {KNOWLEDGE_PATH}"
        )

    with open(
        KNOWLEDGE_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def normalize_name(name: str) -> str:
    """
    Normalizes appliance names.

    Operations:
    - convert to lowercase
    - remove leading/trailing spaces
    - remove repeated whitespace
    """

    if not isinstance(name, str):
        return ""

    name = name.lower()

    name = name.strip()

    name = re.sub(
        r"\s+",
        " ",
        name
    )

    return name


def resolve_synonym(
    name: str,
    synonyms: Dict[str, str]
) -> str:
    """
    Resolves a single synonym.

    Only one lookup is performed.
    No recursive chaining.
    """

    return synonyms.get(
        name,
        name
    )


def match_exact_rule(
    name: str,
    exact_rules: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """
    Matches exact appliance rules.
    """

    if name in exact_rules:

        return {
            "match_type": "exact",
            "matched_name": name,
            "rule": exact_rules[name]
        }

    return None


def contains_whole_word(
    text: str,
    keyword: str
) -> bool:
    """
    Checks whole-word keyword match.

    Example:

    motor
    matches:
        electric motor

    does not match:
        motorized curtain
    """

    pattern = (
        r"\b"
        + re.escape(keyword)
        + r"\b"
    )

    return re.search(
        pattern,
        text
    ) is not None


def match_category_rule(
    name: str,
    category_rules: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """
    Matches category rules using:

    1. Whole-word matching
    2. Longest keyword priority
    3. Alphabetical category tie-break
    """

    matches = []


    for category, rule_data in category_rules.items():

        keywords = rule_data.get(
            "keywords",
            []
        )

        for keyword in keywords:

            keyword = normalize_name(keyword)

            if contains_whole_word(
                name,
                keyword
            ):

                matches.append(
                    {
                        "category": category,
                        "keyword": keyword,
                        "rule": rule_data,
                        "keyword_length": len(keyword)
                    }
                )


    if not matches:
        return None


    matches.sort(
        key=lambda item: (
            -item["keyword_length"],
            item["category"]
        )
    )


    best_match = matches[0]


    return {
        "match_type": "category",
        "category": best_match["category"],
        "keyword": best_match["keyword"],
        "rule": best_match["rule"]
    }


def match_appliance(
    name: str,
    knowledge_base: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Main appliance matching pipeline.

    Flow:

    Normalize

    ↓

    Synonym resolution

    ↓

    Exact rule

    ↓

    Category keyword rule

    ↓

    Generic fallback
    """

    if knowledge_base is None:
        knowledge_base = load_rules()


    normalized_name = normalize_name(name)


    normalized_name = resolve_synonym(
        normalized_name,
        knowledge_base.get(
            "synonyms",
            {}
        )
    )


    exact_match = match_exact_rule(
        normalized_name,
        knowledge_base.get(
            "exact_rules",
            {}
        )
    )


    if exact_match:
        return exact_match


    category_match = match_category_rule(
        normalized_name,
        knowledge_base.get(
            "category_rules",
            {}
        )
    )


    if category_match:
        return category_match


    return {
        "match_type": "generic",
        "rule": knowledge_base.get(
            "generic_rule",
            {}
        )
    }