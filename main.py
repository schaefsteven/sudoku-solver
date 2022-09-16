from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget 
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty, ObjectProperty
from kivy.graphics import Line, Color, Rectangle

from sudoku import sudoku


class SudokuSolverApp(App):
    def build(self):
        return MainLayout()

class MainLayout(BoxLayout):
    """This is the parent layout of all the gui items"""
    cell_grid = ObjectProperty(None)

class CellGrid(GridLayout):
    """This is the actual sudoku board that is displayed to the user"""
    def __init__(self,  **kwargs):
        super().__init__(**kwargs)
        # Create the board object
        self.board = sudoku.Board()
        # Create all of the CellBox objects, one for each cell in self.board
        for cell in self.board.all_cells:
            self.add_widget(CellBox(cell))
        self.update()
        # Create 4 divider lines
        with self.canvas.after:
            self.dividers = []
            Color(0,0,.3,1)
            for i in range(4):
                self.dividers.append(Line(width = 4))
        # Call _update_dividers whenever CellGrid is resized
        self.bind(size = self._update_dividers)

    def _update_dividers(self, inst, value):
        """Called whenever CellGrid is resized, defines points of the divider 
        lines"""
        top = inst.y + inst.height
        bottom = inst.y
        right = inst.x + inst.width
        left = inst.x
        # Vertical lines
        for i, div in enumerate(self.dividers[:2], 1):
            x = left + ((i/3) * inst.width)
            div.points = [x, top, x, bottom]
        # Horizontal lines
        for i, div in enumerate(self.dividers[2:], 1):
            y = bottom + ((i/3) * inst.height)
            div.points = [left, y, right, y]

    def update(self):
        """Checks if cell objects have a value, if so, update the text of the 
        CellBox"""
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
    """This is the graphical representation of an individual cell"""
    text_property = StringProperty('')

    def __init__(self, cell, **kwargs):
        super().__init__(**kwargs)
        self.cell = cell
        self.text = self.text_property


if __name__ == "__main__": 
    SudokuSolverApp().run()

