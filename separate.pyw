import tkinter as tk
from tkinter import filedialog
from PyPDF2 import PdfReader, PdfWriter
import re
import os

def browse_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        file_path_var.set(file_path)

def separate_pdf():
    file_path = file_path_var.get()
    if not os.path.isfile(file_path):
        progress_var.set('Invalid file path')
        return
    try:
        pdf = PdfReader(file_path)
    except:
        progress_var.set('Error opening PDF file')
        return

    # Loop through the pages
    chapter_num = 1
    processed_matters = 0
    for page_num in range(len(pdf.pages)):
        page = pdf.pages[page_num]

        # Check if this is a cover page
        if 'FILE CLOSING FORM' in page.extract_text():
            # This is a cover page
            closingform = PdfWriter()
            closingform.add_page(page)
            matterNo = re.findall(r'(\d{6})', page.extract_text())[0]
            with open(f'{matterNo} - FCF.pdf', 'wb') as f:
                closingform.write(f)
            processed_matters += 1

            # Check if the next page is also a cover page
            if page_num+1 < len(pdf.pages) and 'FILE CLOSING FORM' in pdf.pages[page_num+1].extract_text():
                # If it is, skip this page and continue to the next one
                continue

            # This is a page with matter content
            new_pdf = PdfWriter()

            # Add the pages until the next cover page
            for next_page_num in range(page_num+1, len(pdf.pages)):
                next_page = pdf.pages[next_page_num]
                if next_page.extract_text().strip() == 'Early Destruction Date cannot be less than 12 months from the last activity on the matter' and len(next_page.extract_text()) == len('Early Destruction Date cannot be less than 12 months from the last activity on the matter'):
                    continue
                if 'FILE CLOSING FORM' in next_page.extract_text():
                    # This is the end of the chapter
                    break
                new_pdf.add_page(next_page)

            # Save the new document to a file
            if len(new_pdf.pages) > 0:
                with open(f'{matterNo} - BOD.pdf', 'wb') as f:
                    new_pdf.write(f)
                chapter_num += 1

        progress_var.set(f'Separated {processed_matters} matters')

root = tk.Tk()
root.title('Matter Separator')

file_path_var = tk.StringVar()

file_frame = tk.Frame(root)
file_frame.pack(fill=tk.BOTH, expand=True)
file_label = tk.Label(file_frame, text='PDF File:')
file_label.pack(side=tk.LEFT)
file_entry = tk.Entry(file_frame, textvariable=file_path_var)
file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
browse_button = tk.Button(file_frame, text='Browse', command=browse_file)
browse_button.pack(side=tk.LEFT)

separator_button = tk.Button(root, text='Separate PDF', command=separate_pdf)
separator_button.pack()

progress_var = tk.StringVar()
progress_label = tk.Label(root, textvariable=progress_var)
progress_label.pack()

root.mainloop()
