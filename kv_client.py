#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : kv.py
# Author            : Jing Mai <jingmai@pku.edu.cn>
# Date              : 06.12.2022
# Last Modified Date: 06.12.2022
# Last Modified By  : Jing Mai <jingmai@pku.edu.cn>

from typing import Tuple
import leveldb
import logging
from enum import Enum
from kv_pb2 import KVData
from rwlock import RWLock, ReadLockGuard, WriteLockGuard


logger = logging.getLogger(__name__)


class KVClientRet(Enum):
    OK = 0
    SYS_FAIL = -1
    KEY_NOTEXIST = 1
    KEY_VERSION_CONFLICT = -11

class KVClient(object):
    def __init__(self) -> None:
        self.bHasInit = False
        self.oLevelDB = None
        self.oRWLock = RWLock()

    def Init(self, sDBPath: str) -> bool:
        if self.bHasInit:
            return True
        try:
            self.oLevelDB = leveldb.LevelDB(sDBPath, create_if_missing=True)
        except Exception as e:
            logger.error(f"open leveldb fail, db_path {sDBPath}, err {e}")
            return False
        self.bHasInit = True
        logger.info(f"OK, db_path {sDBPath}")
        return True

    def Get(self, sKey: str) -> Tuple[KVClientRet, str, int]:
        if not self.bHasInit:
            logging.error("not init yet")
            return KVClientRet.SYS_FAIL, None, None
        oGuard = ReadLockGuard(self.oRWLock)
        try:
            sBuffer = self.oLevelDB.Get(bytes(sKey, "utf-8"))
        except KeyError as e:
            logging.error(f"LevelDB.Get not found, key {sKey}")
            iVersion = 0
            return KVClientRet.KEY_NOTEXIST, None, iVersion
        except Exception as e:
            logging.error(f"LevelDB.Get fail, key {sKey}, err {e}")
            return KVClientRet.SYS_FAIL, None, None
        oData = KVData()
        oData.ParseFromString(sBuffer)
        bValue = oData.value
        iVersion = oData.version
        logging.info(f"OK, key {sKey}, value {bValue}, version {iVersion}")
        return KVClientRet.OK, bValue, iVersion
    
