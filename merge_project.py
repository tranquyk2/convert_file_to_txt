import os
import tkinter as tk
from tkinter import filedialog, messagebox
import PyPDF2
from PIL import Image
import pytesseract
from docx import Document
import pandas as pd
import chardet
import sys

def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        result = chardet.detect(file.read(10000))
    return result['encoding']

def convert_to_text(file_path, output_file):
    ext = os.path.splitext(file_path)[1].lower()
    try:
        if ext == '.pdf':
            with open(file_path, 'rb') as file:
                pdf = PyPDF2.PdfReader(file)
                text = ''.join(page.extract_text() or '' for page in pdf.pages)
                output_file.write(f"\n\n--- {file_path} ---\n{text}")
        elif ext in ['.png', '.jpg', '.jpeg']:
            text = pytesseract.image_to_string(Image.open(file_path))
            output_file.write(f"\n\n--- {file_path} ---\n{text}")
        elif ext == '.docx':
            doc = Document(file_path)
            text = '\n'.join(para.text for para in doc.paragraphs)
            output_file.write(f"\n\n--- {file_path} ---\n{text}")
        elif ext in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path)
            text = df.to_string()
            output_file.write(f"\n\n--- {file_path} ---\n{text}")
        elif ext in ['.txt', '.java', '.html', '.css', '.xml', '.properties']:
            encoding = detect_encoding(file_path) or 'utf-8'
            try:
                with open(file_path, 'r', encoding=encoding) as file:
                    output_file.write(f"\n\n--- {file_path} ---\n{file.read()}")
            except UnicodeDecodeError:
                with open(file_path, 'r', encoding='latin1') as file:
                    output_file.write(f"\n\n--- {file_path} ---\n{file.read()}")
        else:
            output_file.write(f"\n\n--- {file_path} ---\n[Không hỗ trợ định dạng]")
    except Exception as e:
        output_file.write(f"\n\n--- {file_path} ---\n[Lỗi: {str(e)}]")

def merge_project():
    folder_path = filedialog.askdirectory(title="Chọn thư mục project")
    if not folder_path:
        messagebox.showerror("Lỗi", "Chưa chọn thư mục!")
        return
    output_file = os.path.join(folder_path, 'project_merged.txt')
    try:
        with open(output_file, 'w', encoding='utf-8') as out:
            out.write(f"Project: {os.path.basename(folder_path)}\n\n")
            for root, _, files in os.walk(folder_path):
                for file in files:
                    if file != 'project_merged.txt':
                        convert_to_text(os.path.join(root, file), out)
        messagebox.showinfo("Thành công", f"Đã tạo {output_file}")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể tạo file: {str(e)}")

def create_main_window():
    root = tk.Tk()
    root.title("Merge Project Files")
    root.geometry("300x150")
    root.resizable(False, False)

    # Đặt giao diện
    label = tk.Label(root, text="Chào mừng đến với Merge Project", font=("Arial", 12))
    label.pack(pady=20)

    start_button = tk.Button(root, text="Bắt đầu", font=("Arial", 10), width=10, command=lambda: [root.destroy(), merge_project()])
    start_button.pack(pady=10)

    # Đặt cửa sổ ở giữa màn hình
    root.eval('tk::PlaceWindow . center')
    root.mainloop()

if __name__ == "__main__":
    pytesseract.pytesseract.tesseract_cmd = r'Tesseract\tesseract.exe'
    if len(sys.argv) > 1:  # Chạy từ terminal với tham số
        folder_path = sys.argv[1]
        if os.path.isdir(folder_path):
            output_file = os.path.join(folder_path, 'project_merged.txt')
            with open(output_file, 'w', encoding='utf-8') as out:
                out.write(f"Project: {os.path.basename(folder_path)}\n\n")
                for root, _, files in os.walk(folder_path):
                    for file in files:
                        if file != 'project_merged.txt':
                            convert_to_text(os.path.join(root, file), out)
            print(f"Đã tạo {output_file}")
        else:
            print("Thư mục không hợp lệ!")
    else:  # Chạy GUI
        create_main_window()