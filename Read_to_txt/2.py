# compare_files_full_line.py
def extract_paths(file_path):
    """Extract both full line and normalized path for comparison."""
    paths = {}
    with open(file_path, "r") as f:
        for line in f:
            parts = line.strip().split()
            if not parts:
                continue
            path = parts[-1]
            normalized = path.replace("ROW_496", "projects/row496")
            paths[normalized] = line.strip()
    return paths

def main():
    original = extract_paths("row496_original.txt")
    copy = extract_paths("row496_copy.txt")

    # Compare based on normalized paths
    missing = [original[path] for path in original if path not in copy]

    # Save missing lines to file
    with open("missing_full_lines.txt", "w") as out:
        for line in missing:
            out.write(line + "\n")

    print(f"✅ Total original files: {len(original)}")
    print(f"✅ Total copied files:   {len(copy)}")
    print(f"❌ Missing files:        {len(missing)}")
    print("📝 Full details saved to 'missing_full_lines.txt'")

if __name__ == "__main__":
    main()
