import pandas as pd
import json
import csv
from tkinter import *
from tkinter import messagebox
#Tk intitial
win_dime=500
top = Tk()
top.geometry(f"{win_dime}x{win_dime}")
##  data one week
#Table1 - class table
Classes={
'A12' : {'M':['C','P','P' ,'M' ,'E','CS ','LAB1 ','LAB1'],'T':['M','P','C','C','E','CS ','LAB1 ','LAB1'],'W':['CS ','P','M','M', 'E','C','LAB3 ','LAB3'],'TH':['CS ','P','M','E','M','C','LAB3 ','LAB3'],'F':['CS ','P' ,'E' ,'PT ','C','C','CS'],'S':['LIB ','P','M','CS ','E']},
'B12' : {'M':['M','E','P','CS','C','C','LAB3','LAB3'],'T':['P','M','CS','E','CS','M','LAB3','LAB3'],'W':['C','M','CS','CS','P','E','E','C'],'TH':['E','C','M','P','LIB','CS','PT','C'],'F':['P','M','CS','M','GS','P','LAB1','LAB1'],'S':['P','C','E','LAB1','LAB1']},
'C12' : {'M':['P','B','M','LIB','C','B','E','PT'],'T':['C','B','GS','P','M','E','C','M'],'W':['P','B','E','C','M','P','LAB1','LAB1'],'TH':['M','B','E','C','P','B','LAB','LAB'],'F':['C','B','P','E','C','M','LAB2','LAB2'],'S':['M','P','E','LAB2','LAB2']}
}
#LAB1=P/C , LAB2=BIO , LAB3 = M/CS <-- convert subj to a list 
#Table2 - teachers table
Teachers={'sowmiya':{'subj':'M','classes':['A12','C12'],'Leave':[]},'gayatri_vp':{'subj':'B','classes':['C12'],'Leave':[]},'divya':{'subj':'P','classes':['C12','B12'],'Leave':[]},'janani':{'subj':'C','classes':['C12'],'Leave':[]},'gayathri_narashiman':{'subj':'E','classes':['C12'],'Leave':[]},'ellamal':{'subj':'PT','classes':['C12','B12'],'Leave':[]},'saraswathi':{'subj':'LIB','classes':['C12','A12','B12'],'Leave':[]},'cvr':{'subj':'E','classes':['A12'],'Leave':[]},'aruna':{'subj':'M','classes':['B12'],'Leave':[]},'sripriya':{'subj':'P','classes':['A12'],'Leave':[]},'buvaneshwari_g':{'subj':'CS','classes':['A12','B12'],'Leave':[]},'gayatri_ramachandran':{'subj':'C','classes':['A12','B12'],'Leave':['M']},}
days=['M','T','W','TH','F','S']
TeachersData_fromfile={}
ClassesData_fromfile={}
subsTeach_data,subsClass_data={},{}
totalPeriod=8

##File handling
#Convert from & to csv & json
#csv teach
def ConvertToCSVTeach(folderPath,fileName,rowHeadings=['subj','classes','Leave']):
    csv_file=folderPath+fileName+'.csv'
    with open(csv_file,'w',newline='') as fc:
        Mrwriter=csv.writer(fc)
        Mrwriter.writerow(['TEACHERS']+rowHeadings)

        for k in Teachers:
            Li=[]
            for i in rowHeadings:
                Li.append(Teachers[k][i])
            Mrwriter.writerow([k]+Li)

def ConvertFromCSVTeach(folderPath,fileName,rowHeadings=['subj','classes','Leave']):
        csv_file=folderPath+fileName+'.csv'
        with open(csv_file,'r',newline='') as fc:
            Mrreader=csv.reader(fc)
            Teachers_dict={}
            for index,values in enumerate(Mrreader):
                if index!=0:
                    Teachers_dict[values[0]]=dict(zip(rowHeadings,values[1:]))
            return Teachers_dict
