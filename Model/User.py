from fastapi import HTTPException

class GetProfile:
  class ProfileInfo:
    def __init__(self, row):
      self.SEQ = row.get("SEQ")
      self.NICKNAME = row.get("NICKNAME")
      self.NAME = row.get("NAME")
      self.CELLNO = row.get("CELLNO")
      self.EMAIL = row.get("EMAIL")
      self.TELNO = row.get("TELNO")
      self.FAXNO = row.get("FAXNO")
      self.ICON = row.get("ICON")
      self.MAXSEQ = row.get("MAXSEQ")
      self.BKC = row.get("BKC")
      self.BLC = row.get("BLC")
      self.CAC = row.get("CAC")
      self.BLI = row.get("BLI")
      self.BLP = row.get("BLP")
      self.LCC = row.get("LCC")
      self.IVI = row.get("IVI")
      self.TXI = row.get("TXI")
      self.FTC = row.get("FTC")
      self.DGC = row.get("DGC")
      self.DLN = row.get("DLN")
      self.VSC = row.get("VSC")
      self.TSC = row.get("TSC")
      self.DOC = row.get("DOC")
      self.EMPGB = row.get("EMPGB")
          
  def __init__(self, db: DBContext, deviceId, token, fcmToken, seq):
    try:
      status = db.call_proc("skr_mobile.Pkg_Account.getProfile", [deviceId, token, fcmToken, seq])
      pResult = status[0]

      self.ResultData = []
      for result in pResult:
        profileinfo = self.ProfileInfo(result)
        self.ResultData.append(profileinfo)
    except Exception as ex:
      raise HTTPException(status_code=500, detail=str(ex))
  
  def __setattr__(self, name, value):
    if value == None:
      return object.__setattr__(self, name, "")
    else:
      return object.__setattr__(self, name, value)
      
class SaveProfile:
  class SaveProfileInfo:
    def __init__(self, row):
      self.STATUS = row.get("STATUS")
      self.MSG = row.get("MSG")
      
  def __init__(self, db: DBContext, token, profile_seq, icon, nickname, name, cellno, email, telno, faxno):
    try:
      status = db.call_proc("skr_mobile.Pkg_Account.saveProfile", [token, profile_seq, icon, nickname, name, cellno, email, telno, faxno])
      pResult = status[0]

      self.ResultData = []
      for stat in pResult:
        statinfo = self.SaveProfileInfo(stat)
        self.ResultData.append(statinfo)
    except Exception as ex:
      raise HTTPException(status_code=500, detail=str(ex))
  
  def __setattr__(self, name, value):
    if value == None:
      return object.__setattr__(self, name, "")
    else:
      return object.__setattr__(self, name, value)
      
class SetProfile:
  class SetProfileInfo:
    def __init__(self, row):
      self.STATUS = row.get("STATUS")
      self.MSG = row.get("MSG")
      
  def __init__(self, db: DBContext, deviceid, token, fcmToken, profile_seq):
    try:
      status = db.call_proc("skr_mobile.Pkg_Account.setMobileProfileInfo", [deviceid, token, fcmToken, profile_seq])
      pResult = status[0]

      self.ResultData = []
      for stat in pResult:
        statinfo = self.SetProfileInfo(stat)
        self.ResultData.append(statinfo)
    except Exception as ex:
      raise HTTPException(status_code=500, detail=str(ex))
  
  def __setattr__(self, name, value):
    if value == None:
      return object.__setattr__(self, name, "")
    else:
      return object.__setattr__(self, name, value)
      
class DeleteProfile:
  class DeleteProfileInfo:
    def __init__(self, row):
      self.STATUS = row.get("STATUS")
      self.MSG = row.get("MSG")
      
  def __init__(self, db: DBContext, token, profile_seq):
    try:
      status = db.call_proc("skr_mobile.Pkg_Account.deleteProfile", [token, profile_seq])
      pResult = status[0]

      self.ResultData = []
      for stat in pResult:
        statinfo = self.DeleteProfileInfo(stat)
        self.ResultData.append(statinfo)
    except Exception as ex:
      raise HTTPException(status_code=500, detail=str(ex))
  
  def __setattr__(self, name, value):
    if value == None:
      return object.__setattr__(self, name, "")
    else:
      return object.__setattr__(self, name, value)
      
