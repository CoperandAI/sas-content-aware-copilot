import os


# ✅ Function to Generate File Tree
def generate_file_tree(directory):
    """Generate a file structure dictionary for Dash."""
    file_tree = []
    for root, dirs, files in os.walk(directory):
        rel_root = os.path.relpath(root, directory)
        if rel_root == ".":
            rel_root = ""
        node = {
            "label": os.path.basename(root) if rel_root else "APP_DATA",
            "value": rel_root,
            "children": [
                {"label": d, "value": os.path.join(rel_root, d), "children": []} for d in dirs
            ] + [
                {"label": f, "value": os.path.join(rel_root, f)} for f in files
            ]
        }
        file_tree.append(node)
    return file_tree