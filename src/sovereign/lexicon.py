"""Structural validation for benign Lexicon Robustness Lab fixtures.

This module validates fixture shape only. It does not judge semantic equivalence,
certify that content is safe, contact a model, or transform prompts.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ALLOWED_TRANSFORMATIONS = frozenset(
    {"synonym", "syntax", "register", "context", "ambiguity", "noise"}
)


def validate_lexicon_fixture(payload: Any) -> list[str]:
    """Return path-specific validation errors for a version 1.0 fixture."""
    if not isinstance(payload, dict):
        return ["root: expected an object"]

    errors: list[str] = []
    if payload.get("schema_version") != "1.0":
        errors.append("schema_version: expected '1.0'")
    if not isinstance(payload.get("description"), str) or not payload["description"].strip():
        errors.append("description: expected a non-empty string")

    cases = payload.get("cases")
    if not isinstance(cases, list) or not cases:
        errors.append("cases: expected a non-empty list")
        return errors

    seen_ids: set[str] = set()
    for case_index, case in enumerate(cases):
        prefix = f"cases[{case_index}]"
        if not isinstance(case, dict):
            errors.append(f"{prefix}: expected an object")
            continue

        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id.strip():
            errors.append(f"{prefix}.id: expected a non-empty string")
        elif case_id in seen_ids:
            errors.append(f"{prefix}.id: duplicate identifier {case_id!r}")
        else:
            seen_ids.add(case_id)

        for field in ("source", "expected_intent"):
            value = case.get(field)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{prefix}.{field}: expected a non-empty string")

        variants = case.get("variants")
        if not isinstance(variants, list) or not variants:
            errors.append(f"{prefix}.variants: expected a non-empty list")
        else:
            for variant_index, variant in enumerate(variants):
                variant_prefix = f"{prefix}.variants[{variant_index}]"
                if not isinstance(variant, dict):
                    errors.append(f"{variant_prefix}: expected an object")
                    continue
                text = variant.get("text")
                if not isinstance(text, str) or not text.strip():
                    errors.append(f"{variant_prefix}.text: expected a non-empty string")
                transformations = variant.get("transformations")
                if not isinstance(transformations, list) or not transformations:
                    errors.append(
                        f"{variant_prefix}.transformations: expected a non-empty list"
                    )
                else:
                    for transformation_index, transformation in enumerate(transformations):
                        if transformation not in ALLOWED_TRANSFORMATIONS:
                            errors.append(
                                f"{variant_prefix}.transformations[{transformation_index}]: "
                                f"unsupported label {transformation!r}"
                            )

        rubric = case.get("rubric")
        if not isinstance(rubric, list) or not rubric:
            errors.append(f"{prefix}.rubric: expected a non-empty list")
        else:
            for rubric_index, criterion in enumerate(rubric):
                if not isinstance(criterion, str) or not criterion.strip():
                    errors.append(
                        f"{prefix}.rubric[{rubric_index}]: expected a non-empty string"
                    )

    return errors


def load_lexicon_fixture(path: str | Path) -> dict[str, Any]:
    """Load a JSON fixture and raise ValueError if its structure is invalid."""
    try:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"Could not load lexicon fixture: {exc}") from exc

    errors = validate_lexicon_fixture(payload)
    if errors:
        raise ValueError("Invalid lexicon fixture:\\n- " + "\\n- ".join(errors))
    return payload
