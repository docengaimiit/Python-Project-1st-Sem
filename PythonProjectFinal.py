import pandas as pd
import matplotlib.pyplot as plt
import csv
students=pd.read_csv('students2022.csv')
students=students.astype(str)
batches=pd.read_csv('batches.csv')
course=pd.read_csv('course.csv')
department=pd.read_csv('Department.csv')
def mainFunc():
    print("Choose the module")
    print("1.Student")
    print("2.Course")
    print("3.Batch")
    print("4.Department")
    print("5.Examinations")
    print("0.To Exit")
    select=int(input())
    if select==1:
        studfunc()
    elif select==2:
        CourseFunc()
    elif select==3:
        BatchFunc()
    elif select==4:
        DepartFunc()
    elif select==5:
        ExaminationsFunc()
    elif select==0:
        return None
    mainFunc()    
def studfunc():
    print("These are the possible functions of the student module :")
    print("1. Display the Student Database")
    print("2. Add a new student ")
    print("3. Delete a student id")
    print("4. Update/Edit database")
    print("5. Generate Report Card")      
    choose=int(input("Enter the number of the function you want to perform :"))
    if choose==1:
        display_Data(students)
    elif choose==2:
        createStudent()
    elif choose==3:
        deleteStud()
    elif choose==4:
        updateDatabase()
    elif choose==5:
         createReport() 
def autoupdatestuID():
    for rows in students.index:
        students.loc[rows,'STUDENT_ID']=students.loc[rows,'BATCH_ID']+str(students.loc[rows,'CLASS_ROLL_NO.']).zfill(2)

def updateBatch_Roll(val,nvalue):
    bat=''
    roll=''
    count=0
    students.loc[val,'STUDENT_ID']=nvalue
    for j in students['STUDENT_ID'][val]:
        if j.isdigit():
            count+=1
        if count<=2:
            bat+=j
        else:
            roll+=j
    students.loc[val,'BATCH_ID']=bat
    students.loc[val,'CLASS_ROLL_NO.']=roll

def chkStuId():
    autoupdatestuID()
    return students.duplicated(subset=['STUDENT_ID']).any()
    
def createStudent():
    list1=['Student ID','Student Name','BATCH_ID','Roll no']
    data = {1:[],2:[],3:[],4:[]}
    for i in range(1,5):
        var=input(f"Enter the {list1[i-1]} : ")
        var=var.upper()
        data[i]=var
    list2=[data]    
    df=pd.DataFrame(list2)
    df.to_csv('students2022.csv',mode='a+',index=False,header=False)
    students=pd.read_csv('students2022.csv')
    autoupdatestuID()

    if(students.duplicated(subset=['STUDENT_ID']).any()):
        print("\nSTUDENT WITH SAME STUDENT_ID ALREADY EXISTS\n")
        display_Data(students[students.duplicated(subset=['STUDENT_ID'],keep='last')])
        students.drop_duplicates(subset=['STUDENT_ID'],keep='first',inplace=True)
        students.to_csv('students2022.csv',index=False)
    else:
        display_Data(students)
       
    

def deleteStud():
    try:
        global students
        print('\n')
        display_Data(students)
        print("\n")
        val=int(input("Enter the index of data you want to delete : "))
        students.drop(val,axis=0,inplace=True)
        students=students.reset_index(drop=True)
        students.to_csv('students2022.csv',index=False)
        print('\n')
        display_Data(students)
    except:
        print("Invalid index entered")
    
def display_Data(s):
    from IPython.display import display
    display(s)
        
def chkduplicate(value,choice):
    count=0
    for rows in students.index:
        if students.iloc[rows,choice-1]==value:
            count+=1
    if count>1:
        return True
    else:
        return False
        
