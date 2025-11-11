import csv
import typer
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

app = typer.Typer(help="Find duplicate files (by hash or name) from S3 inventory CSV")

def read_csv(csv_path: Path):
    """Read CSV and return list of rows"""
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        return [row for row in reader if row]

def process_row(row):
    """
    Expected CSV format:
    path, size, md5
    """
    try:
        path, size, md5 = row
        return md5.strip(), path.strip()
    except ValueError:
        return None

@app.command()
def find_duplicates(
    csv_path: Path = typer.Argument(..., help="Path to the CSV file containing path,size,md5"),
    output_csv: Path = typer.Option("duplicates.csv", help="Output CSV file name"),
    threads: int = typer.Option(8, help="Number of threads to use for processing")
):
    """
    Finds duplicate files (by MD5 hash) and writes them into a new CSV file.
    Each line contains all files with the same hash (duplicates).
    """

    typer.echo(f"🔍 Reading file: {csv_path}")
    rows = read_csv(csv_path)

    duplicates = {}

    with ThreadPoolExecutor(max_workers=threads) as executor:
        for result in executor.map(process_row, rows):
            if result:
                md5, path = result
                duplicates.setdefault(md5, []).append(path)

    # Write duplicates to CSV
    with open(output_csv, "w", newline="", encoding="utf-8") as out_csv:
        writer = csv.writer(out_csv)
        writer.writerow(["MD5 Hash", "Duplicate Files"])
        for md5, paths in duplicates.items():
            if len(paths) > 1:
                writer.writerow([md5, " | ".join(paths)])

    typer.echo(f"✅ Duplicate check complete! Output written to: {output_csv}")

if __name__ == "__main__":
    app()
