#tmp_path is built into pytest

import json
from validator.runner import validate_build
import pytest

#build temp sample directory 
def create_release(tmp_path):
    (tmp_path / "demo_software.bin").write_text("DEMO BUILD", encoding="utf-8",)

    manifest = {
        "release_name": "Demo Software",
        "version": "1.0.0",
        "required_files": ["demo_software.bin"],
    }

    (tmp_path / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

#positive case - valid release
def test_valid_release_passes(tmp_path):
    create_release(tmp_path)

    errors = validate_build(tmp_path)

    assert errors == []

#-------negative cases
def test_missing_file_fails(tmp_path):
    create_release(tmp_path)
    (tmp_path / "demo_software.bin").unlink() #delete a file from a starting point of a known working build

    errors = validate_build(tmp_path)

    assert errors == ["missing a required file: demo_software.bin"] 

def test_missing_manifest_fails(tmp_path):
    errors = validate_build(tmp_path)
    assert errors == ["Manifest file not found"]

#invalid Json is caught and fails
def test_invalid_json_syntax_fails(tmp_path):
    create_release(tmp_path)
    
    manifest = '{"required files": [ }'
    (tmp_path / "manifest.json").write_text(manifest, encoding="utf-8")

    errors = validate_build(tmp_path)
    assert errors == ["Manifest is not proper JSON"]

#test that the value of "required_files" is a list object
@pytest.mark.parametrize("required_files_value",
    [
        "demo_software.bin",
        123,
        None,
        {"filenames":"demo_software.bin"}
    ]
)
def test_required_files_are_not_a_list_object_fails(tmp_path, required_files_value):
    create_release(tmp_path)
    manifest = {"required_files":required_files_value}
    (tmp_path / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    
    errors = validate_build(tmp_path)
    assert errors == ["required files are not a list"]

#required files must contain at least one item 
def test_empty_required_files_list_fails(tmp_path):
    create_release(tmp_path)
    manifest = {
        "release_name": "Demo Software",
        "version": "1.0.0",
        "required_files": []
    }
    (tmp_path / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

    errors = validate_build(tmp_path)
    assert errors == ["required files cannot be empty"]

#test json object is returned
@pytest.mark.parametrize("manifest", 
    [
        ["demo_software.bin"],
        "demo_software.bin",
        12345678
    ]
)
def test_manifest_returned_wrong_type_fails(tmp_path, manifest):
    create_release(tmp_path)
    (tmp_path / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    
    errors = validate_build(tmp_path)
    assert errors == ["Manifest must contain a JSON object"]

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

    assert errors == ["Filename can't have a directory: dir/demo_software.bin"]

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

    assert errors == ["Invalid filename: .."]

#test filenames in the require_files value list are strings
@pytest.mark.parametrize("filename", 
    [
        123,
        None,
        {"name": "demo_software.bin"}
    ]
)
def test_filename_not_string_fails(tmp_path, filename):
    create_release(tmp_path)

    manifest = {
        "release_name": "Demo Software",
        "version": "1.0.0",
        "required_files": [filename]
    }
    
    (tmp_path / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    errors = validate_build(tmp_path)

    assert errors == ["Filename must be a string"]

def test_empty_filename_fails(tmp_path):
    create_release(tmp_path)

    manifest = {
        "release_name": "Demo Software",
        "version": "1.0.0",
        "required_files": [""]
    }

    (tmp_path / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

    errors = validate_build(tmp_path)
    assert errors == ["Filename can't be empty"]





'''    # array object
def test_manifest_returned_array_fails(tmp_path):
    create_release(tmp_path)

    manifest = ["demo_software.bin"]
    (tmp_path / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    
    errors = validate_build(tmp_path)

    assert errors == ["Manifest must contain a JSON object"]

    #string
def test_manifest_returned_string_fails(tmp_path):
    create_release(tmp_path)

    manifest = "demo_software.bin"
    (tmp_path / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    
    errors = validate_build(tmp_path)

    assert errors == ["Manifest must contain a JSON object"]

    #number
def test_manifest_returned_integer_fails(tmp_path):
    create_release(tmp_path)

    manifest = 12345678
    (tmp_path / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    
    errors = validate_build(tmp_path)

    assert errors == ["Manifest must contain a JSON object"]'''