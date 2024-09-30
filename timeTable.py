import json
import csv
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

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
Other_subj={'LAB1':['P','C'],'LAB2':['B'],'LAB3':['M','CS']}
TeachersData_fromfile={}
ClassesData_fromfile={}
subsTeach_data,subsClass_data={},{}
totalPeriod=8

##File handling
#Convert from & to csv & json
#csv teach
def ConvertToCSVTeach(folderPath,fileName,TeachersData,rowHeadings=['subj','classes','Leave']):
    csv_file=folderPath+fileName+'.csv'
    with open(csv_file,'w',newline='') as fc:
        Mrwriter=csv.writer(fc)
        Mrwriter.writerow(['TEACHERS']+rowHeadings)

        for k in TeachersData:
            Li=[]
            for i in rowHeadings:
                Li.append(TeachersData[k][i])
            Mrwriter.writerow([k]+Li)

def ConvertFromCSVTeach(folderPath,fileName,rowHeadings=['subj','classes','Leave']):
        csv_file=folderPath+fileName+'.csv'
        with open(csv_file,'r',newline='') as fc:
            Mrreader=csv.reader(fc)
            Teachers_dict={}
            for index,values in enumerate(Mrreader):
                if index!=0:
                    Teachers_dict[values[0]]=dict(zip(rowHeadings,[values[1],eval(values[2]),eval(values[3])]))
            return Teachers_dict
#csv class                 
def ConvertToCSVClass(folderPath,fileName,ClassesData):
    csv_file=folderPath+fileName+'.csv'
    with open(csv_file,'w',newline='') as fc:
        Mrwriter=csv.writer(fc)
        for curr_class in ClassesData:
            Mrwriter.writerow(['Class:',curr_class])
            curr_class_data=ClassesData[curr_class]
            for curr_day in curr_class_data:
                Mrwriter.writerow([curr_day]+curr_class_data[curr_day])
def ConvertFromCSVClass(folderPath,fileName):
        csv_file=folderPath+fileName+'.csv'
        with open(csv_file,'r',newline='') as fc:
            Mrreader=csv.reader(fc)
            Classess_dict={}
            curr_class_timetable={}
            curr_class=''
            for values in Mrreader:
                
                if values[0].lower()=="class:":
                    curr_class=values[1]
                    Classess_dict[curr_class]={'M':[],'T':[],'W':[],'TH':[],'F':[],'S':[]}
                else:
                    
                    Classess_dict[curr_class][values[0]]=values[1:]
            return Classess_dict
# ConvertToCSVClass('C:/Users/radin/Documents/Adi light/Code/school-time-table/csv/','ClassesData')
# ConvertFromCSVClass('C:/Users/radin/Documents/Adi light/Code/school-time-table/csv/','ClassesData')
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
                        # print("-"*10,Day_timetable[subj_ind])
                        if Teach_data['subj'] == Day_timetable[subj_ind]:
                            # print("Day",Day_timetable[subj_ind],"Teach",Teach_data['subj'])
                            #checks if this teachers subj in that day's timetable
                            Day_timetable[subj_ind]=Teach_name
                        # elif Day_timetable[subj_ind] in Other_subj:
                        #     respctive_subj=Other_subj[Day_timetable[subj_ind]]
                        #     for lab_subjects in respctive_subj: 
                        #         print(respctive_subj,Day_timetable[subj_ind])
                            
                        # just subjs are printed if it is yet to assign
    
    return Classes_Teacher_table_Copy

# 2.Teachers-class time table = Assign class to teachers (primary)
# print("new:",ClassTeacherTimetable(Classes))
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
    # print("TEACERS",TeachersData==Teachers,'\n\n',"*"*100,Classes,'\n\n')
    Teachers_class_timetable = TeacherClassTimetable(TeachersData,ClassesData).copy()
    Class_Teachers_timetable = ClassTeacherTimetable(Classes).copy()
    
    Substitution_adjusted_teachers_table={}
    Substitution_adjusted_classesforTeachers_table={}
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
                        
                        if period_i == 0:#start
                           
                            Final_selectionOf_teachers[period_i]=(sorted_eligibal_teach[0][0])
                            
                        else:#mid & last
                            
                            k=0
                            
                          
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
                       
                print("\nFINAL SELECTION:",Final_selectionOf_teachers)         
                print('Teacher to be Subs:',one_leave_teacher,'\n')            
                        

                #UPDATE & REPLACE & GENERATE
                #replace use the suitable teacher to replace leave teacher in the class-teacher table in the period_i  
                #upd class_teach & teach_class TABLES
                #Get the class and make the teacher of the ith period as the selected one

                #class-teacher data
                print("\t\t\tRESULT:")
                for Leave_class_ind in range(len(teach_leaveday_classes)):
                    Specific_class_name = teach_leaveday_classes[Leave_class_ind]
                    if Specific_class_name!='free':
                        print("original:",end="")
                        print(Class_Teachers_timetable[Specific_class_name][Leave_day])
                        print("Changed:",end="")
                        Class_Teachers_timetable[Specific_class_name][Leave_day][Leave_class_ind]=Final_selectionOf_teachers[Leave_class_ind]
                        print(Class_Teachers_timetable[Specific_class_name][Leave_day])
                        
                #teacher-class
                Substitution_adjusted_teachers_table=TeacherClassTimetable(Teachers,Class_Teachers_timetable)
                Substitution_adjusted_classesforTeachers_table=ClassTeacherTimetable(Class_Teachers_timetable)
    
    return [Substitution_adjusted_teachers_table,Class_Teachers_timetable]
