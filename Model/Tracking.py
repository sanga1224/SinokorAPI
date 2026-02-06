from fastapi import HTTPException

class Tracking:
  class TrackingInfo:
    def __init__(self, row):
      self.BLNO = row.get("BLNO") or ""
      self.POR = row.get("POR") or ""
      self.POL = row.get("POL")
      self.POD = row.get("POD")
      self.DLV = row.get("DLV")
      self.Container = row.get("CNTR")
      self.COC = row.get("COC")
      self.Special = row.get("SPECIAL") or ""
      self.ETD = row.get("ETD")
      self.ETA = row.get("ETA")
      self.VoyageNumber = row.get("VYG")
      self.ServiceCode = row.get("SVC")
      self.VesselCode = row.get("VSLCD")
      self.VesselName = row.get("VSLNM")
      self.Status = row.get("STATUS")
      self.IsShowMap = row.get("ISSHOWMAP")
      self.Event = []
      
  def __init__(self, db: DBContext, apikey, blno, cntrno):
    try:
      tracking = db.call_proc("Pkg_API.getTracking", [apikey, blno, cntrno])
      pResult1 = tracking[0]
      pResult2 = tracking[1]
      pResult3 = tracking[2]
      pResult4 = tracking[3]
      pResult5 = tracking[4]

      self.ResultData = []
      for tracking_row1 in pResult1:
        apistatus = tracking_row1.get("APISTATUS")
        if apistatus == "N":
          apimsg = tracking_row1.get("apimsg")
          raise Exception(apimsg)
        else:
          for tracking_row2 in pResult2:  # pResult2 값
            trackinginfo = self.TrackingInfo(tracking_row2)
            trackinginfo.BLNO = blno  # BLNO 값 지정
            for tracking_row3 in pResult5:  # pResult5 값
              opt = tracking_row3.get("OPT")
              if opt == "EVENT":  # Event인 것만 보이도록
                eventinfo = {
                  "Event": tracking_row3.get("EVENT"),
                  "MV": tracking_row3.get("MV"),
                  "Unit": tracking_row3.get("UNIT"),
                  "Location": tracking_row3.get("LOCATION"),
                  "EventDate": tracking_row3.get("EVENTDATE"),
                  "EventTime": tracking_row3.get("EVENTTIME"),
                }
                trackinginfo.Event.append(eventinfo)
            self.ResultData.append(trackinginfo)

    except Exception as ex:
      raise HTTPException(status_code=500, detail=str(ex))

  def __setattr__(self, name, value):
    if value == None:
      return object.__setattr__(self, name, "")
    else:
      return object.__setattr__(self, name, value)