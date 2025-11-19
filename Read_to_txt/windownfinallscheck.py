
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
            path = line.strip().replace("\\", "/")   
            parts = path.split("/", 2)               
            if len(parts) > 1:
                files.append(parts[2])              
            else:
                files.append(parts[1])
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
def main(original_file,copy_file,out_txt,ex_txt):
    list3=[]

    read_original=Extract_Original_file(original_file)
    copy_original=Extract_Copy_file(copy_file)
    print("total lines in original file= ",len(read_original))
    print("Total Lines In copy file = ",len(copy_original))
    set1=set(read_original)
    set2=set(copy_original)
    set3=set1-set2
    list3=list(set3)
    set4=set2-set1
    list4=list(set4)

    # for i in read_original:
    #     if i not in copy_original:
    #         list3.append(i)
    print("Total Extra Lines = ",len(list4))
    print("Total Mismatch Lines = ",len(list3))
    with open(out_txt,'w') as w:
        for i in list3:
            w.write(i+"\n")
    with open(ex_txt,'w') as we:
        for i in list4:
            we.write(i+"\n")

if __name__=="__main__":
    app()