def updateDatabase():
    try:
        print("\n")
        for i in range(4):
            print(f"For updating {students.columns[i]} enter '{i+1}' " )
        choice=int(input())
        clmn=students.columns[choice-1]
        display_Data(students)
        value=input(f"\nEnter {clmn} you want to change :")
        value=value.upper()
        nvalue=input(f"Enter the new {clmn} :")
        nvalue=nvalue.upper()
        #Searching the cell and checking for duplicates and updating the cell.
        for rows in students.index:
            if students.iloc[rows,choice-1]==value:
                val=rows
                if(chkduplicate(value,choice)):
                    temp=students.columns[choice-1]
                    print(f"\n\nThere are multiple {students.columns[choice-1]} in the database having value {value}\n")
                    display_Data(students.loc[students[temp]==value])
                    newvalue=int(input("Enter the index of the data you want to change :"))
                    students.iloc[newvalue,choice-1]=nvalue
                    break
                else:
                    students.iloc[rows,choice-1]=nvalue
                    break
            elif rows==len(students.index)-1:
                print("\n Data not found")
                return updateDatabase()
        #checking if same student id exists
        if(chkStuId() & choice!=1):
            print("\n Student with same Student Id already exists.\n")
            #print(students[students.duplicated(subset=['STUDENT_ID'],keep='last')])
            return None
        if(choice==1):
            if(students.duplicated(subset=['STUDENT_ID']).any()):
                print("\n Student with same Student Id already exists.\n")
                return None
            updateBatch_Roll(val,nvalue)
        else:
            autoupdatestuID()
        students.to_csv('students2022.csv',index=False)
        display_Data(students)
    except:
        print("Invalid choice")
def createReport():    
    course=pd.read_csv('Course.csv')
    students=pd.read_csv('students2022.csv')
    display_Data(students)
    studid=input("Enter the StudentId of students whose report card you want to generate : ")
    studid=studid.upper()
    score=0
    count=0
    grade=''
    pass_status=''
    for name in students.index:
        if students.loc[name,'STUDENT_ID']==studid:
            import csv
            studname=students.loc[name,'STUDENT_NAME']
            studroll=students.loc[name,'CLASS_ROLL_NO.']
            with open(f"{studname}_{studid}.txt",mode='w+') as file1:
                file1.write(f"STUDENT NAME : {studname}\n")
                file1.write(f"STUDENT_ID : {studid}\n")
                file1.write(f"STUDENT ROLL NO. : {studroll}\n\n")
                for i in course.index:
                    couid=course.loc[i,'COURSEID']
                    a=(course.iloc[i,2]).split(",")
                    for j in a:
                        k=j.split(":")
                        if k[0]==studid:
                            score+=int(k[1])
                            count+=1
                            if int(k[1])>=90:
                                grade='A'
                            elif int(k[1])>=80 and int(k[1])<90:
                                grade='B'
                            elif int(k[1])>=70 and int(k[1])<80:
                                grade='C'
                            elif int(k[1])>=60 and int(k[1])<70:
                                grade='D'
                            elif int(k[1])>=50 and int(k[1])<60:
                                grade='E'   
                            elif int(k[1])<50:
                                grade='F'    
                            file1.write(f"MARKS IN {course.loc[i,'COURSE_NAME']} : {k[1]}   GRADE: {grade}\n")
                            break
                avg=score/count
                if avg<40:
                    pass_status='Failed'
                else :
                    pass_status='Passed'    
                file1.write(f"\n\nTotal Average Score is : {round(avg)}\nTHE STUDENT HAS {pass_status}")
            break
def CourseFunc():
    print("These are the possible functions of the Course module :")
    print("1. Create new Course")
    print("2. View performane of all students in the course")
    print("3. Show course statistics")     
    choose=int(input("Enter the number of the function you want to perform :"))
    if choose==1:
        createCourse() 
    elif choose==2:
        view_Course_Perf()
    elif choose==3:
        course_graph()