#csv class                 
def ConvertToCSVClass(folderPath,fileName):
    csv_file=folderPath+fileName+'.csv'
    with open(csv_file,'w',newline='') as fc:
        Mrwriter=csv.writer(fc)
        for curr_class in Classes:
            Mrwriter.writerow(['Class:',curr_class])
            curr_class_data=Classes[curr_class]
            for curr_day in curr_class_data:
                Mrwriter.writerow([curr_day]+curr_class_data[curr_day])

ConvertToCSVClass('C:/Users/radin/Documents/Adi light/Code/school-time-table/csv/','ClassesData')
##  Algos
# 1.class-teachers time table = Assign teachers to class time table(primary) 
def ClassTeacherTimetable(Classesdata):
    #Assigns teachers and produces TEACHERS ASSIGNED TABLE for the classses based on teachers table and classes table
    Classes_Teacher_table_Copy = Classesdata.copy()
    for one_class in Classes_Teacher_table_Copy:
        #get one class data
        Class_data = Classes[one_class]
        for Teach_name in Teachers:
            #get one teachers data
            Teach_data = Teachers[Teach_name]
            if one_class in Teach_data['classes']:
                #check if this class is habdled by this teach
                for day in Class_data:
                    #get day from class_data
                    #get timetable of that date 
                    Day_timetable = Class_data[day]
            
                    for subj_ind in range(len(Day_timetable)):
                        #get subjects index of that timetable
                        
                        if Teach_data['subj'] in Day_timetable[subj_ind]:
                            #checks if this teachers subj in that day's timetable
                            Day_timetable[subj_ind]=Teach_name
                        # just subjs are printed if it is yet to assign
    return Classes_Teacher_table_Copy

# 2.Teachers-class time table = Assign class to teachers (primary)

def createTeachClassedTimetableTempl(TeachersDict):
    Teach_Classes_timetable={}
    for Teach_name in TeachersDict:
        Teach_Classes_timetable[Teach_name]={}
        Teach_dict = Teach_Classes_timetable[Teach_name]
        for day in days:
            if day=='S':
                Teach_dict[day]=['free']*5
            else:
                Teach_dict[day]=['free']*totalPeriod
    return Teach_Classes_timetable

def TeacherClassTimetable(TeachersData,ClassesData):
    Teach_classes_format_original = createTeachClassedTimetableTempl(TeachersData)
    Teach_classes_format =Teach_classes_format_original.copy()
    Classes_Teacher_table_Copy = ClassTeacherTimetable(ClassesData).copy()
    for Teacher in Teach_classes_format:
        Teachers_data= Teach_classes_format[Teacher]
        for day in Teachers_data:
            day_timetable_data = Teachers_data[day]
            for one_class in Classes_Teacher_table_Copy:
                one_class_data = Classes_Teacher_table_Copy[one_class]
                for dayclass in one_class_data:
                    day_timetable_ofcls_data=one_class_data[dayclass]
                    for i in range(len(day_timetable_ofcls_data)):
                        if day_timetable_ofcls_data[i]==Teacher and dayclass == day:
                            day_timetable_data[i]=one_class
    return Teach_classes_format 

# 3. Leave-Teachers Table = Assign substitution acc.to many critias (Generated)

