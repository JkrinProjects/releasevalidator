import sys
from validator.runner import validate_build

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = "candidate"

    errors = validate_build(target)
    
    if errors:
        print("VALIDATION FAILURE")

        for error in errors:
            print(f"ERROR FOUND: {error}")
        sys.exit(1)
    
    print("VALIDATION PASSED")