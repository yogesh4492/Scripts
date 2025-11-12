
import os
import typer
app=typer.Typer()
def list_all_files_recursive(directory_path):
    """Lists the full paths of all files in the directory and all subdirectories."""
    all_files = []
    for dirpath, dirnames, filenames in os.walk(directory_path):
        for filename in filenames:
            # Construct the full file path
            full_path = os.path.join(dirpath, filename)
            all_files.append(full_path)
    return all_files

# Example usage for the current directory and all its subfolders:
@app.command()
def main(input_dir:str=typer.Argument(...,help="Input Directory path or name ")):
    all_files_list = list_all_files_recursive(input_dir)
    print(len(all_files_list))
    
    
if __name__=="__main__":
    app()