#Create a pdf from the SubClassesDatatable 
def csv_to_pdf_SubClasses(csv_file_path, pdf_file_path):
    # Read the CSV file into a DataFrame
    rowsToSkip=[]
    classNames=[]
    rows=[]
    header=['S/P','1','2','3','4','5','6','7','8']
    with open(csv_file_path,'r',newline='') as fc:
        fr=csv.reader(fc)
        ci=0
        for i in fr:
            print(i)
            if len(i)<4:
                rowsToSkip.append(ci)
                classNames.append(i[1])
            else:
                if 4<len(i)<9:
                    rows.append([*i,'','',''])
                else:
                    rows.append(i)
            ci+=1
    print(classNames,rowsToSkip,rows)

    
    
    # Create a PDF file to save the tables
    with PdfPages(pdf_file_path) as pdf:
        # Create the first figure for the first table
        for i in range(len(classNames)):
            fig, ax= plt.subplots(figsize=(8, 6))  # Adjust size as needed
            ax.axis('tight')
            ax.axis('off')
            
            # Create the first table
            if i==0:
                ax.table(cellText=rows[:5+1], colLabels=header, cellLoc='center', loc='center')
            else:
                st,en=i*5,5+i*5
                ax.table(cellText=rows[st+1:en+2], colLabels=header, cellLoc='center', loc='center')
          

            ax.set_title(classNames[i], fontweight="bold")

            # Save the first table to the PDF
            pdf.savefig(fig)
            plt.close(fig)  # Close the figure to free memory

      

    print(f"Successfully created a PDF with two tables from {csv_file_path} on separate pages.")

#TK fns
def Button_gen():
    TeachersData_fromfile = ConvertFromCSVTeach('./csv/','TeachersData')
    ClassesData_fromfile = ConvertFromCSVClass('./csv/','ClassesData')

    SubsAdj_teach_timetable,SubsAdj_class_timetable=SubstitutionTimeTablesHandler(TeachersData_fromfile,Classes)
    # print("+"*100,SubsAdj_teach_timetable)
    ConvertToCSVTeach('./csv/Final Subs/','SubsTeachersData',SubsAdj_teach_timetable,rowHeadings=days)
    ConvertToCSVClass('./csv/Final Subs/','SubsDailyTeachersData',SubsAdj_teach_timetable)
    ConvertToCSVClass('./csv/Final Subs/','SubsClassesData',SubsAdj_class_timetable)
    messagebox.showinfo("Success","Check the csv in the Subs folder")


def Button_fn2():
    response = messagebox.askyesno("Are you sure?","Do you want the Teacher.csv values to be replaced by a default TEMPLATE")
    if response:
        ConvertToCSVTeach('./csv/','TeachersData',Teachers)

def Button_fn3():
    response = messagebox.askyesno("Are you sure?","Do you want the ClassesData.csv values to be replaced by a default TEMPLATE")
    if response:
        ConvertToCSVClass('./csv/','ClassesData',Classes)

#Tk intitial
def startTK():
    win_dime=500
    top = Tk()
    top.geometry(f"{win_dime}x{win_dime}")
    top.title("Substitution Teacher handler")
    # Style configuration
    style = ttk.Style()
    style.configure('TButton', font=('Helvetica', 12), padding=10)
    style.map('TButton', background=[('active', '#ff9999'), ('!disabled', '#ff6666')])

    space=80
    BHeight=50
    Cx,Cy=win_dime/3,win_dime/3 #<- 3rd  button's x & y

    B1 = ttk.Button(top, text ="Put Substitutions", command = Button_gen)
    B2 = ttk.Button(top, text ="Reset TeachersData.csv", command =Button_fn2)
    B3 = ttk.Button(top, text ="Reset ClassesData.csv", command =Button_fn3)

    B1.place(x=Cx,y=Cy-space,  height=BHeight)
    B2.place(x=Cx,y=Cy,  height=BHeight)
    B3.place(x=Cx,y=Cy+space, height=BHeight)
    top.mainloop()
# startTK()
# B2 = Button(top, text ="Reset teach csv", command =lambda:ConvertToCSVTeach('C:/Users/radin/Documents/Adi light/Code/school-time-table/csv/','TeachersData',['subj','classes','Leave']))



###FEATURES
#1. Drop down to add the laeve teachers and the days one by one
#2. Drop down to fetch only the required teachers details and display it either in the Tkinter or cmd
