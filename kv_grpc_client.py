from gzip import WRITE
import kv_pb2, kv_pb2_grpc
import grpc
from kv_enum import KVOperatorType, KVStatus

class KVClient(object):
    def __init__(self, oChannel: grpc.Channel):
        self.oStub = kv_pb2_grpc.KVServerStub(oChannel)
    
    def Put(self, sKey: str, sValue: str, iVersion : int) -> KVStatus:
        oRequest = kv_pb2.KVRequest(key=sKey, value=sValue, version=iVersion)
        oRequest.opeartor = KVOperatorType.WRITE
        try:
            oResponse = self.oStub.Put(oRequest)
        except grpc.RpcError as e:
            status = e.code()
        else:
            status = grpc.StatusCode.OK
        if status == grpc.StatusCode.OK:
            return oResponse.ret
        else:
            return KVStatus.FAIL
    
    def GetLocal(self, sKey: str) -> KVStatus:
        oRequest = kv_pb2.KVRequest(key=sKey)
        oRequest.operator = KVOperatorType.READ
        try:
            oResponse = self.oStub.GetLocal(oRequest)
        except grpc.RpcError as e:
            status = e.code()
        else:
            status = grpc.StatusCode.OK
        if status == grpc.StatusCode.OK:
            return oResponse.ret, oResponse.data.value, oResponse.data.version
        else:
            return KVStatus.FAIL, None, None

    def GetLocal(self, sKey: str, iMinVersion: int) -> KVStatus:
        eStatus, sValue, iVersion = self.GetLocal(sKey)
        if eStatus == KVStatus.SUCC:
            if iVersion is not None and iVersion < iMinVersion:
                eStatus = KVStatus.VERSION_NOTEXIST
        return eStatus, sValue, iVersion
    
    def GetGlobal(self, sKey: str) -> KVStatus:
        oRequest = kv_pb2.KVRequest(key=sKey)
        oRequest.operator = KVOperatorType.READ
        try:
            oResponse = self.oStub.GetGlobal(oRequest)
        except grpc.RpcError as e:
            status = e.code()
        else:
            status = grpc.StatusCode.OK
        if status == grpc.StatusCode.OK:
            return oResponse.ret, oResponse.data.value, oResponse.data.version
        else:
            return KVStatus.FAIL, None, None
    
    def Delete(self, sKey: str, iVersion: int) -> KVStatus:
        oRequest = kv_pb2.KVRequest(key=sKey, version=iVersion)
        oRequest.operator = KVOperatorType.DELETE
        try:
            oResponse = self.oStub.Delete(oRequest)
        except grpc.RpcError as e:
            status = e.code()
        else:
            status = grpc.StatusCode.OK
        if status == grpc.StatusCode.OK:
            return oResponse.ret
        else:
            return KVStatus.FAIL
    