from fastapi import HTTPException

class TrackingMap:
  class TrackingMapInfo:
    def __init__(self):
      self.location = []
      self.path = []

  def __init__(self, db: DBContext, blno):
    try:
      result = db.call_proc("skr_mobile.Pkg_BL.getTrackingMapData", [blno])
      pResult1 = result[0]
      pResult2 = result[1]

      self.ResultData = []
      mapinfo = self.TrackingMapInfo()
      for location_row in pResult1:
        locationinfo = {
          "SEQ": location_row.get("SEQ"),
          "CODE": location_row.get("CODE"),
          "NAME": location_row.get("NAME"),
          "MESSAGE": location_row.get("MESSAGE"),
          "LAT": location_row.get("LAT"),
          "LNG": location_row.get("LNG"),
          "COURSE": location_row.get("COURSE"),
        }
        mapinfo.location.append(locationinfo)
      for path_row in pResult2:
        pathinfo = {
          "VSLCD": path_row.get("VSLCD"),
          "VSLNM": path_row.get("VSLNM"),
          "LINER": path_row.get("LINER"),
          "NANM": path_row.get("NANM"),
          "IMONO": path_row.get("IMONO"),
          "CALLSIGN": path_row.get("CALLSIGN"),
          "LAT": path_row.get("LAT"),
          "LNG": path_row.get("LNG"),
        }
        mapinfo.path.append(pathinfo)
      self.ResultData.append(mapinfo)
    except Exception as ex:
      raise HTTPException(status_code=500, detail=str(ex))

  def __setattr__(self, name, value):
    if value == None:
      return object.__setattr__(self, name, "")
    else:
      return object.__setattr__(self, name, value)