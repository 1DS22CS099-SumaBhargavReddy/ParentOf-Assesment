import os
import zipfile

ZIP_NAME = "K_Bhargav_Reddy_Assessment.zip"
EXCLUDE_DIRS = {"__pycache__", ".pytest_cache", ".venv", "venv", ".git"}
EXCLUDE_FILES = {ZIP_NAME, "pack_submission.py"}


def create_zip():
    # We want to place the zip on the Desktop (parent of the workspace directory)
    workspace_dir = os.path.abspath(os.path.dirname(__file__))
    parent_dir = os.path.dirname(workspace_dir)
    zip_path = os.path.join(parent_dir, ZIP_NAME)

    print(f"Creating submission archive at: {zip_path}")

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(workspace_dir):
            # Modify dirs in-place to avoid traversing excluded directories
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

            for file in files:
                if file in EXCLUDE_FILES:
                    continue

                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, workspace_dir)
                zipf.write(full_path, rel_path)
                print(f"  + Added: {rel_path}")

    print(f"\n[SUCCESS] Archive '{ZIP_NAME}' created successfully on the Desktop!")


if __name__ == "__main__":
    create_zip()
