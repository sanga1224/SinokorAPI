from fastapi import HTTPException

class Port:
  class PortInfo:
    def __init__(self, row):
      self.NATION = row.get("NATION")
      self.NATIONNM = row.get("NATIONNM")
      self.PORT = row.get("PORT")
      self.PORTNM = row.get("PORTNM")
      self.MAIN = row.get("MAIN")
      self.PORTORDER = row.get("PORTORDER")
      self.LAT = row.get("LAT")
      self.LNG = row.get("LNG")         

  def __init__(self, db: DBContext):
    try:
      port = db.call_proc("Pkg_API.getPortList", [])
      pResult = port[0]

      self.ResultData = []
      for port_row in pResult:
        portinfo = self.PortInfo(port_row)
        self.ResultData.append(portinfo)
    except Exception as ex:
      raise HTTPException(status_code=500, detail=str(ex))
  def __setattr__(self, name, value):
    if value == None:
      return object.__setattr__(self, name, "")
    else:
      return object.__setattr__(self, name, value)