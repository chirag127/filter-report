"""Offline CLI regressions for domain-preserving rule generation."""

import pytest
from click.testing import CliRunner

from filter_report.cli import cli


@pytest.mark.parametrize(
    "domain",
    ["shop.example.com", "https://shop.example.com/path", "http://tools.example.com/path"],
)
def test_rule_preserves_hostname_characters(domain):
    """Remove URL prefixes without stripping characters from the hostname."""
    expected = "tools.example.com" if "tools." in domain else "shop.example.com"
    result = CliRunner().invoke(cli, ["rule", domain])
    assert result.exit_code == 0
    assert result.output == f"||{expected}^\n"
