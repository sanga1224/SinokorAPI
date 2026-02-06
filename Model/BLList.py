from fastapi import HTTPException

class BLList:
  class GetBLList:
    def __init__(self, row):
      self.blno = row.get("BLNO")
      self.vslcd = row.get("VSLCD")
      self.vslnm = row.get("VSLNM")
      self.vyg = row.get("VYG")
      self.pol = row.get("POL")
      self.pod = row.get("POD")
      self.cntr = row.get("CNTR")
      self.dg = row.get("DG")
      self.etd = row.get("ETD")
      self.eta = row.get("ETA")
      self.transit = row.get("TRANSIT")
      self.pickupTransit = row.get("PICKUPTRANSIT")
      self.returnTransit = row.get("RETURNTRANSIT")
      
  def __init__(self, db: DBContext, token, bound, fmdt, todt, pol, pod):
    try:
      if bound == 'O':
        resultSet = db.call_proc("skr_mobile.Pkg_List.GetOutboundList", [token, fmdt, todt, pol, pod])
      elif bound == 'I':
        resultSet = db.call_proc("skr_mobile.Pkg_List.GetInboundList", [token, fmdt, todt, pol, pod])
      else:
        resultSet = db.call_proc("skr_mobile.Pkg_List.GetCrossboundList", [token, fmdt, todt, pol, pod])
      pResult = resultSet[0]

      self.ResultData = []
      for result in pResult:
        lst = self.GetBLList(result)
        self.ResultData.append(lst)
    except Exception as ex:
      raise HTTPException(status_code=500, detail=str(ex))
  
  def __setattr__(self, name, value):
    if value == None:
      return object.__setattr__(self, name, "")
    else:
      return object.__setattr__(self, name, value)