from fastapi import HTTPException

class GetMsgList:
  class GetMsgListInfo:    
    def __init__(self, row):
      self.refno = row.get("REFNO")
      self.title = row.get("TITLE")
      self.contents = row.get("CONTENTS")
      self.inpdate = row.get("INPDATE")
      self.blno = row.get("BLNO")
      self.read = row.get("READ")
      
  def __init__(self, db: DBContext, fcmToken):
    try:
      lstResult = db.call_proc("skr_mobile.Pkg_PushAlarm.getMsgList", [fcmToken])
      pResult = lstResult[0]

      self.ResultData = []
      for data in pResult:
        lstinfo = self.GetMsgListInfo(data)
        self.ResultData.append(lstinfo)
    except Exception as ex:
      raise HTTPException(status_code=500, detail=str(ex))
  
  def __setattr__(self, name, value):
    if value == None:
      return object.__setattr__(self, name, "")
    else:
      return object.__setattr__(self, name, value)
      
class GetNotReadAlarm:
  class GetNotReadAlarmInfo:    
    def __init__(self, row):
      self.cnt = row.get("CNT")
      
  def __init__(self, db: DBContext, fcmToken):
    try:
      lstResult = db.call_proc("skr_mobile.Pkg_PushAlarm.getNotReadCount", [fcmToken])
      pResult = lstResult[0]

      self.ResultData = []
      for data in pResult:
        lstinfo = self.GetNotReadAlarmInfo(data)
        self.ResultData.append(lstinfo)
    except Exception as ex:
      raise HTTPException(status_code=500, detail=str(ex))
  
  def __setattr__(self, name, value):
    if value == None:
      return object.__setattr__(self, name, "")
    else:
      return object.__setattr__(self, name, value)
      
class SetReadAlarm:
  class SetReadAlarmInfo:
    def __init__(self, row):
      self.cnt = row.get("CNT")
      
  def __init__(self, db: DBContext, fcmToken, refno):
    try:
      lstResult = db.call_proc("skr_mobile.Pkg_PushAlarm.setReadAlarm", [fcmToken, refno])
      pResult = lstResult[0]

      self.ResultData = []
      for data in pResult:
        lstinfo = self.SetReadAlarmInfo(data)
        self.ResultData.append(lstinfo)
    except Exception as ex:
      raise HTTPException(status_code=500, detail=str(ex))
  
  def __setattr__(self, name, value):
    if value == None:
      return object.__setattr__(self, name, "")
    else:
      return object.__setattr__(self, name, value)