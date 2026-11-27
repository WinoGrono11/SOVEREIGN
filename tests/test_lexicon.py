import json
from pathlib import Path

import pytest

from sovereign.lexicon import load_lexicon_fixture, validate_lexicon_fixture


FIXTURE = Path(__file__).parent / "fixtures" / "lexicon_cases.json"


def test_seed_fixture_has_valid_structure():
    payload = load_lexicon_fixture(FIXTURE)

    assert len(payload["cases"]) == 4
    assert validate_lexicon_fixture(payload) == []


def test_validator_reports_duplicate_ids_and_unknown_transformations():
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    payload["cases"][1]["id"] = payload["cases"][0]["id"]
    payload["cases"][0]["variants"][0]["transformations"] = ["concealment"]

    errors = validate_lexicon_fixture(payload)

    assert any("duplicate identifier" in error for error in errors)
    assert any("unsupported label 'concealment'" in error for error in errors)


def test_validator_rejects_missing_rubric_and_empty_variant_text():
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    payload["cases"][0]["rubric"] = []
    payload["cases"][0]["variants"][0]["text"] = "  "

    errors = validate_lexicon_fixture(payload)

    assert any(".rubric:" in error for error in errors)
    assert any(".text:" in error for error in errors)


def test_loader_raises_for_invalid_fixture(tmp_path):
    invalid = tmp_path / "invalid.json"
    invalid.write_text(json.dumps({"schema_version": "9.0", "cases": []}), encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid lexicon fixture"):
        load_lexicon_fixture(invalid)
