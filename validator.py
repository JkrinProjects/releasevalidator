import json
import re
import sys
from pathlib import Path

def validate_build(release_directory):
    release_directory = Path(release_directory)
    errors = []
    manifest_path = release_directory/"manifest.json"

    #does it exist
    if not manifest_path.is_file():
        return ["Manifest file not found"]

    #is a json file
    try:
        manifest_file = json.loads(manifest_path.read_text(encoding="utf-8"))
    
    except(json.JSONDecodeError, UnicodeDecodeError):
        return ["Manifest is not proper or valid JSON"]

    #check for the full list of required files 
    required_files = manifest_file.get("required_files")

    #check the requested files exist and are properly formatted
    if not isinstance(required_files, list):
        errors.append("required files are not a list")
        required_files = []

    for filename in required_files:
        if(not isinstance(filename, str)):
            errors.append("Filename must be a string")
            continue
        
        if filename == "":
            errors.append("Filename can't be empty")
            continue

        if (Path(filename).name != filename):
            errors.append(f"Filename can't have a directory: {filename}")
            continue

        if (filename == ".."):
            errors.append(f"Invalid filename: {filename}")
            continue

        filepath = release_directory/filename
        if not filepath.is_file():
            errors.append(f"missing a required file: {filename}")

    return errors


if __name__ == "__main__":
    if (len(sys.argv) > 1):
        filename = sys.argv[1]
    else:
        target = "candidate"

errors = validate_build(target)
if errors:
    print("VALIDATION FAILURE")

    for error in errors:
        print(f"ERROR FOUND: {error}")
    sys.exit(1)
    
print("VALIDATION PASSED")