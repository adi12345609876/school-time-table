import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import csv
def csv_to_pdf_multiple_tables_separate_pages(csv_file_path, pdf_file_path):
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
            fig, ax= plt.subplots(figsize=(12, 8))  # Adjust size as needed
            ax.axis('tight')
            ax.axis('off')
            
            # Create the first table
            if i==0:
                ax.table(cellText=rows[:5+1], colLabels=header, cellLoc='center', loc='center')
            else:
                st,en=i*5,5+i*5
                ax.table(cellText=rows[st+1:en+2], colLabels=header, cellLoc='center', loc='center')
          

            ax.set_title(classNames[i], fontweight="bold", fontsize=16, pad=1)

            # Save the first table to the PDF
            pdf.savefig(fig)
            plt.close(fig)  # Close the figure to free memory

      

    print(f"Successfully created a PDF with two tables from {csv_file_path} on separate pages.")

# # Example usage
# csv_file_path = './csv/Final Subs/SubsClassesData.csv' # Replace with your CSV file path
# pdf_file_path = 'op.pdf'  # Path where you want to save the PDF

# csv_to_pdf_multiple_tables_separate_pages(csv_file_path, pdf_file_path)
