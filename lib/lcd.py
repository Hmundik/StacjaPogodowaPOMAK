import upm.pyupm_jhd1313m1 as upmjhd
import sys, mraa

# sphinx autoapi required
__all__ = [
    "Display",
    "TYPE_CHAR",
    "TYPE_GRAY",
    "TYPE_COLOR",
    "MAX_GRAY"
]

TYPE_CHAR  = 0
TYPE_GRAY  = 1
TYPE_COLOR = 2

MAX_GRAY = 100

class Display(object):
    '''
    All display devices should inherit this virtual class,
    which provide infrastructure such as cursor and backlight inteface, etc.
    '''
    def __init__(self):
        self._cursor = False
        self._backlight = False

    # To be derived
    def _cursor_on(self, en):
        pass

    def cursor(self, enable = None):
        '''
        Enable or disable the backlight on display device,
        not all device support it.

        Args:
            enable (bool): Optional, ``True`` to enable, ``Flase`` to disable.
                           if not provided, only to get cursor status.

        Returns:
            bool: cursor status, ``True`` - on, ``False`` - off.
        '''
        if type(enable) == bool:
            self._cursor = enable
            self._cursor_on(enable)
        return self._cursor

    # To be derived
    def _backlight_on(self, en):
        pass

    def backlight(self, enable = None):
        '''
        Enable or disable the cursor on display device,
        not all device support it.

        Args:
            enable (bool): Optional, ``True`` to enable, ``Flase`` to disable.
                           if not provided, only to get cursor status.

        Returns:
            bool: backlight status, ``True`` - on, ``False`` - off.
        '''
        if type(enable) == bool:
            self._backlight = enable
            self._backlight_on(enable)
        return self._backlight



__all__ = ["JHD1802"]

class JHD1802(Display):
    def __init__(self, address = 0x3E):
        self._bus = mraa.I2c(0)
        self._addr = address
        self._bus.address(self._addr)
        if self._bus.writeByte(0):
            print("Check if the LCD {} inserted, then try again"
                    .format(self.name))
            sys.exit(1)
        self.jhd = upmjhd.Jhd1313m1(0, address, address)

    @property
    def name(self):
        '''
        Get device name

        Returns:
            string: JHD1802
        '''
        return "JHD1802"

    def type(self):
        '''
        Get device type

        Returns:
            int: ``TYPE_CHAR``
        '''
        return TYPE_CHAR

    def size(self):
        '''
        Get display size

        Returns:
            (Rows, Columns): the display size, in characters.
        '''
        # Charactor 16x2
        # return (Rows, Columns)
        return 2, 16

    def clear(self):
        '''
        Clears the screen and positions the cursor in the upper-left corner.
        '''
        self.jhd.clear()

    def draw(self, data, bytes):
        '''
        Not implement for char type display device.
        '''
        return False

    def home(self):
        '''
        Positions the cursor in the upper-left of the LCD.
        That is, use that location in outputting subsequent text to the display.
        '''
        self.jhd.home()

    def setCursor(self, row, column):
        '''
        Position the LCD cursor; that is, set the location
        at which subsequent text written to the LCD will be displayed.

        Args:
            row   (int): the row at which to position cursor, with 0 being the first row
            column(int): the column at which to position cursor, with 0 being the first column

	Returns:
	    None
        '''
        self.jhd.setCursor(row, column)

    def write(self, msg):
        '''
        Write character(s) to the LCD.

        Args:
            msg (string): the character(s) to write to the display

        Returns:
            None
        '''
        self.jhd.write(msg)

    def _cursor_on(self, enable):
        if enable:
            self.jhd.cursorOn()
        else:
            self.jhd.cursorOff()
