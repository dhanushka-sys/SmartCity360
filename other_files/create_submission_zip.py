import os
import zipfile
import shutil

def create_project_zip():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    out_zip_root = os.path.join(root_dir, "SmartCity360_Source_Code.zip")
    out_zip_doc = os.path.join(os.path.dirname(__file__), "SmartCity360_Source_Code.zip")
    out_zip_compat = os.path.join(os.path.dirname(__file__), "SmartCity360_Project_Source_Code.zip")
    
    exclude_dirs = {
        "node_modules",
        ".next",
        ".git",
        "__pycache__",
        "target",
        ".idea",
        ".vscode",
        ".settings",
        ".gradle",
        "bin",
        "scratch"
    }
    
    exclude_files = {
        "SmartCity360_Source_Code.zip",
        "SmartCity360_Project_Source_Code.zip",
        ".DS_Store",
        "thumbs.db"
    }

    count = 0
    with zipfile.ZipFile(out_zip_root, "w", zipfile.ZIP_DEFLATED) as zipf:
        for foldername, subfolders, filenames in os.walk(root_dir):
            subfolders[:] = [d for d in subfolders if d not in exclude_dirs]
            
            for filename in filenames:
                if filename in exclude_files or filename.endswith(".class") or filename.endswith(".pyc"):
                    continue
                
                filepath = os.path.join(foldername, filename)
                relpath = os.path.relpath(filepath, root_dir)
                
                parts = relpath.split(os.sep)
                if any(p in exclude_dirs for p in parts):
                    continue
                
                zipf.write(filepath, relpath)
                count += 1

    # Remove redundant duplicates in other_files to maintain a lean repository
    for dup in [out_zip_doc, out_zip_compat]:
        if os.path.exists(dup):
            try:
                os.remove(dup)
                print(f"Removed redundant zip: {dup}")
            except Exception as e:
                pass

    zip_size_mb = os.path.getsize(out_zip_root) / (1024 * 1024)
    print(f"Successfully packaged {count} clean source files into {out_zip_root} ({zip_size_mb:.2f} MB)")

if __name__ == "__main__":
    create_project_zip()
