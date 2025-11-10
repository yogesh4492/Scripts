import os

def rename_wav_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith("_left.wav"):
            new_name = filename.replace("_left.wav", "_in.wav")
        elif filename.endswith("_right.wav"):
            new_name = filename.replace("_right.wav", "_out.wav")
        else:
            continue

        old_path = os.path.join(directory, filename)
        new_path = os.path.join(directory, new_name)

        os.rename(old_path, new_path)
        print(f"Renamed: {filename} → {new_name}")

if __name__ == "__main__":
    directory = input("Enter directory path: ").strip()
    rename_wav_files(directory)

