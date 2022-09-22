# Set the default size of the application window
from kivy.config import Config
Config.set('graphics', 'width', '600')
Config.set('graphics', 'height', '660')

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.properties import StringProperty, ObjectProperty
from kivy.graphics import Line, Color

from sudoku import sudoku


class SudokuSolverApp(App):
    """Main application"""
    def build(self):
        return MainLayout()

class MainLayout(BoxLayout):
    """Parent layout of all the gui items"""
    # This layout is defined in the .kv file. 
    pass

class CellGrid(GridLayout):
    """Sudoku board that is displayed to the user"""
    def __init__(self, board=None ,**kwargs):
        super().__init__(**kwargs)
        # Create the board object
        self.board = sudoku.Board(board)
        # Create all of the CellBox objects, one for each cell in self.board
        for cell in self.board.all_cells:
            self.add_widget(CellBoxWrapper(cell))
        # If board was passed, we need to update the CellBoxes to show those
        # values
        self.update(False)

        # Create 4 divider lines. No points specified because they will be 
        # updated by self._update_dividers
        with self.canvas.after:
            self.dividers = []
            Color(0,0,.3,1)
            for i in range(4):
                self.dividers.append(Line(width = 4, cap = 'none'))
        # Call self._update_dividers whenever CellGrid is resized
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

    def update(self, show_poss = True):
        """Checks if cell objects have a value, if so, update the text of the 
        CellBox"""
        for cell_box in self.children:
            if cell_box.cell.value:
                cell_box.text = str(cell_box.cell.value)
                cell_box.children[0].text = ''
            else:
                if show_poss:
                    cell_box.children[0].text = str(cell_box.cell.possibilities)

    def on_solve_click(self):
        for cell_box in self.children:
            value = self._sanitize(cell_box.text)
            cell_box.cell.set_value(value)
            if not value:
                cell_box.cell.reset()
        self.board.print()
        self.board.solve()
        self.board.check()
        self.update()

    def on_reset_click(self):
        for cell in self.children:
            cell.cell.reset()
            cell.text = ''
            cell.children[0].text = ''

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

class CellBoxWrapper(RelativeLayout):
    """This is a wrapper for the CellBox and the possibilities label"""
    possibilities_property = StringProperty('')

    def __init__(self, cell, **kwargs):
        super().__init__(**kwargs)
        self.cell_box = CellBox(cell)
        self.add_widget(self.cell_box)
        self.cell = self.cell_box.cell
        self.text = self.cell_box.text
        self.possibilities = self.possibilities_property
        self.add_widget(Label(text = self.possibilities, 
                              color = [0,0,0,.8],
                              text_size = self.size,
                              halign = 'center',
                              valign = 'middle',
                              padding = [15, 15]
                              ))

    @property
    def cell(self):
        return self.cell_box.cell

    @cell.setter
    def cell(self, value):
        self.cell_box.cell = value

    @property
    def text(self):
        return self.cell_box.text

    @text.setter
    def text(self, value):
        self.cell_box.text = value


if __name__ == "__main__": 
    SudokuSolverApp().run()

