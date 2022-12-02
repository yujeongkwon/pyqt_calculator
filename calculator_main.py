import math
import sys
from PyQt5.QtWidgets import *

class Main(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        ### 각 위젯을 배치할 레이아웃을 미리 만들어 둠
        layout_button = QGridLayout()
        layout_lineEdit = QFormLayout()

        ### 수식 입력과 답 출력을 위한 LineEdit 생성
        self.lineEdit = QLineEdit("")
        self.equation=""

        ### layout_lineEdit 레이아웃에 LineEdit위젯을 추가
        layout_lineEdit.addRow(self.lineEdit)

        ### 사칙연산 버튼 생성
        button_plus = QPushButton("+")
        button_minus = QPushButton("-")
        button_product = QPushButton("x")
        button_division = QPushButton("÷")
        ### 추가 연산 버튼 생성
        button_rest = QPushButton("%")
        button_clearEntry = QPushButton("CE")
        button_clear = QPushButton("C")
        button_inverse = QPushButton("1/x")
        button_square = QPushButton("x²")
        button_squareRoot = QPushButton("²√x")

        ### 사칙연산 버튼을 클릭했을 때, 각 사칙연산 부호가 수식에 추가될 수 있도록 시그널 설정
        button_plus.clicked.connect(lambda state, operation = "+": self.button_operation_clicked(operation))
        button_minus.clicked.connect(lambda state, operation = "-": self.button_operation_clicked(operation))
        button_product.clicked.connect(lambda state, operation = "*": self.button_operation_clicked(operation))
        button_division.clicked.connect(lambda state, operation = "/": self.button_operation_clicked(operation))
        ### 추가 연산 버튼을 클릭했을 때, 각 추가연산 부호가 작동할수 있도록 시그널 설정
        button_rest.clicked.connect(lambda state, operation = "%": self.button_operation_clicked(operation))
        button_clearEntry.clicked.connect(self.button_clearEntry_clicked)
        button_inverse.clicked.connect(self.button_inverse_clicked)
        button_square.clicked.connect(self.button_square_clicked)
        button_squareRoot.clicked.connect(self.button_squareRoot_clicked)

        ### 사칙연산 버튼을 layout_button 레이아웃에 추가
        layout_button.addWidget(button_plus,4,3)
        layout_button.addWidget(button_minus,3,3)
        layout_button.addWidget(button_product,2,3)
        layout_button.addWidget(button_division,1,3)
        ### 추가연산 버튼을 layout_button 레이아웃에 추가
        layout_button.addWidget(button_rest, 0, 0)
        layout_button.addWidget(button_clearEntry, 0, 1)
        layout_button.addWidget(button_clear, 0, 2)
        layout_button.addWidget(button_inverse, 1, 0)
        layout_button.addWidget(button_square, 1, 1)
        layout_button.addWidget(button_squareRoot, 1, 2)

        ### =, clear, backspace 버튼 생성
        button_equal = QPushButton("=")
        button_backspace = QPushButton("Backspace")

        ### =, clear, backspace 버튼 클릭 시 시그널 설정
        button_equal.clicked.connect(self.button_equal_clicked)
        button_clear.clicked.connect(self.button_clear_clicked)
        button_backspace.clicked.connect(self.button_backspace_clicked)

        ### =, clear, backspace 버튼을 layout_button 레이아웃에 추가
        layout_button.addWidget(button_clear,0,2)
        layout_button.addWidget(button_backspace,0,3)
        layout_button.addWidget(button_equal,5,3)

        ### 숫자 버튼 생성하고, layout_button 레이아웃에 추가
        ### 각 숫자 버튼을 클릭했을 때, 숫자가 수식창에 입력 될 수 있도록 시그널 설정
        number_button_dict = {}
        for number in range(0, 10):
            number_button_dict[number] = QPushButton(str(number))
            number_button_dict[number].clicked.connect(lambda state, num = number:
                                                       self.number_button_clicked(num))
            if number >0:
                x,y = divmod(number-1, 3)
                layout_button.addWidget(number_button_dict[number], x+2, y)
            elif number==0:
                layout_button.addWidget(number_button_dict[number], 5, 1)

        ### 소숫점 버튼과 00 버튼을 입력하고 시그널 설정
        button_dot = QPushButton(".")
        button_dot.clicked.connect(lambda state, num = ".": self.number_button_clicked(num))
        layout_button.addWidget(button_dot, 5, 2)

        button_double_zero = QPushButton("00")
        button_double_zero.clicked.connect(lambda state, num = "00": self.number_button_clicked(num))
        layout_button.addWidget(button_double_zero, 5, 0)

        ### 각 레이아웃을 main_layout 레이아웃에 추가
        main_layout.addLayout(layout_lineEdit)
        main_layout.addLayout(layout_button)

        self.setLayout(main_layout)
        self.show()

    #################
    ### functions ###
    #################


    def number_button_clicked(self, num):
        self.equation += str(num)
        equation = self.lineEdit.text()
        equation += str(num)
        self.lineEdit.setText(equation)

    def button_operation_clicked(self, operation):
        equation = self.equation
        if equation[-1].isdigit():
            self.equation = str(calculator(equation))
            self.equation += operation
        else:
            self.equation = self.equation[:-1] + operation
        self.lineEdit.setText("")

    def button_equal_clicked(self):
        if self.equation[-1].isdigit():
            self.lineEdit.setText(str(calculator(self.equation)))
        else:
            self.lineEdit.setText("error")

    def button_clear_clicked(self):
        self.equation=""
        self.lineEdit.setText("")

    def button_clearEntry_clicked(self):
        equation = self.equation
        if not isOnlyNumeric(equation):
            index = search_operator(equation)
            self.equation = equation[:index+1]
        else:
            self.equation = ""
        self.lineEdit.setText("")

    def button_backspace_clicked(self):
        self.equation = self.equation[:-1]
        self.lineEdit.setText(self.lineEdit.text()[:-1])

    def button_inverse_clicked(self):
        equation = self.equation
        if not isOnlyNumeric(equation):
            index = search_operator(equation)
            self.equation = equation[:index+1] + str(1 / float(equation[index+1:]))
            equation = str(1 / float(equation[index+1:]))
        else:
            if len(equation) > 0:
                self.equation = str(1 / float(equation))
            else:
                self.equation = "0"
            equation = self.equation
        self.lineEdit.setText(equation)

    def button_square_clicked(self):
        equation = self.equation
        if not isOnlyNumeric(equation):
            index = search_operator(equation)
            self.equation = equation[:index+1] + str(math.pow(float(equation[index+1:]), 2))
            equation = str(math.pow(float(equation[index+1:]), 2))
        else:
            if len(equation) > 0:
                self.equation = str(math.pow(float(equation), 2))
            else:
                self.equation = "0"
            equation = self.equation
        self.lineEdit.setText(equation)

    def button_squareRoot_clicked(self):
        equation = self.equation
        if not isOnlyNumeric(equation):
            index = search_operator(equation)
            self.equation = equation[:index+1] + str(math.sqrt(float(equation[index+1:])))
            equation = str(math.sqrt(float(equation[index+1:])))
        else:
            if len(equation) > 0:
                self.equation = str(math.sqrt(float(equation)))
            else:
                self.equation = "0"
            equation = self.equation
        self.lineEdit.setText(equation)

def calculator(equation):
    if not isOnlyNumeric(equation):
        index = search_operator(equation)
        if equation[index] == '+':
            return float(equation[:index]) + float(equation[index+1:])
        if equation[index] == '-':
            return float(equation[:index]) - float(equation[index+1:])
        if equation[index] == '*':
            return float(equation[:index]) * float(equation[index+1:])
        if equation[index] == '/':
            return float(equation[:index]) / float(equation[index+1:])
        if equation[index] == '%':
            return float(equation[:index]) % float(equation[index+1:])
    return equation

def search_operator(equation):
    index = 0
    if equation[0] == '-':
        index = 1
    while equation[index].isdigit() or equation[index] == '.':
        index += 1
    return index

def isOnlyNumeric(equation):
    operator = ["+","-","*","/","%"]
    if equation[0] == '-':
        equation = equation[1:]

    for exp in operator:
        if exp in equation:
            return False
    return True

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())