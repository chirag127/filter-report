"""Offline regression coverage for report preparation; never submit issues."""

from urllib.parse import parse_qs, urlparse

import pytest

from filter_report.platforms import PLATFORMS
from filter_report.report import build_report, build_reports


@pytest.mark.parametrize("platform_id", list(PLATFORMS))
def test_report_destination_and_payload(platform_id):
    """Preserve each platform destination and URL-encoded report payload."""
    url = "https://example.com/article?one=1&two=2#details"
    report = build_report(url, "ad", platform_id, selector="#banner")
    platform = PLATFORMS[platform_id]
    destination = urlparse(report["open_url"])
    expected = urlparse(platform.base_url)
    assert (destination.scheme, destination.netloc, destination.path) == (
        expected.scheme,
        expected.netloc,
        expected.path,
    )
    params = parse_qs(destination.query)
    assert report["platform_id"] == platform_id
    if platform.issue_type == "web_form":
        assert params == {"site": ["example.com"]}
    else:
        assert params["title"] == [report["title"]]
        assert params["body"] == [report["body"]]
        assert url in params["body"][0]
        assert "#banner" in params["body"][0]


def test_uassets_checklist_requires_human_confirmation():
    """Leave every uAssets prerequisite unchecked for human verification."""
    body = build_report("https://example.com", "tracker", "uassets")["body"]
    assert "- [ ] I have read" in body
    assert "- [ ] I have verified" in body
    assert "- [ ] I have searched" in body
    assert "- [x]" not in body.lower()


def test_generic_report_preserves_screenshot():
    """Retain screenshot URLs and their query parameters in report bodies."""
    screenshot = "https://example.com/screenshot.png?x=1&y=2"
    report = build_report("https://example.com", "ad", "adguard", screenshot=screenshot)
    assert screenshot in parse_qs(urlparse(report["open_url"]).query)["body"][0]


def test_multiple_reports_preserve_requested_order():
    """Return prepared reports in the caller's requested platform order."""
    ids = ["brave", "adguard", "easylist"]
    reports = build_reports("https://example.com", "ad", ids)
    assert [report["platform_id"] for report in reports] == ids


def test_unknown_platform_is_rejected():
    """Reject unknown platform identifiers instead of inventing a destination."""
    with pytest.raises(KeyError):
        build_report("https://example.com", "ad", "not-a-platform")
