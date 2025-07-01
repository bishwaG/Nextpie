import os
import json

class uploadStats:
    @staticmethod
    def get_folder_size(path):
        total = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                try:
                    fp = os.path.join(dirpath, f)
                    if not os.path.islink(fp):
                        total += os.path.getsize(fp)
                except OSError:
                    pass
        return total

    @staticmethod
    def count_subfolders(path):
        try:
            return sum(1 for entry in os.scandir(path) if entry.is_dir())
        except FileNotFoundError:
            return 0

    @staticmethod
    def build_tree_with_counts(root_path):
        warnings = []
        
        if not os.path.exists(root_path):
            return {
                "error": True,
                "message": f"The folder '{root_path}' does not exist. It will be created automatically after uploading a trace file via the API or the GUI",
                "warnings": warnings
            }
        
        # Check required subfolders
        required_subfolders = ['API', 'GUI']
        missing_subfolders = []
        for sub in required_subfolders:
            if not os.path.exists(os.path.join(root_path, sub)):
                missing_subfolders.append(sub)

        if missing_subfolders:
            warnings.append(f"Missing subfolders: {', '.join(missing_subfolders)}")
        
        root_size_mb = round(uploadStats.get_folder_size(root_path) / (1024 * 1024), 2)
        
        children = []
        try:
            for entry in os.scandir(root_path):
                if entry.is_dir() and entry.name in required_subfolders:
                    folder_path = entry.path
                    folder_size_kb = round(uploadStats.get_folder_size(folder_path) / 1024, 2)
                    subfolder_count = uploadStats.count_subfolders(folder_path)
                    children.append({
                        "name": entry.name,
                        "size_kb": folder_size_kb,
                        "num_subfolders": subfolder_count
                    })
        except PermissionError:
            warnings.append("Permission denied reading some folders.")
        
        result = {
            "name": os.path.basename(root_path),
            "size_mb": root_size_mb,
            "children": children,
            "warnings": warnings,
            "error": False
        }
        return result


