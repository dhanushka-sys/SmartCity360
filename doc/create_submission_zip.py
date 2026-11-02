import os
import zipfile

def create_project_zip():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    out_zip = os.path.join(os.path.dirname(__file__), "SmartCity360_Project_Source_Code.zip")
    
    # Exclude bloated, temporary, or unneeded directories and files
    exclude_dirs = {
        "node_modules",
        ".next",
        ".git",
        "__pycache__",
        "target",
        ".idea",
        ".vscode",
        ".settings"
    }
    
    exclude_files = {
        "SmartCity360_Project_Source_Code.zip",
        ".DS_Store"
    }

    count = 0
    with zipfile.ZipFile(out_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
        for foldername, subfolders, filenames in os.walk(root_dir):
            # Prune excluded directories
            subfolders[:] = [d for d in subfolders if d not in exclude_dirs]
            
            for filename in filenames:
                if filename in exclude_files or filename.endswith(".class"):
                    continue
                
                filepath = os.path.join(foldername, filename)
                relpath = os.path.relpath(filepath, root_dir)
                
                # Double-check relative path does not start with excluded dir
                parts = relpath.split(os.sep)
                if any(p in exclude_dirs for p in parts):
                    continue
                
                zipf.write(filepath, relpath)
                count += 1

    zip_size_mb = os.path.getsize(out_zip) / (1024 * 1024)
    print(f"Successfully packaged {count} files into {out_zip} ({zip_size_mb:.2f} MB)")

if __name__ == "__main__":
    create_project_zip()

