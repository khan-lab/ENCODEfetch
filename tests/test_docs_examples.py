import re
import shlex
from pathlib import Path

from click.exceptions import Exit

from encodefetch.cli import main


DOCS_DIR = Path(__file__).resolve().parents[1] / "docs"


def _bash_blocks(path: Path):
    text = path.read_text()
    return re.findall(r"```bash\n(.*?)```", text, flags=re.DOTALL)


def _commands(block: str):
    normalized = block.replace("\\\n", " ")
    for line in normalized.splitlines():
        line = line.strip()
        if line.startswith("encodefetch "):
            yield shlex.split(line)


def test_documented_encodefetch_commands_parse():
    for path in sorted(DOCS_DIR.glob("*.md")):
        for block in _bash_blocks(path):
            for argv in _commands(block):
                try:
                    with main.make_context("encodefetch", argv[1:]) as ctx:
                        assert ctx.params, f"{path}: failed to parse {' '.join(argv)}"
                except Exit as exc:
                    assert exc.exit_code == 0, f"{path}: failed to parse {' '.join(argv)}"


def test_mkdocs_nav_targets_exist():
    mkdocs = Path(__file__).resolve().parents[1] / "mkdocs.yml"
    nav_targets = re.findall(r": ([a-z0-9_-]+\.md)", mkdocs.read_text())

    missing = [target for target in nav_targets if not (DOCS_DIR / target).exists()]

    assert not missing