def SubstitutionTimeTablesHandler(TeachersData,ClassesData):
    Teachers = TeachersData
    Classes = ClassesData
    Teachers_class_timetable = TeacherClassTimetable(Teachers,Classes).copy()
    Class_Teachers_timetable = ClassTeacherTimetable(Classes).copy()
    Substitution_adjusted_teachers_table={}
    for teach_id in Teachers:
        teach_data = Teachers[teach_id]
        teach_subj = teach_data['subj']
        teach_classes = teach_data['classes']
        Leave_days = teach_data['Leave']
        if len(Leave_days)>0:
            one_leave_teacher= teach_id
            leave_teach_class_data = Teachers_class_timetable[one_leave_teacher]
            for Leave_day in Leave_days:
                teach_leaveday_classes=leave_teach_class_data[Leave_day]
                eligible_free_teachers={}#for this day
                # Final_selectionOf_teachers=[]#final selection to replace after all sorting
                Final_selectionOf_teachers={}#final selection to replace after all sorting
                period_days_speial=0
                if Leave_day!='S':
                    period_days_speial=totalPeriod
                else:
                    period_days_speial=5
                
                for localperiod in range(period_days_speial):
                    eligible_free_teachers[localperiod]=[]
                for all_teach in Teachers_class_timetable:
                    #generating those teachers eleigible to filter
                    if all_teach!=one_leave_teacher:
                        all_teach_data=Teachers_class_timetable[all_teach]
                        all_teach_leaveday_class = all_teach_data[Leave_day]
                        # print(all_teach_leaveday_class)
                        for period in range(period_days_speial):
                            ith_period_class=all_teach_leaveday_class[period]
                            if ith_period_class=='free' and Leave_day not in Teachers[all_teach]['Leave']:
                                #if ith period is free
                                eligible_free_teachers[period]+=[all_teach]
                # print(eligible_free_teachers)  
         
                              
                #FINDING ELIGIBLE TEACH
                for period_i in eligible_free_teachers:
                    #checking for one period after another
                    if teach_leaveday_classes[period_i]!='free':
                        ith_period_eligible_teachers = eligible_free_teachers[period_i]
                        # print(period_i,ith_period_eligible_teachers)
                        ith_eligblity_score = {}
                        #creating the dict format
                        
                        #sort one who is eligible to the left 
                        for eligible_teacher in ith_period_eligible_teachers:
                        
                            #checking/testing teachers worthiness for the period
                            current_chk_teach_data = Teachers_class_timetable[eligible_teacher]
                            currentchk_teach_class_day = current_chk_teach_data[Leave_day]
                        
                            #Check & scoring
                            #same subj/class handler
                            bool_sameSubj=Teachers[eligible_teacher]['subj'] == teach_subj
                            bool_sameClass=teach_leaveday_classes[period_i] in Teachers[eligible_teacher]['classes']
                            #2 & 3inrows
                            if period_i==0:#start
                                if currentchk_teach_class_day[period_i+1]=='free':
                                    #2inrow
                                    ith_eligblity_score[eligible_teacher]=2
                                    if currentchk_teach_class_day[period_i+2]=="free":
                                        #3inrow
                                        ith_eligblity_score[eligible_teacher]+=2
                            elif period_i==period_days_speial-1:#end
                                if currentchk_teach_class_day[period_i-1]=="free":
                                    #2inrow
                                    ith_eligblity_score[eligible_teacher]=2
                                    if currentchk_teach_class_day[period_i-2]=="free":
                                        #3inrow
                                        ith_eligblity_score[eligible_teacher]+=2
                            else:#mids
                                if currentchk_teach_class_day[period_i-1]=="free" or currentchk_teach_class_day[period_i+1]=="free":
                                    #2inrow
                                    ith_eligblity_score[eligible_teacher]=2
                                    if currentchk_teach_class_day[period_i-1]=="free" and currentchk_teach_class_day[period_i+1]=="free":
                                        #3inrow
                                        ith_eligblity_score[eligible_teacher]+=2                        
                            if bool_sameClass or bool_sameSubj:
                                if eligible_teacher in ith_eligblity_score:
                                            ith_eligblity_score[eligible_teacher]+=1
                                else:
                                    ith_eligblity_score[eligible_teacher]=1
        
                        # print(period_i,ith_eligblity_score) #Eligibilty score is GOOD
                        # print(ith_eligblity_score)
                        #SORTING the dict (eligility score) / take the key with the hightest value -> suitable teacher
                        
                        sorted_eligibal_teach = sorted(ith_eligblity_score.items(), key=lambda x:x[1],reverse=True)
                        # print("sorted",period_i,sorted_eligibal_teach) #sorting score is GOOD
                        # print(sorted_eligibal_teach)

                        #SELECTION if one teacher is selected for one period the next period should not have them   

                        # print(Final_selectionOf_teachers,len(Final_selectionOf_teachers))  
                        print(period_i,end=" : ") 
                        if period_i == 0:#start
                            print(sorted_eligibal_teach)
                            Final_selectionOf_teachers[period_i]=(sorted_eligibal_teach[0][0])
                            
                        else:#mid & last
                            
                            k=0
                            
                            print(sorted_eligibal_teach)
                            while True:
                                #checking if pre period also has same teacher
                                bool_sameTeach_PrePeriod=False
                                if period_i-1 in Final_selectionOf_teachers:
                                    bool_sameTeach_PrePeriod=(Final_selectionOf_teachers[period_i-1]==sorted_eligibal_teach[k][0])
                                if bool_sameTeach_PrePeriod:
                                    #if same teach last period check for the next one
                                    k+=1
                                else:    
                                    Final_selectionOf_teachers[period_i]=(sorted_eligibal_teach[k][0])  
                                    
                                    break    
                       
                        print("-"*10)                         
                       
                print("\nFINAL SELECTION:",Final_selectionOf_teachers,'\n')                     
                        

                #UPDATE & REPLACE & GENERATE
                #replace use the suitable teacher to replace leave teacher in the class-teacher table in the period_i  
                #upd class_teach & teach_class TABLES
                #Get the class and make the teacher of the ith period as the selected one

                #class-teacher data
                print("\t\t\tRESULT:")
                for Leave_class_ind in range(len(teach_leaveday_classes)):
                    Specific_class_name = teach_leaveday_classes[Leave_class_ind]
                    if Specific_class_name!='free':
                        print(Specific_class_name)
                        print("original")
                        print("Changed")
                        print(Class_Teachers_timetable[Specific_class_name][Leave_day])
                        Class_Teachers_timetable[Specific_class_name][Leave_day][Leave_class_ind]=Final_selectionOf_teachers[Leave_class_ind]
                        print(Class_Teachers_timetable[Specific_class_name][Leave_day])
                        print("-"*10)
                #teacher-class
                Substitution_adjusted_teachers_table=TeacherClassTimetable(Teachers,Class_Teachers_timetable)
    # return [Substitution_adjusted_teachers_table,Class_Teachers_timetable]
    subsTeach_data,subsClass_data=Substitution_adjusted_teachers_table,Class_Teachers_timetable