def createCourse():
    dict1={}
    list1=['COURSEID','COURSE_NAME']
    data = {1:[],2:[],3:{}}
    for i in range(1,3):
        var=input(f"Enter the {list1[i-1]} : ")
        var=var.upper()
        data[i]=var
    n=int(input("Enter the no.of Students enrolled in the course"))    
    for i in range(n):
        k=input("Enter the student ID :")
        v=int(input("Enter the marks"))
        dict1.update({k:v})
    to_remov = {"{":"","}":"","'":"","'":""," ":""}
    string=str(dict1)
    for char in to_remov.keys():
        string = string.replace(char, to_remov[char])
    data[3]=string
    list2=[data]    
    df=pd.DataFrame(list2)
    df.to_csv('Course.csv',mode='a+',index=False,header=False)
    course=pd.read_csv('Course.csv')

def view_Course_Perf():
    course=pd.read_csv('Course.csv')
    perf=pd.DataFrame(index=students.loc[:,'STUDENT_ID'],columns=course.COURSEID)
    for i in course.index:
        couid=course.loc[i,'COURSEID']
        a=(course.iloc[i,2]).split(",")
        for j in a:
            k=j.split(":")
            #print(k)
            perf.loc[k[0],couid]=int(k[1])
            
    print("If you want to see performance of all courses enter 1 ")
    print("If you want to see performance for a particular course enter 2")
    choice=int(input())
    #print(perf)

    df2=perf.mean(axis='index')
    df2.columns='Mean'
    data={"Mean":df2}
    dframe=pd.DataFrame(data)
    #perf[perf.isnull()]="-"
    df1=pd.merge(perf.T,dframe,left_index=True,right_index=True)
    df1=df1.T
    if choice==1:
        df1[df1.isnull()]="-"
        df3=pd.merge(students,df1,left_on='STUDENT_ID',right_on=df1.index,how='outer')
        display_Data(df3.drop(columns=['BATCH_ID']))
    elif choice==2:
        val=input("Enter the course Id of the course whose performance you want to see : ")
        val=[val.upper()]
        df1[df1.isnull()]="-"
        df3=pd.merge(students,df1,left_on='STUDENT_ID',right_on=df1.index,how='outer')
        res=[i for i in course.COURSEID if i not in val]
        display_Data(df3.drop(columns=res))
def course_graph():    
    import matplotlib.pyplot as plt
    course=pd.read_csv('Course.csv')
    couid=input("Enter the Course ID whose stats you want to see :")
    couid=couid.upper()
    perf=pd.DataFrame(index=students.loc[:,'STUDENT_ID'],columns=course.COURSEID)
    
    for i in course.index:
        if couid==course.loc[i,'COURSEID']:
            a=(course.iloc[i,2]).split(",")
            for j in a:
                k=j.split(":")
                if int(k[1])<40:
                    k[1]=40
                perf.loc[k[0],couid]=int(k[1])
            break
    a=perf.loc[:,couid].dropna().to_numpy()
    graph, (plot1) = plt.subplots(1)
    labels = ['A', 'B', 'C', 'D', 'E', 'F']
    plot1.hist(a,bins=[40,50,60,70,80,90,100],ec='black',align='right')
    plt.xlabel('Grades')
    plt.ylabel('No. of Students')
    plt.title(f"Performance of students of Course {couid}")
    plt.xticks([100,90,80,70,60,50,40],labels)
    plot1.invert_xaxis()
    plt.show()

def BatchFunc():
    print("These are the possible functions of the Batch module :")
    print("1. Create new Batch")
    print("2. View list of all students in a batch")
    print("3. View list of all courses taught in the batch") 
    print("4. View complete performance of all students in a batch")
    print("5. Pie Chart of Percentage of all students")
    choose=int(input("Enter the number of the function you want to perform :"))
    if choose==1:
        createBatch() 
    elif choose==2:
        studInBatch()
    elif choose==3:
        courseInBatch()
    elif choose==4:
        BatchPerf()
    elif choose==5:
        batch_Graph()      
          
