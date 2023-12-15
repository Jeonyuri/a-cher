import tkinter as tk
from tkinter import messagebox
import random

class TimetableEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("시간표 편집기")

        self.days = ["월", "화", "수", "목", "금", "토", "일"]
        self.times = ["1교시", "2교시", "3교시", "4교시", "5교시", "6교시"]

        self.subjects = []
        self.blocks = {}

        self.create_table()

        # 과목 추가 관련 GUI 요소
        self.subject_entry = tk.Entry(root)
        self.add_subject_button = tk.Button(root, text="과목 추가", command=self.add_subject)

        self.subject_entry.grid(row=8, column=0, padx=10, pady=10, columnspan=7)
        self.add_subject_button.grid(row=9, column=0, padx=10, pady=10, columnspan=7)

        # 드래그 앤 드롭 관련 변수
        self.drag_data = {"subject": "", "start_row": 0, "start_col": 0}

    def create_table(self):
        for i, day in enumerate(self.days):
            tk.Label(self.root, text=day, width=8, height=2, relief="solid").grid(row=0, column=i+1)

        for i, time in enumerate(self.times):
            tk.Label(self.root, text=time, width=8, height=2, relief="solid").grid(row=i+1, column=0)

        for i in range(6):
            for j in range(7):
                block = tk.Label(self.root, text="", width=8, height=2, relief="solid")
                block.grid(row=i+1, column=j+1)
                block.bind("<Button-1>", lambda event, row=i, col=j: self.start_drag(event, row, col))
                block.bind("<B1-Motion>", lambda event, row=i, col=j: self.drag_to(event, row, col))
                block.bind("<ButtonRelease-1>", lambda event, row=i, col=j: self.stop_drag(event, row, col))
                block.bind("<Button-3>", lambda event, row=i, col=j: self.remove_block(event, row, col))
                self.blocks[(i, j)] = block

        # 일요일 표시
        tk.Label(self.root, text="일", width=8, height=2, relief="solid").grid(row=0, column=7)

    def add_subject(self):
        subject_name = self.subject_entry.get().strip()
        if not subject_name:
            messagebox.showwarning("경고", "과목명을 입력하세요.")
            return

        self.subjects.append(subject_name)

        # 빈 블록에 추가
        for i, j in sorted(self.blocks.keys()):
            if self.blocks[(i, j)].cget("text") == "":
                self.blocks[(i, j)].config(text=subject_name)
                break
        else:
            messagebox.showwarning("경고", "더 이상 과목을 추가할 수 없습니다.")

    def start_drag(self, event, row, col):
        if self.blocks[(row, col)].cget("text") != "":
            self.drag_data["subject"] = self.blocks[(row, col)].cget("text")
            self.drag_data["start_row"] = row
            self.drag_data["start_col"] = col

    def drag_to(self, event, row, col):
        if self.drag_data["subject"]:
            self.blocks[(row, col)].config(text=self.drag_data["subject"])

    def stop_drag(self, event, row, col):
        if self.drag_data["subject"]:
            self.blocks[(self.drag_data["start_row"], self.drag_data["start_col"])].config(text="")
            self.drag_data["subject"] = ""

    def remove_block(self, event, row, col):
        if self.blocks[(row, col)].cget("text") != "":
            self.blocks[(row, col)].config(text="")
            self.drag_data["subject"] = ""

if __name__ == "__main__":
    root = tk.Tk()
    app = TimetableEditor(root)
    root.mainloop()
