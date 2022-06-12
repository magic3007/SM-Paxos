from kv_pb2_grpc import KVServerServicer
from kv_pb2 import KVResponse
import grpc
from kv_paxos import PaxosKV
from node import NodeInfo, NodeInfoList
import logging
from kv_enum import KVStatus

logger = logging.getLogger(__name__)

class KVServerImpl(KVServerServicer):
    def __init__(self,
                 oMynode: NodeInfo,
                 vecNodeList: NodeInfoList,
                 sKVDBPath: str,
                 sPaxosLogPath: str):
        super(KVServerImpl, self).__init__()
        self.oPhxosKV = PaxosKV(oMynode, vecNodeList, sKVDBPath, sPaxosLogPath)
        
    def Put(self, request, context) -> KVResponse:
        eStatus = self.oPhxosKV.Put(request.key, request.value, request.version)
        oResponse = KVResponse(ret=eStatus)
        logging.info(f"ret {eStatus}, key {request.key}, value {request.value}, version {request.version}")
        return oResponse
    
    def GetLocal(self, request, context) -> KVResponse:
        eStatus, sValue, iVersion = self.oPhxosKV.GetLocal(request.key)
        oResponse = KVResponse(ret=eStatus)
        if eStatus == KVStatus.SUCC:    
            oResponse.data.value = sValue
            oResponse.data.version = iVersion 
        elif eStatus == KVStatus.KEY_NOTEXIST:
            oResponse.data.is_deleted = True
            oResponse.data.version = iVersion 
        logging.info(f"ret {eStatus}, key {request.key}, value {sValue}, version {iVersion}")
        return oResponse

    def GetGlobal(self, request, context) -> KVResponse:
        return self.GetLocal(request, context)
    
    def Delete(self, request, context) -> KVResponse:
        eStatus = self.oPhxosKV.Delete(request.key, request.version)
        oResponse = KVResponse(ret=eStatus)
        logging.info(f"ret {eStatus}, key {request.key}, version {request.version}")
        return oResponse 