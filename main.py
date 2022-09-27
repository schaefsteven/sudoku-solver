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
from kivy.uix.popup import Popup
from kivy.uix.button import Button
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
            self.add_widget(CellBox(cell))
        # If board was passed, we need to update the CellBoxes to show those
        # values
        self._update_grid(False)
        # Create 4 divider lines. No points specified because they will be 
        # updated by self._update_dividers
        with self.canvas.after:
            self.dividers = []
            Color(0,0,0,1)
            for i in range(4):
                self.dividers.append(Line(width = 4, cap = 'none'))
        # Call self._update_dividers whenever CellGrid is resized
        self.bind(size = self._update_dividers)

    def _update_dividers(self, inst, value):
        """Called whenever CellGrid is resized, defines points of the divider 
        lines
        """
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

    def _update_grid(self, show_poss = True):
        """Checks if cell objects have a value, if so, update the text of the 
        CellBox
        """
        for cell_box in self.children:
            # If the cell has a value, display it
            if cell_box.cell.value:
                cell_box.text = str(cell_box.cell.value)
                cell_box.poss_disp.text = ''
            else:
                cell_box.text = ''
                if show_poss:
                    cell_box.poss_disp.text = str(cell_box.cell.possibilities)

    def on_solve_click(self):
        """Processes user inputs and calls the solve method on the puzzle"""
        # Take the values entered by the user into the TextInputs and put them
        # in the actual cell objects
        for cell_box in self.children:
            value = self._sanitize(cell_box.text)
            cell_box.cell.set_value(value)
            # This accounts for cells out of which the value was deleted by user
            if not value:
                cell_box.cell.reset()
        solved = self.board.solve()
        self._update_grid()
        if not solved:
            layout = BoxLayout(orientation = "vertical")
            layout.add_widget(Label(text = "Could not solve board."))
            button = Button(text = "Okay",
                            size_hint = (.3, .5),
                            pos_hint = {"center_x": .5}
                            )
            layout.add_widget(button)
            popup = Popup(title = "Error", 
                          content = layout,
                          size_hint = (.5, .3),
                          )
            button.bind(on_press = popup.dismiss)
            popup.open()

    def on_reset_click(self):
        """Clears all of the values from the display and resets the board 
        object 
        """
        for cell in self.children:
            cell.cell.reset()
            cell.text = ''
            cell.poss_disp.text = ''

    def _sanitize(self, input):
        """Sanitizes user input from the sudoku board grid"""
        # Cut off all but the first char of the input
        if input:
            input = input[0]
        # If possible, convert to int
        try:
            input = int(input)
        except:
            return None
        # Don't accept zeros
        if 0 < input < 10:
            return input
        else:
            return None

class CellBox(RelativeLayout):
    """This is a wrapper for the CellBoxText and the possibilities overlay 
    label
    """
    possibilities_property = StringProperty('')

    def __init__(self, cell, **kwargs):
        super().__init__(**kwargs)
        # TextInput widget that displays the value and takes input
        self.text_input = CellBoxText(cell)
        self.add_widget(self.text_input)
        # Label widget to display the possibilities if the value is unknown. 
        # This object is not used in the current implementation.
        self.possibilities = self.possibilities_property
        self.poss_disp = (Label(text = self.possibilities, 
                              color = [0,0,0,.8],
                              text_size = self.size,
                              halign = 'center',
                              valign = 'middle',
                              padding = [15, 15]
                              ))
        # This line is commented out to disable the poss_disp overlay.
        # self.add_widget(self.poss_disp)

    # Point references to cell and text into the TextInput child object
    @property
    def cell(self):
        return self.text_input.cell
    @cell.setter
    def cell(self, value):
        self.text_input.cell = value

    @property
    def text(self):
        return self.text_input.text
    @text.setter
    def text(self, value):
        self.text_input.text = value

class CellBoxText(TextInput):
    """Text Input and display for the cell's value"""
    text_property = StringProperty('')

    def __init__(self, cell, **kwargs):
        super().__init__(**kwargs)
        self.cell = cell
        self.text = self.text_property


if __name__ == "__main__": 
    SudokuSolverApp().run()

