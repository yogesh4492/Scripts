import typer
import os
from concurrent.futures import ThreadPoolExecutor,as_completed
from rich.progress import Progress


def Extract_Original_file(file_path):
    list=[]
    with open(file_path,'r') as rt:
        for i in rt:
            part=i.strip().split("/",2)
            list.append(part[2])
    return list
    
def Extract_Copy_file(file_path):
    files = []
    with open(file_path, 'r') as rt:
        for line in rt:
            path = line.strip().replace("\\", "/")   # Convert Windows path → Linux style
            parts = path.split("/", 1)               # Split only once
            if len(parts) > 1:
                files.append(parts[1])               # Take everything after drive letter
            else:
                files.append(parts[0])
    return files
# def Extract_Copy_file(file_path):
#     list=[]
#     with open(file_path,'r') as rt:
#         for i in rt:
#             part=i.strip().split("/",1)
#             # print(part[1])
#             list.append(part[1])
#     return list      
app=typer.Typer()

@app.command()
def main(original_file,copy_file,out_txt="nov14.txt"):
    list3=[]
    read_original=Extract_Original_file(original_file)
    copy_original=Extract_Copy_file(copy_file)
    print("total lines in original file= ",len(read_original))
    print("Total Lines In copy file = ",len(copy_original))
    for i in read_original:
        if i not in copy_original:
            list3.append(i)
    print("Total Mismatch Lines = ",len(list3))
    with open(out_txt,'w') as w:
        for i in list3:
            w.write(i+"\n")

if __name__=="__main__":
    app()

