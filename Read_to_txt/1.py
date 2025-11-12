# compare_files.py
def extract_paths(file_path):
    paths = []
    with open(file_path, "r") as f:
        for line in f:
            # Extract path part (last column)
            parts = line.strip().split()
            if len(parts) > 0:
                # The last part is the file path
                path = parts[-1]
                # Normalize: replace "ROW_496" with "projects/row496" for matching
                path = path.replace("ROW_496", "projects/row496")
                paths.append(path)
    return set(paths)

def main():
    original = extract_paths("row496_original.txt")
    copy = extract_paths("row496_copy.txt")

    missing = original - copy

    with open("missing_files.txt", "w") as out:
        for path in sorted(missing):
            out.write(path + "\n")

    print(f"✅ Total original files: {len(original)}")
    print(f"✅ Total copied files:   {len(copy)}")
    print(f"❌ Missing files:        {len(missing)}")
    print("📝 Missing file list saved to 'missing_files.txt'")

if __name__ == "__main__":
    main()
