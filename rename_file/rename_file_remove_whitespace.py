import os
import typer
app=typer.Typer()

def remove_whitespace_in_filenames(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            old_path = os.path.join(root, file)

            # Remove all whitespace characters
            new_name = "".join(file.split())
       
            new_path = os.path.join(root, new_name)

            if old_path != new_path:
                print(f"Renaming:\n  {old_path}\n→ {new_path}")
                os.rename(old_path, new_path)

    print("\n✔ All filenames cleaned. Whitespaces removed.")


# Run the function
@app.command()
def main(input_folder:str=typer.Argument(...,help="input folder path that contain filename with whitespace")):
        remove_whitespace_in_filenames(input_folder)



if __name__=="__main__":
    app()

