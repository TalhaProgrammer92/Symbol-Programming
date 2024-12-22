##############################
# Importing - Modules
##############################
import tkinter as tk
import tkinter.messagebox as tmsg
import tkinter.filedialog as tfdg
import os
# import tkinter.font as font

##############################
# Global - Variables
##############################
LEGALS: str = '+-*/&|~^<>(){}[]_!@.'

##############################
# Cell - Class
##############################
class Cell:
    def __init__(self):
        self.__value: int = 0

    ##############
    # Getters
    ##############
    @property
    def value(self) -> int:
        return self.__value

    ##############
    # Methods
    ##############
    def increment(self) -> None:
        """ To increase cell's value by 1 """
        self.__value += 1 if self.value < 127 else 0

    def decrement(self) -> None:
        """ To decrease cell's value by 1 """
        self.__value -= 1 if self.value > 0 else 0

    def double(self) -> None:
        """ To double the cell's value """
        self.__value *= 2 if self.value * 2 <= 127 else 1

    def half(self) -> None:
        """ To half the cell's value """
        self.__value = int(self.__value / 2 if int(self.value * 2) >= 0 else 1)

    def bitwise_and(self, value: int) -> None:
        """ Perform bitwise AND operation """
        self.__value = self.__value & value

    def bitwise_or(self, value: int) -> None:
        """ Perform bitwise OR operation """
        self.__value = self.__value | value

    def bitwise_not(self) -> None:
        """ Perform bitwise NOT operation """
        self.__value = ~self.__value

    def bitwise_xor(self, value: int) -> None:
        """ Perform bitwise XOR operation """
        self.__value = self.__value ^ value

    def output(self) -> None:
        """ To display ASCII character of the value """
        print(chr(self.value), end='')

    def reset(self) -> None:
        """ To reset the value """
        self.__value = 0


##############################
# Stack - Class
##############################
class Stack:
    def __init__(self):
        self.cells: list[Cell] = []
        self.__limit: int = 8
        self.__pointer: int = 0

        for count in range(self.__limit):
            cell = Cell()
            self.cells.append(cell)

    ##############
    # Getters
    ##############
    @property
    def pointer(self):
        return self.__pointer

    ######################
    # Methods - Stack
    ######################
    def to_next(self) -> None:
        """ Goto next cell in the stack """
        self.__pointer += 1 if self.__pointer < self.__limit - 1 else 0

    def to_previous(self) -> None:
        """ Goto previous cell in the stack """
        self.__pointer -= 1 if self.__pointer > 0 else 0

    def jump_start(self) -> None:
        """ Goto to first cell in the stack """
        self.__pointer = 0

    def jump_end(self) -> None:
        """ Goto to last cell in the stack """
        self.__pointer = self.__limit - 1

    def reset(self) -> None:
        """ To reset values of all cells in the stack """
        for cell in self.cells:
            cell.reset()
        self.__pointer = 0


##############################
# Memory - Class
##############################
class Memory:
    def __init__(self):
        self.stacks: list[Stack] = []
        self.__limit: int = 16
        self.__pointer: int = 0
        self.add()

    ##############
    # Getters
    ##############
    @property
    def pointer(self):
        return self.__pointer

    ######################
    # Methods - Memory
    ######################
    def add(self) -> None:
        """ To add a Stack in the memory """
        if len(self.stacks) < self.__limit - 1:
            stack = Stack()
            self.stacks.append(stack)

    def to_next(self) -> None:
        """ Goto next cell in the memory """
        self.__pointer += 1 if self.__pointer < len(self.stacks) - 1 else 0

    def to_previous(self) -> None:
        """ Goto previous cell in the memory """
        self.__pointer -= 1 if self.__pointer > 0 else 0

    def jump_start(self) -> None:
        """ Goto first cell in the memory """
        self.__pointer = 0

    def jump_end(self) -> None:
        """ Goto last cell in the memory """
        self.__pointer = len(self.stacks) - 1


##############################
# Token - Class
##############################
class Token:
    def __init__(self, symbol: str):
        self.__symbol: str = symbol
        self.__is_valid: bool = self.__validity()

    ##############
    # Methods
    ##############
    def __validity(self) -> bool:
        if self.__symbol in LEGALS:
            return True
        return False

    ##############
    # Getters
    ##############
    @property
    def symbol(self) -> str:
        return self.__symbol

    @property
    def is_valid(self) -> int:
        return self.__is_valid


