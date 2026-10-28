#tmp_path is built into pytest

import json
from validator import validate_build

#build temp sample directory 
def create_release(tmp_path):
    (tmp_path / "demo_software.bin").write_text("DEMO BUILD", encoding="utf-8",)

    manifest = {
        "release_name": "Demo Software",
        "version": "1.0.0",
        "required_files": ["demo_software.bin"],
    }

    (tmp_path / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8",)

#positive case
def test_valid_release_passes(tmp_path):
    create_release(tmp_path)

    errors = validate_build(tmp_path)

    assert errors == []


def test_missing_file_fails(tmp_path):
    create_release(tmp_path)
    (tmp_path / "demo_software.bin").unlink()

    errors = validate_build(tmp_path)

    assert "missing a required file: demo_software.bin" in errors

def test_missing_manifest_fails(tmp_path):
    errors = validate_build(tmp_path)

    assert errors == ["Manifest file not found"]