def createBatch():
    #display_Data(batches)
    list1=['BATCH_ID','Batch Name','Department','List of Course']
    data = {1:[],2:[],3:[],4:[]}
    print("Enter data according to the format shown above")
    for i in range(1,5):
        var=input(f"Enter the {list1[i-1]} : ")
        var=var.upper()
        data[i]=var
    list2=[data]    
    df=pd.DataFrame(list2)
    df.to_csv('batch.csv',mode='a+',index=False,header=False)
    batches=pd.read_csv('batches.csv')
    updateStuList()    

def studInBatch():
    students=pd.read_csv('students2022.csv')
    val=input("Enter the BatchID")
    val=val.upper()
    list1=[val]
    display_Data(students[students.BATCH_ID.isin(list1)])
##Finding courses running in a batch
def courseInBatch():
    batches=pd.read_csv('batches.csv')
    course=pd.read_csv('course.csv')
    value=input("Enter the BATCH_ID whose courses you want to see\n")
    value=value.upper()
    for i in batches.index:
        if batches.iloc[i,0]==value:
            list1=batches.iloc[i,3].split(':')
            #print(list1)
            break
    display_Data(course.query('COURSEID==@list1').drop('MARKS_OBTAINED',axis=1))
def batch_Graph():
    import matplotlib.pyplot as plt
    course=pd.read_csv('Course.csv')
    #perf=pd.DataFrame(index=students.loc[:,'STUDENT_ID'],columns=course.COURSEID)
    a=0
    b=0
    c=0
    d=0
    e=0
    f=0
    for i in course.index:
        couid=course.loc[i,'COURSEID']
        A=(course.iloc[i,2]).split(",")
        for j in A:
            k=j.split(":")
            if int(k[1])>=90:
                a+=1
            elif int(k[1])>=80 and int(k[1])<90:
                b+=1
            elif int(k[1])>=70 and int(k[1])<80:
                c+=1
            elif int(k[1])>=60 and int(k[1])<70:
                d+=1
            elif int(k[1])>=50 and int(k[1])<60:
                e+=1   
            elif int(k[1])<50:
                f+=1    
    student_Grade=['A','B','C','D','E','F']
    student_values=[a,b,c,d,e,f]
    plt.figure(figsize=(9,15))
    plt.pie(student_values,labels=student_Grade,shadow=True,autopct="%2.1f%%")
    plt.legend(title="Grade")
    plt.show()
#performance of a particular Batch
def BatchPerf():
    students=pd.read_csv('students2022.csv')
    bat=input("Enter the BATCH_ID : ")
    bat=bat.upper()
    df1=view_Overall_Perf()
    df3=pd.merge(students,df1,left_on='STUDENT_ID',right_on=df1.index)
    df3=df3.round(2)
    df3=df3[df3.BATCH_ID==bat]
    score=0
    display_Data(df3)
#     for i in df3.index:
#         score+=float(df3.loc[i,'Percentage'])
#     avg=score/len(df3)
#     dict0.update({bat:avg})    

def DepartFunc():
    print("These are the possible functions of the Department module :")
    print("1. Create new Department")
    print("2. View all batches in a department")
    print("3. View average performance of all batches in the department") 
    print("4. Show department statistics")
    choose=int(input("Enter the number of the function you want to perform :"))
    if choose==1:
        createDepartment() 
    elif choose==2:
        BatchInDep()
    elif choose==3:
        perfinDep()
    elif choose==4:
        depart_graph()
def createDepartment():
    department=pd.read_csv('Department.csv')
    display_Data(department)
    list1=['Department ID','Department Name','List Of Batches']
    data = {1:[],2:[],3:[],4:[]}
    for i in range(1,5):
        var=input(f"Enter the {list1[i-1]} : ")
        var=var.upper()
        data[i]=var
    list2=[data]    
    df=pd.DataFrame(list2)
    df.to_csv('Department.csv',mode='a+',index=False,header=False)
    department=pd.read_csv('Department.csv')

