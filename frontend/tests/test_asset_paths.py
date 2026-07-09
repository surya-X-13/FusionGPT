from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from frontend.utils.api import get_asset_path, get_logo_path


def test_get_asset_path_finds_existing_logo():
    resolved = Path(get_asset_path("assets/logo.png"))

    assert resolved.exists()
    assert resolved.name == "logo.png"


def test_get_logo_path_uses_images_folder_logo():
    resolved = Path(get_logo_path())

    assert resolved.exists()
    assert resolved.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".svg"}
