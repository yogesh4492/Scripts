import typer
import os
from concurrent.futures import ThreadPoolExecutor,as_completed
from rich.progress import Progress


def Extract_Original_file(file_path):
    list=[]
    with open(file_path,'r') as rt:
        for i in rt:
            part=i.strip().split("/",2)
            list.append(part)
    return list
    

def Extract_Copy_file(file_path):
    list=[]
    with open(file_path,'r') as rt:
        for i in rt:
            part=i.strip().split("/",1)
            # print(part[1])
            list.append(part[1])
    return list
                  
app=typer.Typer()

@app.command()
def main(original_file,copy_file,out_txt):
    list3=[]
    read_original=Extract_Original_file(original_file)
    copy_original=Extract_Copy_file(copy_file)
    print("total lines in original file= ",len(read_original))
    print("Total Lines In copy file = ",len(copy_original))
    for i in read_original:
        if i[2] not in copy_original:
            list3.append(i)
            for k in read_original:
                if k[2]==i[2]:
                    stri=" ".join(k)
                    with open(out_txt,'a') as w:
                        w.write(stri+"\n")
                
    print("Total Mismatch Lines = ",len(list3))
    
    

if __name__=="__main__":
    app()