def depart_graph():
    import matplotlib.pyplot as plt
    department=pd.read_csv('Department.csv')
    dict0={}
    list1=''
    dep=input("Enter the Department ID : ")
    dep=dep.upper()
    for i in department.index:
        if department.loc[i,'Department_ID']==dep:
             list1=department.loc[i,'List_of_Batches']
    #print(list1)
    for i in list1.split(","):
        bat=i
        bat=bat.upper()
        #print(bat)
        df1=view_Overall_Perf()
        df3=pd.merge(students,df1,left_on='STUDENT_ID',right_on=df1.index)
        df3=df3.round(2)
        #display_Data(df3)
        df3=df3[df3.BATCH_ID==bat]
        score=0
        #display_Data(df3)
        for i in df3.index:
            score+=float(df3.loc[i,'Percentage'])
        avg=score/len(df3)
        dict0.update({bat:avg})
    fig, ax = plt.subplots()
    for j in dict0:
        x=list(dict0.keys())
        y=list(dict0.values())
        ax.plot(x, y,marker=".",markerfacecolor='blue', markersize=15,label=j[0],linewidth=3)
        plt.xlabel("BATCH_ID ------>")
        plt.ylabel("Average Percentage of the Batch ----->")
        plt.title(f"Performane Graph for Department of {dep}")
    plt.show()
def view_Overall_Perf():    
    course=pd.read_csv('Course.csv')
    perf=pd.DataFrame(index=students.loc[:,'STUDENT_ID'],columns=course.COURSEID)
    for i in course.index:
        couid=course.loc[i,'COURSEID']
        a=(course.iloc[i,2]).split(",")
        for j in a:
            k=j.split(":")
            #print(k)
            perf.loc[k[0],couid]=int(k[1])
    
    #perf.astype(int)
    df2=perf.mean(axis='columns')
    df2.columns='Percentage'
    data={"Percentage":df2}
    dframe=pd.DataFrame(data)
    #df4=perf.mean(axis='index')
    
    perf[perf.isnull()]='-'
    #display_Data(dframe)
    #perf[perf.loc[:,:]==0]="-"
    df1=pd.merge(perf,dframe,left_index=True,right_index=True)
    for i in df1.index:
        if df1.loc[i,'Percentage']<50:
            df1.loc[i,'Grade']='F'
        elif df1.loc[i,'Percentage']<=60 and df1.loc[i,'Percentage']>=50:
            df1.loc[i,'Grade']='E'
        elif df1.loc[i,'Percentage']<=70 and df1.loc[i,'Percentage']>60:
            df1.loc[i,'Grade']='D' 
        elif df1.loc[i,'Percentage']<=80 and df1.loc[i,'Percentage']>70:
            df1.loc[i,'Grade']='C'
        elif df1.loc[i,'Percentage']<=90 and df1.loc[i,'Percentage']>80:
            df1.loc[i,'Grade']='B'    
        elif df1.loc[i,'Percentage']<=100 and df1.loc[i,'Percentage']>90:
            df1.loc[i,'Grade']='A'
        if df1.loc[i,'Grade']=='F':
            df1.loc[i,'Pass_Status']='Fail'
        else:
            df1.loc[i,'Pass_Status']='Pass'
    #display_Data(df1.round(2))
    return df1
#Finding Batches running in a department
def BatchInDep():
    batches=pd.read_csv('batches.csv')
    val=input("Enter the Department ID whose batches you want to see :")
    val=val.upper()
    print(f"The Batches running in Department {val} are :")
    display_Data(batches.Batch_ID[batches.Batch_ID.str.startswith(val)])


