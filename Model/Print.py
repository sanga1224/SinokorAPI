from fastapi import HTTPException

class GetPrintData:
  class PrintDataModel:
    def __init__(self, row):
      self.COMPCD = row.get("COMPCD")
      self.DIV = row.get("DIV")
      self.BKNO = row.get("BKNO")
      self.PID = row.get("PID")
      self.NA = row.get("NA")
      self.SEQ = row.get("SEQ")
      
  def __init__(self, db: DBContext, nacd, token, div, blno):
    try:
      status = db.call_proc("skr_mobile.Pkg_Print.GetPrintData", [nacd, token, div, blno])
      pResult = status[0]

      self.ResultData = []
      for stat in pResult:
        statinfo = self.PrintDataModel(stat)
        self.ResultData.append(statinfo)
    except Exception as ex:
      raise HTTPException(status_code=500, detail=str(ex))
  
  def __setattr__(self, name, value):
    if value == None:
      return object.__setattr__(self, name, "")
    else:
      return object.__setattr__(self, name, value)