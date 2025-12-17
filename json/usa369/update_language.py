import json
from pathlib import Path
import typer

app = typer.Typer(help="Replace en_us_usa_263 with en_us in JSON files")


OLD_VALUE = "en_US_USA263"
NEW_VALUE = "en_US"


def replace_recursive(obj):
    """
    Recursively replace string values in JSON (keys and values)
    """
    if isinstance(obj, dict):
        new_dict = {}
        for k, v in obj.items():
            new_key = k.replace(OLD_VALUE, NEW_VALUE) if isinstance(k, str) else k
            new_dict[new_key] = replace_recursive(v)
        return new_dict

    elif isinstance(obj, list):
        return [replace_recursive(item) for item in obj]

    elif isinstance(obj, str):
        return obj.replace(OLD_VALUE, NEW_VALUE)

    else:
        return obj


@app.command()
def process(
    input_dir: Path = typer.Argument(..., exists=True, file_okay=False, help="Input JSON directory"),
    output_dir: Path = typer.Argument(..., help="Output directory for updated JSON files"),
):
    """
    Process all JSON files and replace locale value
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    json_files = list(input_dir.rglob("*.json"))

    if not json_files:
        typer.echo("No JSON files found")
        raise typer.Exit(1)

    for json_file in json_files:
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            updated_data = replace_recursive(data)

            relative_path = json_file.relative_to(input_dir)
            output_file = output_dir / relative_path
            output_file.parent.mkdir(parents=True, exist_ok=True)

            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(updated_data, f, indent=2, ensure_ascii=False)

            typer.echo(f"Updated: {relative_path}")

        except Exception as e:
            typer.echo(f"Failed: {json_file} → {e}")


if __name__ == "__main__":
    app()
