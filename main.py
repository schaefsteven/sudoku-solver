from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget 
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
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
            self.add_widget(CellBox(cell))
        self.update()

    def update(self):
        for cell_box, cell in zip(self.children, self.board.all_cells):
            if cell.value:
                print(cell.value)
                cell_box.text = str(cell.value)

class CellBox(TextInput):

    text_property = StringProperty('')

    def __init__(self, cell, **kwargs):
        super().__init__(**kwargs)
        self.cell = cell
        self.text = self.text_property

if __name__ == "__main__": 
    MainApp().run()

