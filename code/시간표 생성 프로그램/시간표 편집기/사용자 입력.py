import tkinter as tk
from tkinter import messagebox

class GUIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("할 일 입력")

        # 첫 번째 텍스트 입력 창과 버튼
        self.subject_label = tk.Label(root, text="과목을 추가하세요:")
        self.subject_entry = tk.Entry(root)
        self.add_subject_button = tk.Button(root, text="과목 추가", command=self.add_subject)

        # 두 번째 텍스트 입력 창과 버튼
        self.time_label = tk.Label(root, text="시간을 입력하세요:")
        self.time_entry = tk.Entry(root)
        self.add_time_button = tk.Button(root, text="입력", command=self.add_time)

        # 배치
        self.subject_label.grid(row=0, column=0, padx=10, pady=10)
        self.subject_entry.grid(row=0, column=1, padx=10, pady=10)
        self.add_subject_button.grid(row=0, column=2, padx=10, pady=10)

        self.time_label.grid(row=1, column=0, padx=10, pady=10)
        self.time_entry.grid(row=1, column=1, padx=10, pady=10)
        self.add_time_button.grid(row=1, column=2, padx=10, pady=10)

    def add_subject(self):
        subject = self.subject_entry.get()
        if subject:
          messagebox.showinfo("과목 추가", f"과목 추가: {subject}")
        else:
            messagebox.showwarning("경고", "과목을 입력하세요.")

    def add_time(self):
        time = self.time_entry.get()
        if time:
            messagebox.showinfo("시간 입력", f"시간 입력: {time}")
        else:
            messagebox.showwarning("경고", "시간을 입력하세요.")

if __name__ == "__main__":
    root = tk.Tk()
    app = GUIApp(root)
    root.mainloop()
