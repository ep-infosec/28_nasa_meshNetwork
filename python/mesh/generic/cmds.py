
NodeCmds = {'NoOp': 0, 'CmdResponse': 5, 'GCSCmd': 10, 'ParamUpdate': 30, 'ConfigRequest': 40, 'ConfigUpdate': 35}

PixhawkCmds = NodeCmds.copy()
PixhawkCmds.update({'FormationCmd': 20, 'NodeStateUpdate': 111, 'StateUpdate': 101, 'TargetUpdate': 105, 'PosCmd': 100})

SatFCCmds = NodeCmds.copy()
SatFCCmds.update({'StateUpdate': 201, 'NodeStateUpdate': 211, 'ManeuverCmd': 210})

PixhawkFCCmds = {'ModeChange': 50, 'ArmCommand': 55, 'VehicleStatus': 60, 'PosCmd': 100}

TDMACmds = {'MeshStatus': 90, 'TimeOffset': 91, 'TimeOffsetSummary': 92, 'LinkStatus': 93, 'LinkStatusSummary': 94, 'BlockTxRequest': 95, 'BlockTxPacketReceipt': 97, 'BlockTxStatus': 98, 'BlockData': 99, 'CurrentConfig': 120, 'ConfigUpdate': 121, 'NetworkRestart': 125} 

GndCmds = {'TimeOffsetSummary': 92, 'LinkStatusSummary': 94}

TestCmds = {'SendDataBlock': 150}

FPGACmds = {'FPGAMsgStart': 250}

# Commands that should be relayed
cmdsToRelay = []
#cmdsToRelay = [NodeCmds['GCSCmd'], NodeCmds['ConfigRequest'], NodeCmds['ParamUpdate'], TDMACmds['BlockTxRequest'], TDMACmds['BlockTxRequestResponse'], TDMACmds['BlockTxStatus'], TestCmds['SendDataBlock']]