def ExaminationsFunc():
    print("These are the possible functions of the Examination module :")
    print("1. Enter marks of all students for a specific examination")
    print("2. View performance of all students in the examination ")
    print("3. Show examination statistics")
     
    choose=int(input("Enter the number of the function you want to perform :"))
    if choose==1:
        updateMarks()
    elif choose==2:
        ad=view_Overall_Perf()
        display_Data(ad)
    elif choose==3:
        ScatterGraph()

def updateMarks():
    course=pd.read_csv('Course.csv')
    display_Data(course.drop(columns='MARKS_OBTAINED'))
    coid=input("Enter the Course ID :")
    coid=coid.upper()
    list0=[]
    print(f"To enter marks of all students for the course {coid} enter 1")
    print(f"To enter marks of a particular for the course {coid} enter 2")
    choice=int(input())
    if choice==1:
        for i in batches.index:
            if (coid in batches.iloc[i,3].split(':')):
                for j in students.index:
                    stud=students.iloc[j,0]
                    if stud.startswith(batches.iloc[i,0]):
                        val=int(input(f"Enter the marks of {stud} for the course {coid} : "))
                        for row in course.index:
                            if course.iloc[row,0]==coid:
                                list0.append(f"{stud}:{val}")
                                to_remov = {"[":"","]":"","'":"","'":""," ":""}
                                string=str(list0)
                                for char in to_remov.keys():
                                    string = string.replace(char, to_remov[char])
                                course.iloc[row,2]=string
        course.to_csv('Course.csv',index=False)
          
    elif choice==2:
        list1=[]
        for i in batches.index:
            if (coid in batches.iloc[i,3].split(':')):
                for j in students.index:
                    stud=students.iloc[j,0]
                    
                    if stud.startswith(batches.iloc[i,0]):
                        list1.append(stud)
        print(f"These are the students present in {coid} Course : {list1}")
        studId=input("Enter one of the above given Id : ")
        studId=studId.upper()
        val=int(input(f"Enter the marks of {studId} for the course {coid} : "))
        for row in course.index:
            if course.iloc[row,0]==coid:
                temp=course.iloc[row,2].split(",")
                temp=[s.strip() for s in temp]
                #print(temp)
                for tem in range(len(temp)):
                    temp[tem].strip()
                    if temp[tem].startswith(studId):
                        tempstr=temp[tem].split(':')
                        tempstr[1]=val
                        temp[tem]=str(tempstr[0])+":"+str(tempstr[1])
                        break
                #print(temp)
                to_remov = {"[":"","]":"","'":"","'":""," ":"",'"':"",'"':""}
                string=str(temp)
                for char in to_remov.keys():
                    string = string.replace(char, to_remov[char])
                course.iloc[row,2]=string
                course.to_csv('Course.csv',index=False)
                break
    display_Data(course)
#performance of a particular Department
def perfinDep():
    students=pd.read_csv('students2022.csv')
    batches=pd.read_csv('batches.csv')
    dict0={}
    dep=input("Enter the Department ID : ")
    dep=dep.upper()
    df1=view_Overall_Perf()
    df3=pd.merge(students,df1,left_on='STUDENT_ID',right_on=df1.index)
    df3=df3.round(2)
    display_Data(df3[df3.BATCH_ID.str.startswith(dep)])

def ScatterGraph():
    import matplotlib.pyplot as plt
    course=pd.read_csv('Course.csv')
    perf=pd.DataFrame(index=students.loc[:,'STUDENT_ID'],columns=course.COURSEID)
    list1=[]
    list0=[]
    list2=["Red","Blue","Green","Brown","Pink","Red"]
    fig, ax = plt.subplots()
    for i in course.index:
        couid=course.loc[i,'COURSEID']
        a=(course.iloc[i,2]).split(",")
        for j in a:
            k=j.split(":")
            #print(k)
            list0.append(int(k[1]))
            list1.append(k[0])            
            perf.loc[k[0],couid]=int(k[1])
        ax=plt.scatter(list0,list1,color=list2[i])
    plt.show()                     
mainFunc()          
