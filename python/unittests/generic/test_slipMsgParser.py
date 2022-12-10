from mesh.generic.msgParser import MsgParser
from mesh.generic.slipMsg import SLIPMsg
from test_SLIPMsg import truthSLIPMsg, testMsg
from mesh.generic.utilities import packData

class TestSLIPMsgParser:
    
    def setup_method(self, method):
        # Create SLIPMsgParser instance
        self.msgParser = MsgParser({'parseMsgMax': 10}, SLIPMsg(256))
    
    def test_parseSerialMsg(self):
        """Test parseSerialMessage method of SLIPMsgParser."""
        # Check rejection of message with invalid CRC
        self.msgParser.parseSerialMsg(truthSLIPMsg, 0)
        assert(self.msgParser.msg.msgFound == True) # slip msg found
        assert(self.msgParser.msg.msgEnd != 1) # message end found
        assert(self.msgParser.parsedMsgs == []) # message rejected      

        # Check acceptance of message with valid CRC    
        crc = self.msgParser.msg.crc(testMsg)
        slipMsg = SLIPMsg(256)
        slipMsg.encodeMsg(testMsg) 
        self.msgParser.parseSerialMsg(slipMsg.encoded, 0)
        assert(self.msgParser.msg.msgFound == True) # slip msg found
        assert(self.msgParser.msg.msgEnd != 1) # message end found
        assert(self.msgParser.parsedMsgs[0] == testMsg) # message accepted  
        
        # Check that proper message end position is returned
        self.msgParser.parsedMsgs = []
        paddedMsg = slipMsg.encoded + b'989898'
        msgEnd = self.msgParser.parseSerialMsg(paddedMsg, 0)
        assert(self.msgParser.parsedMsgs[0] == testMsg)
        assert(msgEnd == len(slipMsg.encoded)-1)
        
    def test_encodeMsg(self):
        """Test encodeMsg method of SLIPMsgParser."""
        slipMsg = SLIPMsg(256)
        slipMsg.encodeMsg(testMsg)
        encodedMsg = self.msgParser.encodeMsg(testMsg)
        assert(encodedMsg == slipMsg.encoded)
