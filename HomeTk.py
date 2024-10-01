import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from timeTable import ConvertFromCSVTeach,Button_gen,give_pdf_path,csv_to_pdf_SubClasses,give_pdf_paths
import csv
# Function to display the download page after generating the output
teach_csv_data=ConvertFromCSVTeach('./csv/','TeachersData')
Teachers_names=list(teach_csv_data.keys())
# print(Teachers_names)
##TODO:
#--Gen list of teachers 
#--Convert MONDAY--> M
#--draft and add to the teachers csv
#--using tk inputs add leave_day to the csv file
#--call generate function
#--convert csv->pdf
#download

def show_download_page():
    download_window = tk.Toplevel(root)  # Create a new window for download
    download_window.title("Download Page")
    download_window.geometry("300x200")

    download_label = tk.Label(download_window, text="Your report is ready!", font=('Arial', 12))
    download_label.pack(pady=20)

    # Download button
    download_button = tk.Button(download_window, text="Download", font=('Arial', 12), width=10, command=download_action)
    download_button.pack(pady=10)

    # Close button to close the download window
    close_button = tk.Button(download_window, text="Close", font=('Arial', 12), width=10, command=download_window.destroy)
    close_button.pack(pady=10)

# Simulating a download action when the download button is clicked
def download_action():
    #sub class pdf
    # subclass_csv_path='./csv/Final Subs/SubsClassesData.csv' 
    # subclass_pdf_path=give_pdf_path()
    # csv_to_pdf_SubClasses(subclass_csv_path,subclass_pdf_path)
    sub_csv_paths=['./csv/Final Subs/SubsClassesData.csv','./csv/Final Subs/SubsDailyTeachersData.csv'] 
    sub_pdf_paths=give_pdf_paths(sub_csv_paths)
    for i in range(len(sub_pdf_paths)):
        csv_to_pdf_SubClasses(sub_csv_paths[i],sub_pdf_paths[i])

    messagebox.showinfo("Download", "Report has been downloaded!")
def addLeavedaystoCSV(folderPath,fileName,SelectedteachName,Unformattedleaveday):
    csv_file=folderPath+fileName+'.csv'
    NewCsvrows=[]
    leaveday=Unformattedleaveday[0] if Unformattedleaveday!="Thursday" else Unformattedleaveday[:2].upper()

    with open(csv_file,'r+',newline='') as fc:
        Mrreader=csv.reader(fc)
        for i,data in enumerate(Mrreader):
            if i == 0: 
                NewCsvrows.append(data)
                continue  # Skip the first iteration
            if data[0]==SelectedteachName and leaveday not in eval(data[3]):
                # print(eval(data[3]))
                NewCsvrows.append(data[:3]+[str(eval(data[3])+[leaveday])] )
                result_label.config(text=f'Drafted:\nSubstitute Teacher: {SelectedteachName}\nDay: {Unformattedleaveday}')

            elif leaveday in eval(data[3]):
                print('The same input has alreaady been drafted')
                NewCsvrows.append(data)
                result_label.config(text=f'The same input has alreaady been drafted')
            else:
                NewCsvrows.append(data)
        fc.seek(0)
        Mrwriter=csv.writer(fc)
        Mrwriter.writerows(NewCsvrows)
# addLeavedaystoCSV('./csv/','TeachersData','cvr','M')


def addtoCSV():
    selected_teacher = teacher_var.get()
    selected_day = day_var.get()
    if selected_teacher and selected_day:
        addLeavedaystoCSV('./csv/','TeachersData',selected_teacher,selected_day)

# Function to display loading screen and then show the result
def display_loading_and_generate():
    # Show the loading window
    show_loading_window()

    # After 2 seconds, close the loading screen, generate the output, and then show the download page
    # root.after(2000, generate_substitution)
    generate_substitution()

# Function to generate output based on selections
def generate_substitution():
    selected_teacher = teacher_var.get()
    selected_day = day_var.get()
    if selected_day:
        formatted_selected_day=selected_day[0] if selected_day!="Thursday" else selected_day[:2].upper()
    else:
        formatted_selected_day=None
    Button_gen()
    # Close the loading window
    
    # Check if both teacher and day are selected
    if selected_teacher and selected_day:
        result_label.config(text=f'Substitute Teacher: {selected_teacher}\nDay: {formatted_selected_day}')
    show_download_page()

    loading_window.destroy()

# Function to reset the selections and output
def reset_fields():
    teacher_var.set('')
    day_var.set('')
    result_label.config(text='')

# Function to show the loading window
def show_loading_window():
    global loading_window
    loading_window = tk.Toplevel(root)  # Create a new top-level window (a secondary window)
    loading_window.title("Loading...")
    loading_window.geometry("300x200")
    
    loading_label = tk.Label(loading_window, text="Loading, please wait...", font=('Arial', 12))
    loading_label.pack(expand=True, padx=10, pady=10)

# Main window
root = tk.Tk()
root.title("Substitute Teacher Handler")
root.geometry("500x400")

# Substitute Teacher Dropdown
teacher_label = tk.Label(root, text="Substitute Teacher Name:", font=('Arial', 12))
teacher_label.pack(pady=10)

teacher_var = tk.StringVar()
teacher_dropdown = ttk.Combobox(root, textvariable=teacher_var, font=('Arial', 12))
teacher_dropdown['values'] = Teachers_names
teacher_dropdown.pack(pady=10)

# Day Dropdown
day_label = tk.Label(root, text="Day:", font=('Arial', 12))
day_label.pack(pady=10)

day_var = tk.StringVar()
day_dropdown = ttk.Combobox(root, textvariable=day_var, font=('Arial', 12))
day_dropdown['values'] = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday")
day_dropdown.pack(pady=10)

# Generate and Reset Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=20)

generate_button = tk.Button(button_frame, text="Draft", command=addtoCSV, font=('Arial', 12), width=10)
generate_button.grid(row=0, column=0, padx=10)
generate_button = tk.Button(button_frame, text="Generate", command=display_loading_and_generate, font=('Arial', 12), width=10)
generate_button.grid(row=0, column=1, padx=10)

reset_button = tk.Button(button_frame, text="Reset", command=reset_fields, font=('Arial', 12), width=10)
reset_button.grid(row=0, column=2, padx=10)

# Result Label
result_label = tk.Label(root, text="", font=('Arial', 14), fg="green")
result_label.pack(pady=20)

# Run the application
root.mainloop()
