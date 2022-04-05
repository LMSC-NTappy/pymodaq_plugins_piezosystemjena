"""
Demo Wrapper to illustrate the plugin developpement. This Mock wrapper will emulate communication with an instrument
"""

import serial
import warnings
import time

class NV403CLE:
    """Class for wrapping NV40/3 CLE commands"""
    def __init__(self, port: str):
        self.ser = serial.Serial()
        self.ser.baudrate = 19200
        self.ser.bytesize = serial.EIGHTBITS
        self.ser.parity = serial.PARITY_NONE
        self.ser.stopbits = serial.STOPBITS_ONE
        self.ser.xonxoff = True
        self.ser.timeout = 1.0

        self.ser.port = port

    def open(self) -> None:
        """
        Open communication.
        """
        self.ser.open()

    def reset_buffer(self) -> str:
        """Check if the buffer of serial communication has bytes waiting inside.
        If that's the case, read it and log it as some kind of warning."""
        dumped = ""
        if self.ser.in_waiting != 0:
            #Maybe raise a warning?
            dumped = self.ser.read_all().decode()
            warnings.warn(f'Dumped IO-buffer content: {dumped}',RuntimeWarning)
        # self.emit_status(ThreadCommand('Update_Status', [f'Dumped buffer content: {dumped}']))
        return dumped

    def set_axis_remote(self,axis_index: int, remote: bool) -> None:
        """Enable remote control for one axis."""
        val = int(remote)
        cmd = f'setk,{axis_index:d},{val:d}\r'.encode()
        self.ser.write(cmd)

    def get_position(self, axis_index: int) -> float:
        """
        Get the current actuator value
        Returns
        -------
        float: The current value
        """
        _ = self.reset_buffer()

        #Get the index of the current axis
        #Encode it for communication with stage controller
        cmd = f'rk,{axis_index}\r'.encode()

        #Send command and read reply
        self.ser.write(cmd)
        reply = self.ser.read(11) #11 is the size of expected reply
        #Convert value to float
        pos = float(reply[5:-1])

        return pos

    def set_display_brightness(self,brightness: int) -> None:
        """Set Brightness of the Controller display between 0 (screen off) and 255 (max)"""
        if brightness > 255:
            b = 0
        elif brightness < 0:
            b = 0
        else:
            b = brightness
        cmd = f'light,{b}\r'.encode()

        self.ser.write(cmd)

    def set_closed_loop(self,axis_index: int, closed: bool = True):
        """Set an axis to closed-loop or open-loop control
        """
        val = int(closed)
        cmd = f'cloop,{axis_index},{val}\r'.encode()
        self.ser.write(cmd)

    def get_position_offset(self,axis_index: int) -> float:
        """Measure the offset of the axis, """
        #Get the current position
        current_pos = self.get_position(axis_index)

        #Set it as target and measure where it actually lands
        self.set_position(axis_index,value=current_pos)
        time.sleep(0.500) #Here it is mandatory to wait a little bit
        return_position = self.get_position(axis_index)

        #The difference between the two is the offset
        offset = return_position - current_pos

        #Return the axis to where it was
        self.set_position(axis_index,value = current_pos - offset)

        return offset

    def set_position(self,axis_index: int, value: float) -> None:
        """
        Send a call to the actuator to move at the given value
        Parameters
        ----------
        axis_index: (int) the axis to move
        value: (float) the target value in um
        """
        cmd = f'set,{axis_index},{value:.3f}\r'.encode()
        self.ser.write(cmd)

    def get_infos(self) -> str:
        return self.ser.port

    def close(self):
        """
        Close communication.
        """
        self.ser.close()