from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget 
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty, ObjectProperty

from sudoku import sudoku


class MainApp(App):
    def build(self):
        return MainLayout()

class MainLayout(BoxLayout):
    cell_grid = ObjectProperty(None)

class CellGrid(GridLayout):
    def __init__(self,  **kwargs):
        super().__init__(**kwargs)
        self.board = sudoku.Board()
        for cell in self.board.all_cells:
            self.add_widget(CellBox(cell))
        self.update()

    def update(self):
        for cell_box in self.children:
            if cell_box.cell.value:
                cell_box.text = str(cell_box.cell.value)

    def on_solve_click(self):
        for cell_box in self.children:
            value = self._sanitize(cell_box.text)
            cell_box.cell.set_value(value)
            if not value:
                cell_box.cell.possibilities = [1,2,3,4,5,6,7,8,9]
        self.board.print()
        self.board.solve()
        self.board.print()
        self.board.check()
        self.update()

    def _sanitize(self, input):
        try:
            input = int(input)
        except:
            return None
        if 0 < input < 10:
            return input
        else:
            return None

class CellBox(TextInput):
    text_property = StringProperty('')

    def __init__(self, cell, **kwargs):
        super().__init__(**kwargs)
        self.cell = cell
        self.text = self.text_property

    # def on_text_validate(self):
        # self.cell.value = int(self.text)

if __name__ == "__main__": 
    MainApp().run()

