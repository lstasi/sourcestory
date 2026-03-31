"""Tests for the SourceStory CLI."""

from __future__ import annotations

from typer.testing import CliRunner

from sourcestory import __version__
from sourcestory.cli import BACKENDS, FORMATS, app

runner = CliRunner()


class TestVersion:
    """Test version display."""

    def test_version_flag(self) -> None:
        result = runner.invoke(app, ["--version"])
        assert result.exit_code == 0
        assert __version__ in result.output

    def test_short_version_flag(self) -> None:
        result = runner.invoke(app, ["-V"])
        assert result.exit_code == 0
        assert __version__ in result.output


class TestListFormats:
    """Test list-formats command."""

    def test_lists_all_formats(self) -> None:
        result = runner.invoke(app, ["list-formats"])
        assert result.exit_code == 0
        for fmt in FORMATS:
            assert fmt in result.output


class TestListBackends:
    """Test list-backends command."""

    def test_lists_all_backends(self) -> None:
        result = runner.invoke(app, ["list-backends"])
        assert result.exit_code == 0
        for b in BACKENDS:
            assert b in result.output


class TestGenerate:
    """Test generate command."""

    def test_generate_prints_info(self) -> None:
        result = runner.invoke(app, ["generate", "some/path"])
        assert result.exit_code == 0
        assert "some/path" in result.output

    def test_generate_invalid_format(self) -> None:
        result = runner.invoke(app, ["generate", "some/path", "--format", "invalid"])
        assert result.exit_code == 1
        assert "Unknown format" in result.output

    def test_generate_invalid_backend(self) -> None:
        result = runner.invoke(app, ["generate", "some/path", "--backend", "invalid"])
        assert result.exit_code == 1
        assert "Unknown backend" in result.output

    def test_generate_custom_options(self) -> None:
        result = runner.invoke(
            app,
            ["generate", "my_project/", "--format", "podcast", "--model", "llama3"],
        )
        assert result.exit_code == 0
        assert "podcast" in result.output
        assert "my_project/" in result.output
        assert "llama3" in result.output


class TestPackage:
    """Test package-level attributes."""

    def test_version_string(self) -> None:
        assert isinstance(__version__, str)
        parts = __version__.split(".")
        assert len(parts) == 3
