import json
import re
import os
import typer
from rich.progress import Progress

app = typer.Typer(help="Replace 'en_US_VNM' or 'en-usa-vnm' to 'en_US' or 'en-usa' in all JSON files of a directory.")

def replace_language_codes(obj):
    """Recursively replace 'en_US_VNM' or 'en-usa-vnm' with 'en_US' or 'en-usa'."""
    if isinstance(obj, dict):
        return {k: replace_language_codes(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [replace_language_codes(i) for i in obj]
    elif isinstance(obj, str):
        obj = re.sub(r'en[_-]usa[_-]vnm', 'en-usa', obj, flags=re.IGNORECASE)
        obj = re.sub(r'en[_-]us[_-]vnm', 'en_US', obj, flags=re.IGNORECASE)
        return obj
    else:
        return obj

@app.command()
def process(
    input_dir: str = typer.Argument(..., help="Path to directory containing JSON files."),
    output_dir: str = typer.Argument(..., help="Path to directory to save modified JSON files.")
):
    """Process all JSON files in input_dir and save updated copies to output_dir."""
    os.makedirs(output_dir, exist_ok=True)
    
    files = [f for f in os.listdir(input_dir) if f.lower().endswith(".json")]
    if not files:
        typer.echo("❌No JSON files found in the input directory.")
        raise typer.Exit()

    with Progress() as progress:
        task = progress.add_task("Processing JSON files...", total=len(files))
        for file_name in files:
            in_path = os.path.join(input_dir, file_name)
            out_path = os.path.join(output_dir, file_name)

            try:
                with open(in_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                updated_data = replace_language_codes(data)

                with open(out_path, "w", encoding="utf-8") as f:
                    json.dump(updated_data, f, indent=4, ensure_ascii=False)
            except Exception as e:
                typer.echo(f"⚠️ Error processing {file_name}: {e}")

            progress.advance(task)

    typer.echo(f"✅ All files processed. Updated files saved in: {output_dir}")

if __name__ == "__main__":
    app()
