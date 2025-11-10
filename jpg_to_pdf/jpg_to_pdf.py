from PIL import Image
import os
import typer
app=typer.Typer()
def jpg_to_pdf(input_folder, output_folder):
    # Get all JPG/JPEG files in the folder
    images = [f for f in os.listdir(input_folder) if f.lower().endswith(('.jpg', '.jpeg'))]
    if not images:
        print("No JPG images found in the folder.")
        return

    # Sort images alphabetically (optional but useful)
    images.sort()
    image_list = []

    for img_name in images:
        img_path = os.path.join(input_folder, img_name)
        img = Image.open(img_path).convert('RGB')
        image_list.append(img)

    # First image + rest appended
    first_image = image_list[0]
    rest = image_list[1:]
    # print(first_image)
    print(images)
    os.makedirs(output_folder,exist_ok=True)
    for i in images:
        pass
    #     output_file=os.path.join(output_folder,f"{os.path.splitext(i)[0]}.pdf")
    #     # print(output_file)
    #     first_image.save(output_file, save_all=True, append_images=rest)
    # print(f"✅ PDF created successfully: {output_pdf}")

# Example usage:
# Change these paths as per your system
@app.command()
def to_pdf(input_folder,output_folder):
    jpg_to_pdf(input_folder,output_folder)

if __name__=="__main__":
    app()


