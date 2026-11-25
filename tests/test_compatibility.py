"""Regression checks for the declared Python 3.9 annotation contract."""

from filter_report.platforms import Platform
from filter_report.report import build_report


def test_optional_template_annotation_is_postponed():
    """Avoid evaluating PEP 604 unions during module import on Python 3.9."""
    assert Platform.__annotations__["template"] == "str | None"
    assert Platform("sample", "Sample", "", "web_form", "https://example.com").template is None


def test_uassets_documentation_checklist_text_is_preserved():
    """Keep the original prerequisite link and human-only unchecked state."""
    body = build_report("https://example.com", "ad", "uassets")["body"]
    assert (
        "- [ ] I have read the [documentation]"
        "(https://github.com/uBlockOrigin/uAssets/blob/master/CONTRIBUTING.md)"
    ) in body
    assert "- [x]" not in body.lower()
