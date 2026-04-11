"""Tests for Jinja2 prompt templates."""

from __future__ import annotations

from pathlib import Path

import jinja2
import pytest

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "sourcestory" / "templates"

TEMPLATE_NAMES = ["book_chapter.j2", "podcast.j2", "summary.j2", "readme.j2"]

SAMPLE_CHUNKS = [
    {
        "symbol_name": "hello_world",
        "narrative": "A simple greeting function.",
        "language": "python",
        "code": 'def hello_world():\n    print("Hello!")',
    },
    {
        "symbol_name": "add",
        "narrative": "Adds two numbers together.",
        "language": "python",
        "code": "def add(a, b):\n    return a + b",
    },
]


@pytest.fixture()
def jinja_env() -> jinja2.Environment:
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=False,
    )


class TestTemplatesExist:
    """Ensure all expected templates are present."""

    @pytest.mark.parametrize("name", TEMPLATE_NAMES)
    def test_template_file_exists(self, name: str) -> None:
        assert (TEMPLATES_DIR / name).is_file(), f"Missing template: {name}"


class TestTemplateRendering:
    """Render each template with sample data and verify output."""

    @pytest.mark.parametrize("name", TEMPLATE_NAMES)
    def test_renders_without_error(
        self, jinja_env: jinja2.Environment, name: str
    ) -> None:
        template = jinja_env.get_template(name)
        output = template.render(
            title="Test Project",
            preamble="An overview of the test project.",
            chunks=SAMPLE_CHUNKS,
        )
        assert len(output) > 0
        assert "hello_world" in output
        assert "add" in output

    def test_book_chapter_has_headings(self, jinja_env: jinja2.Environment) -> None:
        template = jinja_env.get_template("book_chapter.j2")
        output = template.render(title="Test", preamble="Intro.", chunks=SAMPLE_CHUNKS)
        assert "## hello_world" in output
        assert "## add" in output

    def test_podcast_has_hosts(self, jinja_env: jinja2.Environment) -> None:
        template = jinja_env.get_template("podcast.j2")
        output = template.render(title="Test", preamble="Intro.", chunks=SAMPLE_CHUNKS)
        assert "Alex" in output
        assert "Jordan" in output

    def test_summary_has_bullets(self, jinja_env: jinja2.Environment) -> None:
        template = jinja_env.get_template("summary.j2")
        output = template.render(title="Test", preamble="Intro.", chunks=SAMPLE_CHUNKS)
        assert "- **hello_world**" in output
        assert "- **add**" in output