def Button_fn1():
    teachdata=TeachersData_fromfile if TeachersData_fromfile!=False else Teachers
    classdata=ClassesData_fromfile if ClassesData_fromfile!=False else Classes
    SubstitutionTimeTablesHandler(teachdata,classdata)
#TK fns
def Button_fn2():
    response = messagebox.askyesno("Are you sure?","Do you want the values to be replaced by a default TEMPLATE")
    if response:
        ConvertToCSVTeach('C:/Users/radin/Documents/Adi light/Code/school-time-table/csv/','TeachersData',['subj','classes','Leave'])
def Button_fn3():
    global TeachersData_fromfile
    TeachersData_fromfile = ConvertFromCSVTeach('C:/Users/radin/Documents/Adi light/Code/school-time-table/csv/','TeachersData',['subj','classes','Leave'])
    messagebox.showinfo("Success","read CSV successfully")

#TK GUI
space=50
B1 = Button(top, text ="Put Substitutions", command = Button_fn1)
B1.place(x=win_dime/3,y=win_dime/2-space)
B2 = Button(top, text ="Reset teach csv", command =Button_fn2)
B2.place(x=win_dime/3,y=win_dime/2)
B2 = Button(top, text ="use teach.csv values", command =Button_fn3)
B2.place(x=win_dime/3,y=win_dime/2+space)
top.mainloop()
# B2 = Button(top, text ="Reset teach csv", command =lambda:ConvertToCSVTeach('C:/Users/radin/Documents/Adi light/Code/school-time-table/csv/','TeachersData',['subj','classes','Leave']))