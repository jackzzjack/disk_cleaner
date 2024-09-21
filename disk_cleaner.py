import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import subprocess

# 版本號
VERSION = "1.0.0"

# 建立主視窗
root = tk.Tk()
root.title(f"抓取大檔案 - 版本 {VERSION}")
root.geometry("800x600")

# 選擇資料夾的函數
def select_folder():
    folder_selected = filedialog.askdirectory(title="選擇資料夾")
    if folder_selected:
        folder_label.config(text=f"選擇的資料夾: {folder_selected}")
        find_largest_files(folder_selected)

# 打開檔案所在的資料夾
def open_folder(file_path):
    folder = os.path.dirname(file_path)
    try:
        if os.name == 'nt':  # Windows
            os.startfile(folder)
        elif os.name == 'posix':  # Mac 和 Linux
            subprocess.Popen(['open', folder] if sys.platform == 'darwin' else ['xdg-open', folder])
    except Exception as e:
        messagebox.showerror("錯誤", f"無法打開資料夾: {str(e)}")

# 找出最大的檔案 (遞迴方式) 並顯示進度
def find_largest_files(folder_path):
    try:
        # 使用 os.walk 遞迴取得所有檔案
        files = []
        for root_dir, _, filenames in os.walk(folder_path):
            for filename in filenames:
                full_path = os.path.join(root_dir, filename)
                if os.path.isfile(full_path):
                    files.append(full_path)

        # 設置進度條最大值
        progress_bar['maximum'] = len(files)

        # 按檔案大小排序，取前 100 個檔案
        files.sort(key=lambda x: os.path.getsize(x), reverse=True)
        largest_files = files[:100]

        # 清除之前的結果
        result_text.delete(1.0, tk.END)

        # 顯示結果並讓路徑可點擊
        for i, file in enumerate(largest_files):
            size_in_bytes = os.path.getsize(file)
            if size_in_bytes >= 1024 ** 3:  # 大於等於 1 GB
                size_in_gb = size_in_bytes / (1024 ** 3)
                size_str = f"{size_in_gb:.2f} GB"
            else:
                size_in_mb = size_in_bytes / (1024 ** 2)
                size_str = f"{size_in_mb:.2f} MB"

            file_display = f"{i+1:<5}檔案: {os.path.basename(file):<30}\t大小: {size_str:<10}\t路徑: {file}\n"
            result_text.insert(tk.END, file_display)

            # 加入點擊事件
            start_index = f"{i+1}.0"
            end_index = f"{i+1}.end"
            result_text.tag_add(f"file_{i}", start_index, end_index)
            result_text.tag_bind(f"file_{i}", "<Button-1>", lambda e, path=file: open_folder(path))

            # 更新進度條
            progress_bar['value'] = i + 1
            root.update_idletasks()  # 更新 GUI

        messagebox.showinfo("完成", f"搜尋完成，已顯示前 100 個最大的檔案。\n版本 {VERSION}")
    except Exception as e:
        messagebox.showerror("錯誤", f"無法取得檔案大小: {str(e)}")

# UI 元素
folder_label = tk.Label(root, text="請選擇資料夾", font=("Arial", 12))
folder_label.pack(pady=10)

select_button = tk.Button(root, text="選擇資料夾", command=select_folder, font=("Arial", 12))
select_button.pack(pady=10)

progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress_bar.pack(pady=10)

# 調整 Text 結果欄位以適應視窗大小
result_text = tk.Text(root, wrap=tk.NONE)
result_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# 使用 Scrollbar 讓結果視窗可滾動
scrollbar = ttk.Scrollbar(result_text)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
result_text.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=result_text.yview)

# 開始主迴圈
root.mainloop()