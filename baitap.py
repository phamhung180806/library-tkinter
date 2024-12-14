



import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import pandas as pd
import os

class EmployeeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Information")


        self.fields = ["Mã", "Tên", "Ngày sinh", "Giới tính", "Đơn vị", "Chức danh", "Số CMND", "Ngày cấp"]
        self.entries = {}

        for idx, field in enumerate(self.fields):
            label = tk.Label(root, text=field)
            label.grid(row=idx, column=0)
            entry = tk.Entry(root)
            entry.grid(row=idx, column=1)
            self.entries[field] = entry


        self.checkbox_customer = tk.IntVar()
        self.checkbox_supplier = tk.IntVar()
        tk.Checkbutton(root, text="Là khách hàng", variable=self.checkbox_customer).grid(row=len(self.fields), column=0)
        tk.Checkbutton(root, text="Là nhà cung cấp", variable=self.checkbox_supplier).grid(row=len(self.fields), column=1)


        save_button = tk.Button(root, text="Lưu thông tin", command=self.save_info)
        save_button.grid(row=len(self.fields) + 1, column=0, columnspan=2)


        birthday_button = tk.Button(root, text="Sinh nhật ngày hôm nay", command=self.today_birthday)
        birthday_button.grid(row=len(self.fields) + 2, column=0, columnspan=2)


        export_button = tk.Button(root, text="Xuất toàn bộ danh sách", command=self.export_list)
        export_button.grid(row=len(self.fields) + 3, column=0, columnspan=2)

    def save_info(self):

        data = {field: self.entries[field].get() for field in self.fields}
        data["Là khách hàng"] = self.checkbox_customer.get()
        data["Là nhà cung cấp"] = self.checkbox_supplier.get()

        df = pd.DataFrame([data])


        if not os.path.exists("employees.csv"):
            df.to_csv("employees.csv", index=False)
        else:
            df.to_csv("employees.csv", mode='a', header=False, index=False)

        messagebox.showinfo("Thành công", "Thông tin đã được lưu!")

    def today_birthday(self):
        try:
            df = pd.read_csv("employees.csv")
            today = datetime.today().strftime('%d/%m')
            birthdays = df[df['Ngày sinh'].str[:5] == today]
            if not birthdays.empty:
                messagebox.showinfo("Sinh nhật hôm nay", birthdays.to_string(index=False))
            else:
                messagebox.showinfo("Sinh nhật hôm nay", "Hôm nay không có ai sinh nhật!")
        except FileNotFoundError:
            messagebox.showerror("Lỗi", "File dữ liệu chưa tồn tại!")

    def export_list(self):
        try:
            df = pd.read_csv("employees.csv")

            df['Ngày sinh'] = pd.to_datetime(df['Ngày sinh'], format='%d/%m/%Y', errors='coerce')
            df = df.dropna(subset=['Ngày sinh'])
            df.sort_values(by='Ngày sinh', inplace=True, ascending=False)
            df.to_excel("employee_list.xlsx", index=False)
            messagebox.showinfo("Thành công", "Danh sách đã được xuất ra file Excel!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xuất danh sách: {e}")

if _name_ == "_main_":
    root = tk.Tk()
    app = EmployeeApp(root)
    root.mainloop()



