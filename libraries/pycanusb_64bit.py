 # -*- coding: utf-8 -*-
"""
Copyright (c) 2010, Martin Gysel
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the <organization> nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from ctypes import *
from ctypes.wintypes import LPCSTR, LPSTR

##
# @package pycanusb

# define CANUSB_ACCEPTANCE_CODE_ALL 0x00000000
ACCEPTANCE_CODE_ALL         = 0
# CANUSB_ACCEPTANCE_MASK_ALL 0xFFFFFFFF
ACCEPTANCE_MASK_ALL         = 4294967295

STATUS_RECEIVE_FIFO_FULL    = 1
STATUS_TRANSMIT_FIFO_FULL   = 2
STATUS_ERROR_WARNING        = 4
STATUS_DATA_OVERRUN         = 8
STATUS_ERROR_PASSIVE        = 32
STATUS_ARBITRATION_LOST     = 64
STATUS_BUS_ERROR            = 128

# Error return codes
ERROR_OK                    = 1
ERROR_GENERAL               =-1
ERROR_OPEN_SUBSYSTEM        =-2
ERROR_COMMAND_SUBSYSTEM     =-3
ERROR_NOT_OPEN              =-4
ERROR_TX_FIFO_FULL          =-5
ERROR_INVALID_PARAM         =-6
ERROR_NO_MESSAGE            =-7
ERROR_MEMORY_ERROR          =-8
ERROR_NO_DEVICE             =-9
ERROR_TIMEOUT               =-10
ERROR_INVALID_HARDWARE      =-11

# Open flags
FLAG_TIMESTAMP       = 1  # Timestamp messages
FLAG_QUEUE_REPLACE   = 2  # If input queue is full remove oldest message and insert new

# timeout flags
FLAG_BLOCK           = 4   # Block receive/transmit
FLAG_SLOW            = 8   # Check ACK/NACK's
FLAG_NO_LOCAL_SEND   = 16  # Don't send transmited frames on

# Flush flags
FLUSH_WAIT           = 0
FLUSH_DONTWAIT       = 1
FLUSH_EMPTY_INQUEUE  = 2

# message flags
CANMSG_EXTENDED      = 128
CANMSG_RTR           = 64

# typedef long CANHANDLE
CANHANDLE = c_long

# typedef unsigned char CANDATA
CANDATA = c_ubyte * 8

class CANMsg(Structure):
    _fields_ = [("id", c_uint),
                ("timestamp", c_uint),
                ("flags", c_ubyte),
                ("len", c_ubyte),
                ("data", c_ubyte * 8)]
    
    def __repr__(self):
        if self.flags & CANMSG_EXTENDED:
            ext = '|Extended'
        else:
            ext = ''
        if self.flags & CANMSG_RTR:
            rtr = '|RTR'
        else:
            rtr = ''
        return "ID: %d%s%s, Length: %d, Data: %s, Timestamp: %d" % (self.id, ext, rtr, self.len, self.dataAsHexStr(), self.timestamp)
        
    def dataAsHexStr(self, length=8, prefix='0x'):
        s = prefix
        for i in range(length):
            if i < self.len:
                s = s + '%0.2x' % self.data[i]
            else:
                s = s + '00'
        return s
        
    def copy(self):
        m = CANMsg()
        m.id = self.id
        m.timestamp = self.timestamp
        m.flags = self.flags
        m.len = self.len
        for i in range(self.len):
            m.data[i] = self.data[i]
        return m

class CANMsgEx(Structure):
    _fields_ = [("id", c_uint),         # Message id
                ("timestamp", c_uint),  # timestamp in milliseconds
                ("flags", c_ubyte),     # [extended_id|1][RTR:1][reserver:6]
                ("len", c_ubyte)]       # Frame size (0.8)

class CANUsbStatistics(Structure):
    _fields_ = [("cntReceiveFrames", c_uint),  # of receive frames
                ("cntTransmitFrames", c_uint), # of transmitted frames
                ("cntReceiveData", c_uint),    # of received data bytes
                ("cntTransmitData", c_uint),   # of transmitted data bytes	
                ("cntOverruns", c_uint),       # of overruns
                ("cntBusWarnings", c_uint),    # of bys warnings
                ("cntBusOff", c_uint)]         # of bus off's

    def __repr__(self):
        return "ReceiveFrames %d, TransmitFrames %d, ReceiveData %d, TransmitData %d, Overruns %d, BusWarnings %d, BusOff %d" \
                % (self.cntReceiveFrames, self.cntTransmitFrames, 
                   self.cntReceiveData, self.cntTransmitData,
                   self.cntOverruns, self.cntBusWarnings, self.cntBusOff)
    
    def __eq__(self, other):
        if isinstance(other, CANUsbStatistics):
            if self.cntReceiveFrames == other.cntReceiveFrames and \
            self.cntTransmitFrames == other.cntTransmitFrames and  \
            self.cntReceiveData == other.cntReceiveData and        \
            self.cntTransmitData == other.cntTransmitData and      \
            self.cntOverruns == other.cntOverruns and              \
            self.cntBusWarnings == other.cntBusWarnings and        \
            self.cntBusOff == other.cntBusOff:
                return True
        return False
            
    def __ne__(self, other):
        return not self.__eq__(other)
##
# Initiate a search of available CANUSB adapters on a system. 
# \return A list of serial numbers of all attached adapters if there are any, 
#         an empty list otherwise.
# \note Due to the internal functionality of windows USB functionality this call
#       may fail to detect a device that has been added or removed after the
#       driver dll has been loaded. This detection works most of the time but if
#       absolute security is needed it is best if the CAN control and handling
#       code is on one thread and the adapter detection on an other tread/process.
def getAdapters():
    try:
        dll = WinDLL("canusbdrv.dll")
    except Exception:
        try:
            dll = WinDLL("canusbdrv64.dll")
        except Exception:
            return False
    buf = create_string_buffer(35)
    f1 = dll.canusb_getFirstAdapter
    f2 = dll.canusb_getNextAdapter
    f1.argtypes = [POINTER(c_byte), c_int]
    f2.argtypes = [POINTER(c_byte), c_int]
    f1.restypes = c_int
    f2.restypes = c_int
    res = f1(cast(buf, POINTER(c_byte)), 35)
    ret = []
    while res > 0:
        ret.append(buf.value)
        if f2(cast(buf, POINTER(c_byte)), 35) <= 0:
            print("getNextAdapter() failed")
            break
        res -= 1
    del dll
    return ret
            

def declareCallback(pyFunc):
    RCVFUNC = WINFUNCTYPE(None, POINTER(CANMsg))
    return RCVFUNC(pyFunc)

##
# Create an entity of a channel to a physical CAN interface.
# You can create several entities of a  channels to the same physical interface
# A virtual channel is opened for each entity. If there are several entities to
# the same interface, it get's closed by deleting the last instance.
# \note To open virtual channels the interface must be named in szID. A blank
#       id is only valid for the first open. SzBitrate, acceptance_code,
#       acceptance_mask and flags does not have any meaning except for the first
#       instance.
#
class CanUSB(object):
    ## 
    # Creates an instance of an CanUSB object
    # \param id szID Serial number for adapter or None (default) to open the
    #        first found.
    # \param szBitrate
    #           "10" for 10kbps  <br>
    #           "20" for 20kbps  <br>
    #           "50" for 50kbps  <br>
    #          "100" for 100kbps <br>
    #          "250" for 250kbps <br>
    #          "500" for 500kbps <br>
    #          "800" for 800kbps <br>
    #         "1000" for 1Mbps   <br>
    #        or as a btr pair btr0:btr1 pair eg. "0x03:0x1c" or 3:28 Can be used
    #        to set a custom baudrate.
    # \param a_code Set to ACCEPTANCE_CODE_ALL to get all messages or another
    #        code to filter messages..
    # \param a_mask Set to ACCEPTANCE_MASK_ALL to get all messages or another code
    #        to filter messages..
    # \param flags
    #        FLAG_TIMESTAMP     Timestamp will be set by adapter. If not set
    #                           timestamp will be set by the driver.
    #        FLAG_QUEUE_REPLACE Normally when the input queue is full new
    #                           messages received are disregarded by setting
    #                           this
    #                           flag the first message is the queue is removed
    #                           to make room for the new message. This flag is
    #                           useful when using the readFirst method,
    #        FLAG_BLOCK         Can be set to make Read and Writes blocking.
    #                           Default is an infinite block but the timeout can
    #                           be changed with setTimeouts. Note that readFirst
    #                           and readFirstEx never block.
    #        FLAG_SLOW          This flag can be used at slower transmission
    #                           speeds where the data stream still can be high.
    #                           Every effort is made to transfer the frame even
    #                           if the adapter reports that the internal buffer
    #                           is full. Normally a frame is trashed if the
    #                           hardware buffer becomes full to promote speed.
    #        FLAG_NO_LOCAL_SEND Normally when several channels has been
    #                           opened on the same physical adapter a send of
    #                           a frame on one channel will be seen on the
    #                           other channels. By setting this flag this is
    #                           prevented.
    def __init__(self, id=None, bitrate='500',
                 a_code=ACCEPTANCE_CODE_ALL,
                 a_mask=ACCEPTANCE_MASK_ALL,
                 flags=0):
        try:
            self.__lib = WinDLL("canusbdrv.dll")
        except Exception:
            try:
                self.__lib = WinDLL("canusbdrv64.dll")
            except Exception:
                print("Couldn't load canusbdrv.dll or canusbdrv64.dll")
                return None
        self.__cb_set = False
        
        self.__canusb_Open = self.__lib.canusb_Open
        self.__canusb_Open.argtypes = [LPCSTR, LPCSTR, c_ulong, c_ulong, c_ulong]
        self.__canusb_Open.restype = CANHANDLE
        self.__handle = self.__canusb_Open(id, bitrate, a_code, a_mask, flags)
        print self.__handle
        print 'Id',id,type(id)
        print 'bitrate',bitrate,type(bitrate)
        print 'additional params',a_code, a_mask, flags
        if self.__handle <= 0:
            print("Could not open device")
            
            raise AttributeError
#            return None
                
        self.__canusb_Read = self.__lib.canusb_Read
        #self.__canusb_Read.argtypes = [CANHANDLE, POINTER(CANMsg)]
        self.__canusb_Read.restype = c_int
        
        self.__canusb_ReadEx = self.__lib.canusb_ReadEx
        #self.__canusb_ReadEx.argtypes = [CANHANDLE, POINTER(CANMsg), POINTER(CANDATA)]
        self.__canusb_ReadEx.restype = c_int
        
        self.__canusb_ReadFirst = self.__lib.canusb_ReadFirst
        #self.__canusb_ReadFirst.argtypes = [CANHANDLE, c_uint, c_ubyte, POINTER(CANMsg)]
        self.__canusb_ReadFirst.restype = c_int
        
        self.__canusb_ReadFirstEx = self.__lib.canusb_ReadFirstEx
        #self.__canusb_ReadFirstEx.argtypes = [CANHANDLE, c_uint, c_ubyte, POINTER(CANMsgEx), POINTER(CANDATA)]
        self.__canusb_ReadFirstEx.restype = c_int
        
        self.__canusb_Write = self.__lib.canusb_Write
        #self.__canusb_Write.argtypes = [CANHANDLE, POINTER(CANMsg)]
        self.__canusb_Write.restype = c_int
        
        self.__canusb_WriteEx = self.__lib.canusb_WriteEx
        #self.__canusb_WriteEx.argtypes = [CANHANDLE, POINTER(CANMsg), POINTER(CANDATA)]
        self.__canusb_WriteEx.restype = c_int
        
        self.__canusb_Status = self.__lib.canusb_Status
#        print self.__lib
        self.__canusb_Status.argtypes = [c_float]
        self.__canusb_Status.restype = c_int

        self.__canusb_VersionInfo = self.__lib.canusb_VersionInfo
        self.__canusb_VersionInfo.argtypes = [CANHANDLE, LPSTR]
        self.__canusb_VersionInfo.restype = c_int
        
        self.__canusb_Flush = self.__lib.canusb_Flush
        self.__canusb_Flush.argtypes = [CANHANDLE, c_ubyte]
        self.__canusb_Flush.restype = c_int

        self.__canusb_SetTimeouts = self.__lib.canusb_SetTimeouts
        self.__canusb_SetTimeouts.argtypes = [CANHANDLE, c_uint, c_uint]
        self.__canusb_SetTimeouts.restype = c_int

        self.__canusb_GetStatistics = self.__lib.canusb_GetStatistics
        self.__canusb_GetStatistics.restype = c_int
        
        self.__canusb_setReceiveCallBack = self.__lib.canusb_setReceiveCallBack
        self.__canusb_setReceiveCallBack.restype = c_int
        
        self.__canusb_Close = self.__lib.canusb_Close
        self.__canusb_Close.restype = c_int


    def __del__(self):
        try:
            self.__canusb_Close(self.__handle)
        except AttributeError:
            pass
    ##
    # Read message from channel.
    # \note If a callback function is defined this call will not work.
    # \returns TODO: Returns: <= 0 on failure. >0 on ERROR_OK.
    #          ERROR_NO_MESSAGE is returned if there is no message to read.
    def read(self):
        # TODO: check for callback function
#        print 'read called'
        msg = CANMsg()
        
        res = self.__canusb_Read(self.__handle, pointer(msg))
#        print 'res',res,'error',ERROR_NO_MESSAGE
        if res > 0:
#            print 'msg',msg
            return msg
        elif res == ERROR_NO_MESSAGE:
#            print ERROR_NO_MESSAGE
            return None
        else:
            return False

    ##
    # Read message from channel. 
    # Alternative version without data character array in message stucture
    def readEx(self):
        msg = CANMsg()
        data = CANDATA()
        
        res = self.__canusb_ReadEx(self.__handle, pointer(msg), pointer(data));
        if res > 0:
            return msg, data
        elif res == ERROR_NO_MESSAGE:
            return None
        else:
            return False

    ##
    # Read the first message from channel that has an id equal to selectid and
    # flags equal to selectflags.
    def readFirst(self, id):
        msg = CANMsg()
        flags = c_ubyte
        res = self.__canusb_ReadFirst(self.__handle, id, flags, pointer(msg))
        if res > 0:
            return msg, flags
        elif res == ERROR_NO_MESSAGE:
            return None
        else:
            return False
            
    ##
    # Read the first message from channel that has an id equal to selectid and
    # flags equal to selectflags . Alternative version without data character
    # array in message structure.
    def readFirstEx(self, id):
        msg = CANMsg()
        data = CANDATA()
        flags = c_ubyte
        res = self.__canusb_ReadFirstEx(self.__handle, id, flags, pointer(msg), pointer(data))
        if res > 0:
            return msg, data, flags
        elif res == ERROR_NO_MESSAGE:
            return None
        else:
            return False

    ##
    # Write message to channel
    def write(self, msg):
        #print self.__handle,'\nPointer: ', pointer(msg),'msg: ',msg
#        help(self.__canusb_Write)
#        print 'pointer',pointer(msg)
    
        res = self.__canusb_Write(self.__handle, pointer(msg))
        if res > 0:
            return True
        else:
            return res
        #Write message to channel with handle h.
        #Returns: <= 0 on failure. >0 on ERROR_OK.
        #ERROR_TX_FIFO_FULL is returned if there is no room for the message..

    def writeEx(self, msg, data):
        res = self.__canusb_WriteEx(self.__handle, pointer(msg), pointer(data))
        return res

    ##
    # Get Adapter status for channel.
    # Returns: Status value with bit values as below or ERROR_TIMEOUT if
    # unable to get status in time. Call status again if this happens.
    # If this method is called very often performance will degrade. Its is
    # recommended that it is called at most once every ten seconds.
    def status(self, asText=False, sep='|'):
#        print 'status on in pycanusb'
        res = self.__canusb_Status(self.__handle)
#        print 'status off in pycanusb'
        if asText == False:
            return res
        else:
            l = []
            if res & STATUS_RECEIVE_FIFO_FULL:
                l.append("Receive Fifo Full")
            if res & STATUS_TRANSMIT_FIFO_FULL:
                l.append("Transmit Fifo Full") 
            if res & STATUS_ERROR_WARNING:
                l.append("Error Warning")
            if res & STATUS_DATA_OVERRUN:
                l.append("Data Overrun")
            if res & STATUS_ERROR_PASSIVE:
                l.append("Error Passive")
            if res & STATUS_ARBITRATION_LOST:
                l.append("Arbitration Lost")
            if res & STATUS_BUS_ERROR:
                l.append("Bus Error")
#            print res, l
            res = ''
            for i in l:
                res = res + i + sep
            return res[:-1]

    ## Get hardware/firmware and driver version for channel    
    def versionInfo(self):
        buf = create_string_buffer(35)
        res = self.__canusb_VersionInfo(self.__handle, buf) #cast(buf, LPSTR))
        if res <= 0:
            return None
        #Format: "VHhFf - Nxxxx - n.n.n - CCCCCCCCCC"
        #V, N = Constant
        #H = Hardware_Major    h = Hardware_Minor
        #F = Firmware_Major    f = Firmware_Minor
        #x = CANUSB serial #   n = Driver version
        #C = Custom String, Default "LAWICEL AB"
        hw_ver = buf.value[1:5]
        ser_nb = buf.value[9:13]
        drv_ver = buf.value[16:21]
        cst_str = buf.value[24:34]
        return [hw_ver, ser_nb, drv_ver, cst_str]

    ##
    # Flush output buffer for channel.
    # If flushflags is set to FLUSH_DONTWAIT the queue is just emptied and there
    # will be no wait for any frames in it to be sent. FLUSH_EMPTY_INQUEUE ca be
    # used to empty the inqueue.
    def flush(self, flags):
        res = self.__canusb_Flush(self.__handle, flags)
        if res > 0:
            return True
        return False

    ##
    # When an channel has been opened with the FLAG_BLOCK read and write
    # operations will block infinitely. This can be changed by setting the
    # timeout in milliseconds with this call.
    def setTimeouts(self, rxTo, txTo):
        res = self.__canusb_SetTimeouts(self.__handle, rxTo, txTo)
        if res > 0:
            return True
        return False

    ##
    # Get transmission statistics for channel.
    def getStatistics(self):
        stat = CANUsbStatistics()
        res = self.__canusb_GetStatistics(self.__handle, pointer(stat))
        if res > 0:
            return stat
        else:
            return None

    ##
    # With this method one can define a function that will receive all incoming
    # messages. Note that read() will not work after this call. You can make it
    # work again by calling this method and set cb to None.
    # \note cb cannot be any python function. It has to be a windows compatible
    #       callback function which can be declared using declareCallback().
    #       See the example.
    # \code
    # def callback(pointer_msg):
    #    msg = pointer_msg.contents
    #    ....
    # cb = declareCallback(callback)
    # canusb_object.receiveCallback(cb)
    # \endcode
    def setReceiveCallback(self, cb):
        if cb != None:
            res = self.__canusb_setReceiveCallBack(self.__handle, cb)
            self.__cb_set = True
        else:
            res = self.__canusb_setReceiveCallBack(self.__handle, None)
            self.__cb_set = False
        if res > 0:
            return True
        return False
        
if __name__ == "__main__":
    import time
    msg1 = CANMsg()
    msg2 = CANMsg()
    msg1.id = 1
    msg1.len = 1
    msg1.data[0] = 7
    
    
    def callback(msg):
        rmsg = msg.contents
        print("callback called")
        #print(rmsg.id)
        #print(rmsg.data[0])
    
    ad = getAdapters()
    print(ad)
    ad1 = CanUSB(id=ad[0], flags=FLAG_QUEUE_REPLACE)
    time.sleep(2)    
#    print ad1.status()
#    while ad1.status() == 1:
#        del ad1
#        print "reopening"
#        ad1 = CanUSB(id=ad[0], flags=FLAG_QUEUE_REPLACE)
    print(msg1)
    if ad1.write(msg1) > 0:
        print("one msg sent from adapter 1 to 2")

    time.sleep(2)
        
#    cb = declareCallback(callback)
#    ad1.setReceiveCallback(cb)
    
#    time.sleep(2)

    
#    print ad1.status()
    