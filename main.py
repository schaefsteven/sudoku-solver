from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget 
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty

from sudoku import sudoku


def main():
    board = sudoku.Board("sample_boards/board0.csv")
    board.print()
    board.solve()
    board.check()
    board.print()
    return

class MainApp(App):
    def build(self):
        return MainLayout()

class MainLayout(BoxLayout):
    pass

class CellGrid(GridLayout):
    def __init__(self,  **kwargs):
        super().__init__(**kwargs)
        self.board = sudoku.Board("sample_boards/board0.csv")
        for cell in self.board.all_cells:
            if cell.value:
                text = StringProperty(str(cell.value))
                readonly = True
            else: 
                text = StringProperty('')
                readonly = False
            text_box = TextInput(text = text, 
                                 input_filter = 'int',
                                 readonly = readonly,
                                 halign = 'center',
                                 font_size = 30,
                                 )
            self.add_widget(text_box)

    def update(self):
        for text_box, cell in self.children, self.board.all_cells:
            if cell.value:
                text_box.text = cell.value

class CellBox(TextInput):
    def __init__(self, cell, **kwargs):
        super().__init__(**kwargs)
        self.cell = cell
        self.value = ''

if __name__ == "__main__": 
    MainApp().run()

