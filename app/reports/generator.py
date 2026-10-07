from pathlib import Path
from jinja2 import Environment, FileSystemLoader

from app.models.scan import ScanResponse

TEMPLATE_DIR = Path(__file__).parent / "templates"
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR), autoescape=True)


def render_html(report: ScanResponse) -> str:
    template = env.get_template("report.html")
    return template.render(report=report)