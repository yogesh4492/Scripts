import csv
import typer
from collections import deque
app=typer.Typer()
class Main:
    def __init__(self,group__id,group_size,output_file,input_file):
        self.group_id=group__id
        self.group_size=group_size
        self.output_file=output_file
        self.input_file=input_file
        self.filed=['Script','Id','Group_ID']
    def read_csv(self):
        with open(self.input_file,'r') as cr:
            return list(csv.DictReader(cr))

    def generated_csv(self):
        with open(self.output_file,'w') as cw:
            
            csw=csv.DictWriter(cw,fieldnames=self.filed)
            csw.writeheader()
            for i in range(0,len(self.data),self.group_size):
                if i+self.group_size<len(self.data):
                    
                    for j in range(i,i+self.group_size):
                        row={}
                        row['Script']=self.data[j].get('phrase')
                        row['Id']=self.data[j].get('phraseId')
                        row['Group_ID']=self.group_id
                        csw.writerow(row)
                    self.group_id+=1
                else:
                    self.group_size+=len(self.data)-(i+self.group_size)
                    
                    for j in range(i,i+self.group_size):
                        row={}
                        row['Script']=self.data[j].get('phrase')
                        row['Id']=self.data[j].get('phraseId')
                        row['Group_ID']=self.group_id
                        csw.writerow(row)
                    self.group_id+=1
               
    def run(self):
        self.data=self.read_csv()
        print(len(self.data))
        self.phrases=len(self.data)
        self.generated_csv()
        

@app.command()
def main(input_file=typer.Argument(...,help="path of Input Csv File")
         ,group_id:int=typer.Argument(...,help="Group Id like 100001,200001 only starting"),
         output_file=typer.Argument("Yogesh_Patel.csv",help="Give  name and Path For Output file"),
         group_size:int=typer.Argument(55,help="group size per by default its 55")):
    obj=Main(group_id,group_size,output_file,input_file)
    obj.run()

if __name__=="__main__":
    app()