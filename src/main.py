import pathlib

from parse import generate_pages_recursive
from utils import dir_copy

parent_dir = pathlib.Path(__file__).parent.parent.resolve()
from_path = f"{parent_dir}/content"
to_path = f"{parent_dir}/public"
template_path = f"{parent_dir}/template.html"

dir_copy(f"{parent_dir}/static", f"{parent_dir}/public")
generate_pages_recursive(from_path, to_path, template_path)
