import tkinter as Tk


class PythonCalculator:
    def __init__(self) -> None:
        # create window
        self.__window = Tk.Tk()
        self.__window.grid()
        self.__window.rowconfigure(0, weight=1)
        self.__window.columnconfigure(0, weight=1)

        # frame
        self.__main_frame = Tk.Frame(self.__window)
        self.__main_frame.grid(row=0, column=0, sticky=Tk.NSEW)
        self.__main_frame.rowconfigure(0, weight=0)
        self.__main_frame.columnconfigure(0, weight=1)

        # store
        self.__digit_display_store = Tk.StringVar(self.__window, "")
        self.__label_store = Tk.StringVar(self.__window, "")

        # memory array
        self.memory_array = []

        # current operator
        self.current_operator = None

    def get_digit_display(self):
        return self.__digit_display_store.get()

    def set_digit_display(self, value):
        self.__digit_display_store.set(value)

    def set_label(self, value):
        self.__label_store.set(value)

    def add_digit(self, value):
        store = self.get_digit_display()
        if "ERROR" in store:
            self.set_digit_display("")
            store = self.get_digit_display()
        if value == "." and ("." in store):
            return
        self.set_digit_display(f"{store}{value}")

    def str_to_number(value: str):
        # convert to int or float
        if value.isdigit():
            return int(value)
        return float(value)

    def push_digit_to_memory(self):
        # get digit
        store = self.get_digit_display()

        # convert to number first
        num = PythonCalculator.str_to_number(store)

        # push number to memory array
        self.memory_array.append(num)

    def do_calculation(self):
        if self.memory_array[0] == None or self.memory_array[0] == None:
            return None
        if self.current_operator == "+":
            return self.memory_array[0] + self.memory_array[1]
        if self.current_operator == "-":
            return self.memory_array[0] - self.memory_array[1]
        if self.current_operator == "*":
            return self.memory_array[0] * self.memory_array[1]
        if self.current_operator == "/":
            try:
                return self.memory_array[0] / self.memory_array[1]
            except ZeroDivisionError:
                self.set_digit_display("ERROR")

    def press_operator(self, operator):
        # if digit display not clear push it
        if self.get_digit_display() != "":
            self.push_digit_to_memory()

        # if memory length greater than 2 press equal
        if len(self.memory_array) >= 2:
            self.press_equal()
            self.memory_array.clear()
            self.push_digit_to_memory()

        # set current operator
        self.current_operator = operator

        # update label
        if len(self.memory_array) >= 2:
            self.set_label(
                f"{self.memory_array[0]}{self.current_operator}{self.memory_array[1]}"
            )
        else:
            self.set_label(f"{self.memory_array[0]}{self.current_operator}")

        # clear digit display
        self.set_digit_display("")

    def press_clear(self):
        self.set_digit_display("")
        self.set_label("")
        self.memory_array.clear()

    def press_equal(self):
        # if digit & memory[0] & memory[1] & current_operator is not null
        # keep calculation
        if (
            self.get_digit_display() != ""
            and (len(self.memory_array) >= 2)
            and (self.current_operator != None)
        ):
            self.memory_array[0] = PythonCalculator.str_to_number(
                self.get_digit_display()
            )

        # if digit not empty then push digit to memory array first
        elif self.get_digit_display() != "":
            self.push_digit_to_memory()

        # do calculation
        result = self.do_calculation()

        if result == None:
            return

        # update digit display
        self.set_digit_display(result)

        # update label
        self.set_label(
            f"{self.memory_array[0]}{self.current_operator}{self.memory_array[1]}"
        )

    def press_backspace(self):
        # get digit
        digit = self.get_digit_display()

        # check length of string
        if len(digit) <= 0:
            return

        # remove last character of string and update
        self.set_digit_display(digit[:-1])

    def draw_gui(self):
        # draw label
        self.__label = Tk.Label(
            self.__main_frame,
            textvariable=self.__label_store,
            justify=Tk.RIGHT,
            font=("Arial", 20),
        )
        self.__label.grid(row=0, column=0, columnspan=4, sticky=Tk.NE)

        # draw digit display
        self.__digit_display = Tk.Entry(
            self.__main_frame,
            textvariable=self.__digit_display_store,
            justify=Tk.RIGHT,
            font=("Arial", 20),
        )
        self.__digit_display.grid(row=1, column=0, columnspan=4, sticky=Tk.NSEW)

        # draw numpad
        col = 0
        row = 2

        for i in range(1, 10):
            if col == 3:
                col = 0
                row += 1

            button = Tk.Button(
                self.__main_frame,
                text=f"{i}",
                command=lambda x=i: self.add_digit(x),
            )
            button.grid(row=row, column=col, sticky=Tk.NSEW)
            button.config(font=20, width=5, height=2)
            self.__main_frame.columnconfigure(col, weight=1)

            col += 1

        # draw operator
        operators = ("+", "-", "*", "/")

        for i, op in enumerate(operators):
            button = Tk.Button(
                self.__main_frame,
                text=f"{op}",
                command=lambda x=op: self.press_operator(x),
            )
            button.grid(row=i + 2, column=3, sticky=Tk.NSEW)
            button.config(font=20, width=5, height=2)
            self.__main_frame.columnconfigure(3, weight=1)

        # draw numpad 0
        button = Tk.Button(
            self.__main_frame, text="0", command=lambda x=0: self.add_digit(x)
        )
        button.grid(row=5, column=1, sticky=Tk.NSEW)
        button.config(font=20, width=5, height=2)
        self.__main_frame.columnconfigure(0, weight=1)

        # draw dot button
        button = Tk.Button(
            self.__main_frame,
            text=".",
            command=lambda x=".": self.add_digit(x),
        )
        button.grid(row=5, column=0, sticky=Tk.NSEW)
        button.config(font=20, width=5, height=2)
        self.__main_frame.columnconfigure(1, weight=1)

        # draw equal button
        button = Tk.Button(
            self.__main_frame,
            text="=",
            command=self.press_equal,
        )
        button.grid(row=5, column=2, sticky=Tk.NSEW)
        button.config(font=(5), width=5, height=2)
        self.__main_frame.columnconfigure(2, weight=1)

        # draw clear button
        button = Tk.Button(
            self.__main_frame,
            text="CLEAR",
            command=self.press_clear,
        )
        button.grid(row=6, column=0, columnspan=3, sticky=Tk.NSEW)
        button.config(font=(5), width=5, height=2)
        self.__main_frame.columnconfigure(2, weight=1)

        # draw backspace button
        button = Tk.Button(
            self.__main_frame,
            text="⌫",
            command=self.press_backspace,
        )
        button.grid(row=6, column=3, columnspan=1, sticky=Tk.NSEW)
        button.config(font=(5), width=5, height=2)
        self.__main_frame.columnconfigure(2, weight=1)

    def main(self):
        self.draw_gui()
        self.__window.title("Python Calculator")
        self.__window.geometry("300x330")
        self.__window.resizable(width=False, height=False)
        self.__window.mainloop()


if __name__ == "__main__":
    program = PythonCalculator()
    program.main()
