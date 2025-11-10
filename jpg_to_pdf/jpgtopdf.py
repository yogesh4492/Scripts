from PIL import Image
import os
import typer

app = typer.Typer()

def jpg_to_pdf(input_folder: str, output_folder: str):
    # Get all JPG/JPEG files in the folder
    images = [f for f in os.listdir(input_folder) if f.lower().endswith(('.jpg', '.jpeg'))]
    if not images:
        print("No JPG images found in the folder.")
        return

    # Sort images alphabetically
    images.sort()
    os.makedirs(output_folder, exist_ok=True)

    for img_name in images:
        img_path = os.path.join(input_folder, img_name)
        output_file = os.path.join(output_folder, f"{os.path.splitext(img_name)[0]}.pdf")

        try:
            img = Image.open(img_path).convert("RGB")
            img.save(output_file)
            print(f"✅ Saved: {output_file}")
        except Exception as e:
            print(f"❌ Failed to convert {img_name}: {e}")

@app.command()
def to_pdf(input_folder: str, output_folder: str):
    """
    Convert all JPG/JPEG images from input_folder to same-name PDFs in output_folder.
    """
    jpg_to_pdf(input_folder, output_folder)

if __name__ == "__main__":
    app()
