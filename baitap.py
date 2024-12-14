import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import pandas as pd
import os

class EmployeeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Thông tin nhân viên")

        # Labels và Entries
        self.fields = [
            "Mã", "Tên", "Ngày sinh", "Đơn vị", "Chức danh", "Số CMND", "Ngày cấp"
        ]
        self.entries = {}

        # Tạo giao diện cho từng field
        for idx, field in enumerate(self.fields):
            label = tk.Label(root, text=field, font=("Arial", 10))
            label.grid(row=idx, column=0, padx=5, pady=5, sticky="e")

            entry = tk.Entry(root, width=30)
            entry.grid(row=idx, column=1, padx=5, pady=5, sticky="w")
            self.entries[field] = entry

        # Giới tính (Radio Buttons)
        tk.Label(root, text="Giới tính", font=("Arial", 10)).grid(row=2, column=2, sticky="e")
        self.gender_var = tk.StringVar(value="Nam")
        tk.Radiobutton(root, text="Nam", variable=self.gender_var, value="Nam").grid(row=2, column=3, sticky="w")
        tk.Radiobutton(root, text="Nữ", variable=self.gender_var, value="Nữ").grid(row=3, column=3, sticky="w")

        # Checkbox Là khách hàng / Là nhà cung cấp
        self.customer_var = tk.IntVar()
        self.supplier_var = tk.IntVar()
        tk.Checkbutton(root, text="Là khách hàng", variable=self.customer_var).grid(row=0, column=2, sticky="w")
        tk.Checkbutton(root, text="Là nhà cung cấp", variable=self.supplier_var).grid(row=1, column=2, sticky="w")

        # Nút Lưu thông tin
        tk.Button(root, text="Lưu thông tin", command=self.save_info).grid(row=8, column=0, columnspan=2, pady=5)

        # Nút Sinh nhật hôm nay
        tk.Button(root, text="Sinh nhật ngày hôm nay", command=self.check_birthday).grid(row=9, column=0, columnspan=2, pady=5)

        # Nút Xuất danh sách
        tk.Button(root, text="Xuất toàn bộ danh sách", command=self.export_to_excel).grid(row=10, column=0, columnspan=2, pady=5)

    def save_info(self):
        # Lưu thông tin vào file CSV
        data = {field: self.entries[field].get() for field in self.fields}
        data["Giới tính"] = self.gender_var.get()
        data["Là khách hàng"] = self.customer_var.get()
        data["Là nhà cung cấp"] = self.supplier_var.get()

        df = pd.DataFrame([data])

        file_exists = os.path.exists("employees.csv")
        df.to_csv("employees.csv", mode='a', header=not file_exists, index=False, encoding='utf-8-sig')
        messagebox.showinfo("Thành công", "Thông tin đã được lưu!")

    def check_birthday(self):
        try:
            df = pd.read_csv("employees.csv", encoding='utf-8-sig')
            today = datetime.today().strftime('%d/%m')
            df['Ngày sinh'] = pd.to_datetime(df['Ngày sinh'], format='%d/%m/%Y', errors='coerce')
            birthdays = df[df['Ngày sinh'].dt.strftime('%d/%m') == today]

            if not birthdays.empty:
                result = "\n".join(birthdays['Tên'].tolist())
                messagebox.showinfo("Sinh nhật hôm nay", f"Những người có sinh nhật hôm nay:\n{result}")
            else:
                messagebox.showinfo("Sinh nhật hôm nay", "Hôm nay không có ai sinh nhật!")
        except FileNotFoundError:
            messagebox.showerror("Lỗi", "File dữ liệu không tồn tại!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi: {e}")

    def export_to_excel(self):
        try:
            df = pd.read_csv("employees.csv", encoding='utf-8-sig')
            df['Ngày sinh'] = pd.to_datetime(df['Ngày sinh'], format='%d/%m/%Y', errors='coerce')
            df = df.dropna(subset=['Ngày sinh'])
            df.sort_values(by='Ngày sinh', ascending=True, inplace=True)

            df.to_excel("employee_list.xlsx", index=False, engine='openpyxl')
            messagebox.showinfo("Thành công", "Danh sách đã được xuất ra file Excel!")
        except FileNotFoundError:
            messagebox.showerror("Lỗi", "File dữ liệu không tồn tại!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeeApp(root)
    root.mainloop()




