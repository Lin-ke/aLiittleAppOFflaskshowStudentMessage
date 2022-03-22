# -- coding:UTF-8 --
from database import Student
from database import db

# num name age ssex cls depart addr
def ipt():
    b = Student(num = 1902,name = "李四",age = 29,ssex = "男",cls = "b03",depart = "d02",addr = "harbin_Ins")
    db.session.add(b)
    db.session.commit()
    c = Student(num = 1903,name= "王五",age = 29,ssex = "女",cls = "b02",depart = "d03",addr = "harbin_Ins")
    db.session.add(c)
    db.session.commit()
    d = Student(num = 1904,name = "Gouzei",age = 29,ssex = "男",cls = "b04",depart = "d02",addr = "harbin_Ins")
    db.session.add(d)
    db.session.commit()
    e = Student(num = 1901,name = "魏",age = 19,ssex = "男",cls = "b01",depart = "d01",addr = "hrb")
    db.session.add(e)
    db.session.commit()
def show():
    print(Student.query.all())
def changeSth(types,paras):
    str = " * from student where "
    fst = True
    for i in range(len(types)-2):
        if paras[i] != "":
            if(fst == False):
                str+="and "
            else: fst = False
            if types[i] == "age1":
                str+="age>="+paras[i]+" "
            elif types[i] == "age2":
                str+="age<="+paras[i]+" "
            else: str +=types[i]+"="+"\""+paras[i]+"\" "
    if(paras[len(types)-2] == True):
        str = "select"+str
    else : str = "delete"+str
    str = str.strip()
    str+=";"
    print(str)
    return str
if __name__ == "__main__":
     db.create_all()
     ipt()
     show()