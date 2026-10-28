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

    (tmp_path / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

#positive case
def test_valid_release_passes(tmp_path):
    create_release(tmp_path)

    errors = validate_build(tmp_path)

    assert errors == []

###-------#negative cases

def test_missing_file_fails(tmp_path):
    create_release(tmp_path)
    (tmp_path / "demo_software.bin").unlink() #delete a file from a starting point of a known working build

    errors = validate_build(tmp_path)

    assert "missing a required file: demo_software.bin" in errors

def test_missing_manifest_fails(tmp_path):
    errors = validate_build(tmp_path)

    assert errors == ["Manifest file not found"]

#filename has a directory
def test_filename_with_directory_fails(tmp_path):
    create_release(tmp_path)
    
    manifest = {
        "release_name": "Demo Software",
        "version": "1.0.0",
        "required_files": ["dir/demo_software.bin"],
    }

    (tmp_path / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    
    errors = validate_build(tmp_path)

    assert "Filename can't have a directory: dir/demo_software.bin" in errors

# filename is the hidden "file" '..'
def test_parent_directory_filename_fails(tmp_path):
    create_release(tmp_path)
    
    manifest = {
        "release_name": "Demo Software",
        "version": "1.0.0",
        "required_files": [".."],
    }

    (tmp_path / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    
    errors = validate_build(tmp_path)

    assert "Invalid filename: .." in errors