##############################
# Program - Class
##############################
class Program:
    def __init__(self):
        self.__source_code: str = ''
        self.__tokens: list[Token] = []
        self.__stacks: Memory = Memory()

    ##############
    # Methods
    ##############
    def write(self, source_code: str) -> None:
        """ To write program """
        self.__source_code = source_code

    def load(self) -> None:
        """ To load the program written """
        if len(self.__source_code) > 0:
            self.__tokens = []
            for character in self.__source_code:
                token: Token = Token(character)
                if token.is_valid:
                    self.__tokens.append(token)
                    if token.symbol == '.':
                        break
        else:
            tmsg.showerror('Error', 'Empty code space')

    def execute(self) -> None:
        """ To execute the program loaded """
        if len(self.__tokens) > 0:
            for token in self.__tokens:
                stack_pointer: int = self.__stacks.pointer
                cell_pointer: int = self.__stacks.stacks[stack_pointer].pointer
                match token.symbol:
                    #################
                    # Operators
                    #################
                    case '+':
                        self.__stacks.stacks[stack_pointer].cells[cell_pointer].increment()
                    case '-':
                        self.__stacks.stacks[stack_pointer].cells[cell_pointer].decrement()
                    case '*':
                        self.__stacks.stacks[stack_pointer].cells[cell_pointer].double()
                    case '/':
                        self.__stacks.stacks[stack_pointer].cells[cell_pointer].half()
                    case '&':
                        value: int = self.__stacks.stacks[stack_pointer].cells[cell_pointer + 1].value if cell_pointer < 7 else self.__stacks.stacks[stack_pointer].cells[cell_pointer - 1].value
                        self.__stacks.stacks[stack_pointer].cells[cell_pointer].bitwise_and(value)
                    case '|':
                        value: int = self.__stacks.stacks[stack_pointer].cells[cell_pointer + 1].value if cell_pointer < 7 else self.__stacks.stacks[stack_pointer].cells[cell_pointer - 1].value
                        self.__stacks.stacks[stack_pointer].cells[cell_pointer].bitwise_or(value)
                    case '~':
                        self.__stacks.stacks[stack_pointer].cells[cell_pointer].bitwise_not()
                    case '^':
                        value: int = self.__stacks.stacks[stack_pointer].cells[cell_pointer + 1].value if cell_pointer < 7 else self.__stacks.stacks[stack_pointer].cells[cell_pointer - 1].value
                        self.__stacks.stacks[stack_pointer].cells[cell_pointer].bitwise_xor(value)

                    #################
                    # Navigation
                    #################
                    case '<':
                        self.__stacks.stacks[stack_pointer].to_previous()
                    case '>':
                        self.__stacks.stacks[stack_pointer].to_next()
                    case '(':
                        self.__stacks.stacks[stack_pointer].jump_start()
                    case ')':
                        self.__stacks.stacks[stack_pointer].jump_end()
                    case '{':
                        self.__stacks.to_previous()
                    case '}':
                        self.__stacks.to_next()
                    case '[':
                        self.__stacks.jump_start()
                    case ']':
                        self.__stacks.jump_end()

                    #################
                    # Advance
                    #################
                    case '@':
                        self.__stacks.stacks[stack_pointer].cells[cell_pointer].output()
                    case '_':
                        self.__stacks.add()
                    case '!':
                        self.__stacks.stacks[stack_pointer].reset()
        else:
            tmsg.showerror('Error', 'You must compile the program first.')

    def extract(self) -> None:
        """ To save the program in text file """
        if len(self.__tokens) > 0:
            print()
            for token in self.__tokens:
                print(token.symbol, end='')
            print()
        else:
            tmsg.showerror('Error', 'You must compile the program first.')

    def clear(self) -> None:
        """ To clear the source code """
        self.__source_code: str = ''
        self.__tokens: list[Token] = []
        self.__stacks: Memory = Memory()


