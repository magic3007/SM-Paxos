#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : kvsm.py
# Author            : Jing Mai <jingmai@pku.edu.cn>
# Date              : 06.12.2022
# Last Modified Date: 06.12.2022
# Last Modified By  : Jing Mai <jingmai@pku.edu.cn>

from sm import StateMachine


class KVSM(StateMachine):
    def __init__(self, sDBPath: str):
        super(KVSM, self).__init__()
        self.sDBPath = sDBPath
        self.oKVClient = None
        
    def Init(self):
        