class GetProfiles:
  class ProfilesInfo:
    def __init__(self, row):
      self.SEQ = row.get("SEQ")
      self.NICKNAME = row.get("NICKNAME")
      self.NAME = row.get("NAME")
      self.CELLNO = row.get("CELLNO")
      self.EMAIL = row.get("EMAIL")
      self.TELNO = row.get("TELNO")
      self.FAXNO = row.get("FAXNO")
      self.ICON = row.get("ICON")
      self.MAXSEQ = row.get("MAXSEQ")
      self.BKC = row.get("BKC")
      self.BLC = row.get("BLC")
      self.CAC = row.get("CAC")
      self.BLI = row.get("BLI")
      self.BLP = row.get("BLP")
      self.LCC = row.get("LCC")
      self.IVI = row.get("IVI")
      self.TXI = row.get("TXI")
      self.FTC = row.get("FTC")
      self.DGC = row.get("DGC")
      self.DLN = row.get("DLN")
      self.VSC = row.get("VSC")
      self.TSC = row.get("TSC")
      self.DOC = row.get("DOC")
      self.EMPGB = row.get("EMPGB")
          
  def __init__(self, db: DBContext, token):
    try:
      status = db.call_proc("skr_mobile.Pkg_Account.getProfiles", [token])
      pResult = status[0]

      self.ResultData = []
      for result in pResult:
        profilesinfo = self.ProfilesInfo(result)
        self.ResultData.append(profilesinfo)
    except Exception as ex:
      raise HTTPException(status_code=500, detail=str(ex))
  
  def __setattr__(self, name, value):
    if value == None:
      return object.__setattr__(self, name, "")
    else:
      return object.__setattr__(self, name, value)

class GetUserInfo:
  class UserInfo:
    def __init__(self, row):
      self.USERID = row.get("USERID")
      self.STATUS = row.get("STATUS")
      self.PWD1 = row.get("PWD1")
      self.PWD2 = row.get("PWD2")
      self.NACD = row.get("NACD")
      self.BKPORT = row.get("BKPORT")
      self.BKPORTNM = row.get("BKPORTNM")
      self.REGNO = row.get("REGNO")
      self.CUSTNM = row.get("CUSTNM")
      self.CUSTCD = row.get("CUSTCD")
      self.CUSTADDR = row.get("CUSTADDR")
      self.CUSTGB = row.get("CUSTGB")
      self.NICKNAME = row.get("NICKNAME")
      self.USERNAME = row.get("USERNAME")
      self.CELLNO = row.get("CELLNO")
      self.EMAIL = row.get("EMAIL")
      self.TELNO = row.get("TELNO")
      self.FAXNO = row.get("FAXNO")
      self.ICON = row.get("ICON")
      self.INPDATE = row.get("INPDATE")
      self.UPDDATE = row.get("UPDDATE")
      self.CONFIRMUSER = row.get("CONFIRMUSER")
      self.CONFIRMDATE = row.get("CONFIRMDATE")
      self.ROLES = row.get("ROLES")
      self.STPASS = row.get("STPASS")
      self.EDPASS = row.get("EDPASS")
      self.LOGINDATE = row.get("LOGINDATE")
      self.PROHIBITAUTOINVOICE = row.get("PROHIBITAUTOINVOICE")
      self.RESPONSE_MSG = row.get("RESPONSE_MSG")
      self.DASHBOARD = row.get("DASHBOARD")
      self.VALID = row.get("VALID")
          
  def __init__(self, db: DBContext, deviceId, token):
    try:
      status = db.call_proc("skr_mobile.Pkg_Account.getUserInfo", [deviceId, token])
      pResult = status[0]

      self.ResultData = []
      for result in pResult:
        userinfo = self.UserInfo(result)
        self.ResultData.append(userinfo)
    except Exception as ex:
      raise HTTPException(status_code=500, detail=str(ex))
  
  def __setattr__(self, name, value):
    if value == None:
      return object.__setattr__(self, name, "")
    else:
      return object.__setattr__(self, name, value)
      
class DelMobileProfile:
  class DelMobileProfileInfo:
    def __init__(self, row):
      self.STATUS = row.get("STATUS")
      self.MSG = row.get("MSG")
      
  def __init__(self, db: DBContext, deviceId, token):
    try:
      status = db.call_proc("skr_mobile.Pkg_Account.delMobileProfileInfo", [deviceId, token])
      pResult = status[0]

      self.ResultData = []
      for stat in pResult:
        statinfo = self.DelMobileProfileInfo(stat)
        self.ResultData.append(statinfo)
    except Exception as ex:
      raise HTTPException(status_code=500, detail=str(ex))
  
  def __setattr__(self, name, value):
    if value == None:
      return object.__setattr__(self, name, "")
    else:
      return object.__setattr__(self, name, value)
      
class UpdateAlarm:
  class UpdateAlarmInfo:
    def __init__(self, row):
      self.STATUS = row.get("STATUS")
      self.MSG = row.get("MSG")
      
  def __init__(self, db: DBContext, deviceId, token, gb, val):
    try:
      status = db.call_proc("skr_mobile.Pkg_Account.UpdateAlarmInfo", [deviceId, token, gb, val])
      pResult = status[0]

      self.ResultData = []
      for stat in pResult:
        statinfo = self.UpdateAlarmInfo(stat)
        self.ResultData.append(statinfo)
    except Exception as ex:
      raise HTTPException(status_code=500, detail=str(ex))
  
  def __setattr__(self, name, value):
    if value == None:
      return object.__setattr__(self, name, "")
    else:
      return object.__setattr__(self, name, value)