##############################
# Code Editor - Class
##############################
class Editor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.__source_code: Program = Program()

        self.geometry('800x600')
        self.minsize(640, 400)
        self.maxsize(1024, 600)
        self.title('Untitled - Symbol')
        if os.path.exists('symbols.ico'):
            self.wm_iconbitmap('symbols.ico')

        self.__code_area: tk.Text = tk.Text(self, font=('Cascadia Code', 12))    # The code written in Code Editor
        self.__source_file = None  # The file currently working on

    #############################
    # Methods - Menu Actions
    #############################
    def __new_file(self) -> None:
        """ Opens a new blank file """
        self.title('Untitled - Symbol')
        self.__source_file = None
        self.__code_area.delete('1.0', tk.END)

    def __open_file(self) -> None:
        """ Opens an existing file """
        # self.__source_file = tfdg.askopenfilename(defaultextension='.txt', filetypes=[('Text Documents', '*.txt')])
        self.__source_file = tfdg.askopenfilename(defaultextension='.txt', filetypes=[('Text Documents', '*.sym')])

        if self.__source_file == '':
            self.__source_file = None

        else:
            self.title(os.path.basename(self.__source_file[:-4]) + ' - Symbol')
            self.__code_area.delete('1.0', tk.END)

            with open(self.__source_file, 'r') as file:
                self.__code_area.delete('1.0', tk.END)
                self.__code_area.insert('1.0', file.read())

    def __save_file(self) -> None:
        """ Saves an opened file """
        if self.__source_file is None:
            # self.__source_file = tfdg.asksaveasfilename(initialfile='.txt', defaultextension='.txt', filetypes=[('Text Documents', '*.txt')])
            self.__source_file = tfdg.asksaveasfilename(initialfile='.sym', defaultextension='.sym', filetypes=[('Text Documents', '*.sym')])

            if self.__source_file == '':
                self.__source_file = None
                return None

        with open(self.__source_file, 'w') as file:
            file.write(self.__code_area.get('1.0', tk.END))

        self.title(os.path.basename(self.__source_file[:self.__source_file.index('.')]) + ' - Symbol')

    def __quit_editor(self) -> None:
        """ To quit the Code Editor """
        option = tmsg.askyesno('Exit', 'Are you sure you want to quit?')

        if option:
            self.destroy()

    def __copy_text(self) -> None:
        """ To copy highlighted text """
        self.__code_area.event_generate('<<Copy>>')

    def __cut_text(self) -> None:
        """ To cut highlighted text """
        self.__code_area.event_generate('<<Cut>>')

    def __paste_text(self) -> None:
        """ To paste text from clipboard to cursor position """
        self.__code_area.event_generate('<<Paste>>')

    def __find(self) -> None:
        """ To find specific text """
        pass

    def __replace(self) -> None:
        """ To replace specific text """
        pass

    def __compile_code(self) -> None:
        """ To compile the written code """
        self.__source_code.write(self.__code_area.get('1.0', tk.END))
        tmsg.showinfo('Compiled', 'The program has been compiled successfully')
        self.__source_code.load()
        # print(self.__code_area.get('1.0', tk.END))

    def __run_code(self) -> None:
        """ To run the compiled code """
        # os.system('cls')            # For Mac/Linux os.system('clear')
        self.__source_code.execute()
        self.__source_code.clear()

    def __extract_code(self) -> None:
        """ To debug the code """
        self.__source_code.extract()

    def __open_guide(self) -> None:
        """ To open a helping guide to guide the programmer to program in this language """
        guide = """+ is used to increment the value of current stack's cell by 1

- is used to decrement the value of current stack's cell by 1

* is used to double the value of current stack's cell

/ is used to half the value of current stack's cell

& is used to perform bitwise AND on the value of current
stack's cell with the value in right side stack's cell

| is used to perform bitwise OR on the value of current
stack's cell with the value of right side stack's cell

~ is used to perform bitwise NOT on the value of current
stack's cell with the value of right side stack's cell

^ is used to perform bitwise XOR on the value of current
stack's cell with the value of right side stack's cell

> is used to goto the next cell of current stack

< is used to goto the previous cell of current stack

( is used to goto the first cell of current stack

) is used to goto the lest cell of current stack

} is used to goto the next stack of memory

{ is used to goto the previous stack of memory

[ is used to goto the first stack of memory

] is used to goto the last stack of memory

@ is used to display ASCII value of current stack's cell

_ is used to add a new stack a new stack in memory

! is used to reset current stack in memory

. is used to terminate the current program"""
        tmsg.showinfo('Guide', guide)

    def __ascii_table(self) -> None:
        """ To open an ASCII convertor to convert and see ASCII codes """
        if os.path.exists('ascii.png'):
            os.startfile('ascii.png')
        else:
            tmsg.showerror('Error', 'The file \'ascii.png\' does not exist in current path. Please make sure you have the same file.')

    def __about(self) -> None:
        """ To open about page """
        tmsg.showinfo('About', 'Symbol (Esolang) IDE created by Talha Ahmad\nDated: December 2024 CE\nAll Rights are Reserved (c)')

    #############################
    # Methods - Appearance
    #############################
    def __set_menu_bar(self) -> None:
        """ Create menu bar """
        menu_bar: tk.Menu = tk.Menu(self)

        # File - Menu
        file_menu: tk.Menu = tk.Menu(menu_bar, tearoff=0)

        file_menu.add_command(label='New', command=self.__new_file)
        file_menu.add_command(label='Open', command=self.__open_file)
        file_menu.add_command(label='Save', command=self.__save_file)
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=self.__quit_editor)

        menu_bar.add_cascade(label='File', menu=file_menu)

        # Edit - Menu
        edit_menu: tk.Menu = tk.Menu(menu_bar, tearoff=0)

        edit_menu.add_command(label='Copy   Ctrl+C', command=self.__copy_text)
        edit_menu.add_command(label='Cut    Ctrl+X', command=self.__cut_text)
        edit_menu.add_command(label='Paste  Ctrl+V', command=self.__paste_text)
        edit_menu.add_separator()
        edit_menu.add_command(label='Find', command=self.__find)
        edit_menu.add_command(label='Replace', command=self.__replace)

        menu_bar.add_cascade(label='Edit', menu=edit_menu)

        # Code - Menu
        code_menu: tk.Menu = tk.Menu(menu_bar, tearoff=0)

        code_menu.add_command(label='Compile', command=self.__compile_code)
        code_menu.add_command(label='Run', command=self.__run_code)
        code_menu.add_separator()
        code_menu.add_command(label='Extract Symbols', command=self.__extract_code)

        menu_bar.add_cascade(label='Code', menu=code_menu)

        # Help - Menu
        help_menu: tk.Menu = tk.Menu(menu_bar, tearoff=0)

        help_menu.add_command(label='Guide', command=self.__open_guide)
        help_menu.add_command(label='ASCII Table', command=self.__ascii_table)
        help_menu.add_separator()
        help_menu.add_command(label='About', command=self.__about)

        menu_bar.add_cascade(label='Help', menu=help_menu)

        self.config(menu=menu_bar)

    def __set_scroll_bar(self) -> None:
        """ Create vertical scroll bar """
        scroll_bar: tk.Scrollbar = tk.Scrollbar(self)
        scroll_bar.pack(side='right', fill='y')
        scroll_bar.config(command=self.__code_area.yview)
        self.__code_area.config(yscrollcommand=scroll_bar.set)

    def open(self):
        """ Open the GUI of Code Editor """
        self.__code_area.pack(fill='both', expand=True, side='left')    # Set code area
        self.__set_menu_bar()                                           # Set Menu bar
        self.__set_scroll_bar()                                         # Set scroll bar


if __name__ == '__main__':
    """
    72 : H      | 0 -> 72 = 8 * 9 = 2^6 + 8         | +******++++++++@
    101 : e     | 0 -> 101 = 100 + 1 = 3^5 + 5      | +++*****+++++@
    108 : l     | 0 -> 108 = 100 + 8 = 3^5 + 12     | +++*****++++++++++++@
    111 : o     | 0 -> 111 = 100 + 11 = 3^5 + 15    | +++*****+++++++++++++++@
    32 :        | 0 -> 32 = 2^5                     | +*****@
    87 : W      | 0 -> 87 = 96 - 9 = 3^5 - 9        | +++*****---------@
    114 : r     | 0 -> 114 = 100 + 14 = 3^5 + 18    | +++*****++++++++++++++++++@
    100 : d     | 0 -> 100 = 3^5 + 4                | +++*****++++@
    
    Sample Code: +******++++++++@>+++*****+++++@>+++*****++++++++++++@@>+++*****+++++++++++++++@>+*****@>+++*****---------@<<@>>>+++*****++++++++++++++++++@<<<<@>>>>>>+++*****++++@.
    """

    IDE = Editor()
    IDE.open()
    IDE.mainloop()
