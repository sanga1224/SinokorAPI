from fastapi import HTTPException

class GetLogin:
  class GetLoginInfo:    
    def __init__(self, row):
      self.STATUS = row.get("STATUS")
      self.MSG = row.get("MSG")
      
  def __init__(self, db: DBContext, uid, upwd):
      try:
        status = db.call_proc("skr_mobile.Pkg_Account.getLogin", [uid, upwd])
        pResult = status[0]

        self.ResultData = []
        for stat in pResult:
          statinfo = self.GetLoginInfo(stat)
          self.ResultData.append(statinfo)
      except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
  
  def __setattr__(self, name, value):
    if value == None:
      return object.__setattr__(self, name, "")
    else:
      return object.__setattr__(self, name, value)
      
class ChkLogin:
  class ChkLoginInfo:
    def __init__(self, row):
      self.STATUS = row.get("STATUS")
      self.MSG = row.get("MSG")
          
  def __init__(self, db: DBContext, ptoken):
    try:
      status = db.call_proc("skr_mobile.Pkg_Account.chkLogin", [ptoken])
      pResult = status[0]

      self.ResultData = []
      for stat in pResult:
        statinfo = self.ChkLoginInfo(stat)
        self.ResultData.append(statinfo)
    except Exception as ex:
      raise HTTPException(status_code=500, detail=str(ex))
      
  def __setattr__(self, name, value):
    if value == None:
      return object.__setattr__(self, name, "")
    else:
      return object.__setattr__(self, name, value)