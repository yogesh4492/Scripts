import boto3
import hashlib
import pandas as pd
from urllib.parse import urlparse
import tempfile
from tqdm import tqdm
import typer
from concurrent.futures import ThreadPoolExecutor, as_completed

app = typer.Typer(help="Check duplicate files (by name and content) in an S3 path using parallel hashing.")


def get_s3_files(bucket_name: str, prefix: str):
    """List all files from the given S3 path."""
    s3 = boto3.client('s3')
    paginator = s3.get_paginator('list_objects_v2')
    file_list = []

    for page in paginator.paginate(Bucket=bucket_name, Prefix=prefix):
        for obj in page.get('Contents', []):
            if not obj['Key'].endswith('/'):  # skip folder entries
                file_list.append({
                    'Key': obj['Key'],
                    'Size': obj['Size']
                })
    return file_list


def compute_md5(bucket: str, key: str, s3_client, chunk_size: int = 8 * 1024 * 1024):
    """Download S3 file temporarily and compute true MD5 hash."""
    md5 = hashlib.md5()
    with tempfile.NamedTemporaryFile(delete=True) as tmp_file:
        s3_client.download_file(bucket, key, tmp_file.name)
        with open(tmp_file.name, 'rb') as f:
            for chunk in iter(lambda: f.read(chunk_size), b""):
                md5.update(chunk)
    return md5.hexdigest()


def parallel_hash(bucket: str, file_list, max_workers: int = 8):
    """Compute hashes in parallel using ThreadPoolExecutor."""
    s3 = boto3.client('s3')
    results = [None] * len(file_list)

    typer.echo(f"\n🚀 Starting parallel hashing with {max_workers} threads for {len(file_list)} files...\n")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_index = {
            executor.submit(compute_md5, bucket, file_list[i]['Key'], s3): i
            for i in range(len(file_list))
        }

        for future in tqdm(as_completed(future_to_index), total=len(file_list), desc="Hashing files", unit="file"):
            i = future_to_index[future]
            try:
                results[i] = future.result()
            except Exception as e:
                typer.echo(f"⚠️ Error hashing {file_list[i]['Key']}: {e}")
                results[i] = None

    return results


def create_duplicate_rows(df: pd.DataFrame, group_by_col: str):
    """Create rows showing original file and all its duplicates in same row."""
    duplicate_mask = df.duplicated(group_by_col, keep=False) & df[group_by_col].notna()
    dupes = df[duplicate_mask].copy()
    
    if dupes.empty:
        return pd.DataFrame()
    
    # Group by the duplicate key
    grouped = dupes.groupby(group_by_col)
    
    result_rows = []
    for name, group in grouped:
        # Sort by Key to have consistent ordering
        group = group.sort_values('Key').reset_index(drop=True)
        
        # First file is the "original"
        row = {
            'Original_File': group.loc[0, 'Key'],
            'Original_Size': group.loc[0, 'Size'],
            'MD5': group.loc[0, 'MD5'],
            'Total_Duplicates': len(group) - 1
        }
        
        # Add all duplicate files
        for i in range(1, len(group)):
            row[f'Duplicate_{i}_File'] = group.loc[i, 'Key']
            row[f'Duplicate_{i}_Size'] = group.loc[i, 'Size']
        
        result_rows.append(row)
    
    return pd.DataFrame(result_rows)


def save_to_csv(name_dupes, content_dupes, output_file: str):
    """Save duplicate results to separate CSV files."""
    base_name = output_file.replace('.xlsx', '').replace('.csv', '')
    name_file = f"{base_name}_name_duplicates.csv"
    content_file = f"{base_name}_content_duplicates.csv"

    if not name_dupes.empty:
        name_dupes.to_csv(name_file, index=False)
        typer.echo(f"   📄 Name duplicates: {name_file} ({len(name_dupes)} groups)")
    
    if not content_dupes.empty:
        content_dupes.to_csv(content_file, index=False)
        typer.echo(f"   📄 Content duplicates: {content_file} ({len(content_dupes)} groups)")

    typer.echo(f"\n✅ Duplicate reports saved!")


def parse_s3_path(s3_path: str):
    """Split s3://bucket/prefix into bucket and prefix."""
    parsed = urlparse(s3_path)
    return parsed.netloc, parsed.path.lstrip('/')


@app.command()
def check(
    s3path: str = typer.Argument(..., help="S3 path, e.g., s3://my-bucket/folder/"),
    output: str = typer.Option("s3_duplicates.csv", "--output", "-o", help="Base name for output CSV files"),
    threads: int = typer.Option(8, "--threads", "-t", help="Number of threads for parallel hashing"),
):
    """Check for duplicate file names and content (true MD5) in an S3 path."""
    bucket, prefix = parse_s3_path(s3path)
    typer.echo(f"\n📂 Scanning bucket: {bucket}, prefix: {prefix}\n")

    files = get_s3_files(bucket, prefix)
    if not files:
        typer.echo("❌ No files found in given S3 path.")
        raise typer.Exit()

    # Compute hashes in parallel
    md5_hashes = parallel_hash(bucket, files, threads)

    # Combine results
    df = pd.DataFrame(files)
    df['MD5'] = md5_hashes

    # Create duplicate rows (original + duplicates in same row)
    name_dupes = create_duplicate_rows(df, 'Key')
    content_dupes = create_duplicate_rows(df, 'MD5')

    if name_dupes.empty and content_dupes.empty:
        typer.echo("\n✅ No duplicates found!")
    else:
        typer.echo(f"\n📊 Found duplicates:")
        if not name_dupes.empty:
            total_name_dupes = name_dupes['Total_Duplicates'].sum()
            typer.echo(f"   🔤 Name duplicates: {len(name_dupes)} original files with {int(total_name_dupes)} duplicates")
        if not content_dupes.empty:
            total_content_dupes = content_dupes['Total_Duplicates'].sum()
            typer.echo(f"   🔐 Content duplicates: {len(content_dupes)} original files with {int(total_content_dupes)} duplicates")
        save_to_csv(name_dupes, content_dupes, output)


if __name__ == "__main__":
    app()