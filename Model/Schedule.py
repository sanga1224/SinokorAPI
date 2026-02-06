from fastapi import HTTPException

class VSLSchedule:
  class VSLScheduleInfo:
    def __init__(self, row):
      self.ServiceCode = row.get("SVC", "") or ""
      self.VesselCode = row.get("VSL") or ""
      self.VesselName = row.get("VSLNM") or ""
      self.VoyageNumber = row.get("VYG") or ""
      self.Port = row.get("PORT") or ""
      self.PortName = row.get("PORTNM") or ""
      self.WharfCode = row.get("WHARF") or ""
      self.WharfName = row.get("WHARFNM") or ""
      self.ETA = row.get("ETA") or ""
      self.ETA_Day = row.get("ETA_DAY") or ""
      self.ETB = row.get("ETB") or ""
      self.ETB_Day = row.get("ETB_DAY") or ""
      self.ETD = row.get("ETD") or ""
      self.ETD_Day = row.get("ETD_DAY") or ""
      self.Remark = row.get("REMARK") or ""
        
  def __init__(self, db: DBContext, apikey, vslnm, etd):
    try:
      vslschedule = db.call_proc("Pkg_API.getVesselSchedule", [apikey, vslnm, etd])[0]

      self.ResultData = []
      for vslschedule_row in vslschedule:
        apistatus = vslschedule_row.get("APISTATUS")
        if apistatus == "N":
          apimsg = vslschedule_row.get("APIMSG")
          raise Exception(apimsg)
        else:
          self.ResultData.append(self.VSLScheduleInfo(vslschedule_row))

    except Exception as ex:
      raise HTTPException(status_code=500, detail=str(ex))

  def __setattr__(self, name, value):
    if value is None:
      return object.__setattr__(self, name, "")
    else:
      return object.__setattr__(self, name, value)

class PortSchedule:
  class PortScheduleInfo:
    def __init__(self, row):
      self.ServiceCode = row.get("SVC") or ""
      self.VesselCode = row.get("VSL") or ""
      self.VesselName = row.get("VSLNM") or ""
      self.VoyageNumber = row.get("VYG") or ""
      self.WharfCode = row.get("WHARF") or ""
      self.WharfName = row.get("WHARFNM") or ""
      self.ETA = row.get("ETA") or ""
      self.ETA_Day = row.get("ETA_DAY") or ""
      self.ETB = row.get("ETB") or ""
      self.ETB_Day = row.get("ETB_DAY") or ""
      self.ETD = row.get("ETD") or ""
      self.ETD_day = row.get("ETD_DAY") or ""
      self.Remark = row.get("REMARK") or ""

  def __init__(self, db: DBContext, apikey, portcd, etd, wharfcd):
    try:
      portschedule = db.call_proc("Pkg_API.getPortSchedule", [apikey, portcd, wharfcd, etd])[0]

      self.ResultData = []
      for Portschedule_row in portschedule:
        apistatus = Portschedule_row.get("APISTATUS")
        if apistatus == "N":
          apimsg = Portschedule_row.get("APIMSG")
          raise Exception(apimsg)
        else:
          self.ResultData.append(self.PortScheduleInfo(Portschedule_row))

    except Exception as ex:
      raise HTTPException(status_code=500, detail=str(ex))

  def __setattr__(self, name, value):
    if value is None:
      return object.__setattr__(self, name, "")
    else:
      return object.__setattr__(self, name, value)

class PortToPortSchedule:
  class PortToPortScheduleInfo:
    def __init__(self, row):
      self.LoadingPortCode = ""
      self.LoadingPortName = ""
      self.DischargingPortCode = ""
      self.DischargingPortName = ""
      self.DepartureDate = ""
      self.ArrivalDate = ""
      self.DocumentCutOffTime = row.get("DOCUDATE") or ""
      self.CargoCutOffTime = row.get("CNTRDATE") or ""
      self.AvailableForBooking = row.get("AVAILBK") or ""
      self.MRN_Number = row.get("MRN") or ""
      self.TS_PortCode = row.get("TS_PORT") or ""  # null이면 빈문자열로 나오게 처리
      self.TS_PortName = row.get("TS_PORTNM") or ""
      self.CallSign = row.get("CALLSIGN") or ""
      self.VesselInformation = []  # TS 시 새로운 Vessel 객체 생성

  class FastestScheduleInfo:
    def __init__(self, row):
      self.VesselSequence = row.get("VESSELSEQUENCE")
      self.ServiceCode = row.get("SERVICECODE")
      self.VesselCode = row.get("VESSELCODE")
      self.VesselName = row.get("VESSELNAME")
      self.VoyageNumber = row.get("VOYAGENUMBER")
      self.LoadingPortCode = row.get("LOADINGPORTCODE")
      self.LoadingPortName = row.get("LOADINGPORTNAME")
      self.LoadingTerminalCode = row.get("LOADINGTERMINALCODE")
      self.LoadingTerminalName = row.get("LOADINGTERMINALNAME")
      self.DischargingPortCode = row.get("DISCHARGINGPORTCODE")
      self.DischargingPortName = row.get("DISCHARGINGPORTNAME")
      self.DischargingTerminalCode = row.get("DISCHARGINGTERMINALCODE")
      self.DischargingTerminalName = row.get("DISCHARGINGTERMINALNAME")
      self.DepartureDate = row.get("DEPARTUREDATE")
      self.ArrivalDate = row.get("ARRIVALDATE")        

  def __init__(self, db: DBContext, apikey, pol, pod, etd):
    try:
      porttoportSchedule = db.call_proc("PKG_API.getPortToPortSchedule", [apikey, pol, pod, etd])[0]
        
      self.ResultData = []
      for porttoportschedule_row in porttoportSchedule:
        apistatus = porttoportschedule_row.get("APISTATUS")
        if apistatus == "N":
          apimsg = porttoportschedule_row.get("APIMSG")
          raise Exception(apimsg)
        else:
          portinfo = self.PortToPortScheduleInfo(porttoportschedule_row)
          if porttoportschedule_row.get("POR") != None:
            portinfo.LoadingPortCode = porttoportschedule_row.get("POR")
            portinfo.LoadingPortName = porttoportschedule_row.get("PORNM")
          else:
            portinfo.LoadingPortCode = porttoportschedule_row.get("POL1")
            portinfo.LoadingPortName = porttoportschedule_row.get("POLNM1")
          if porttoportschedule_row.get("DLV") != None:
            portinfo.DischargingPortCode = porttoportschedule_row.get("DLV")
            portinfo.DischargingPortName = porttoportschedule_row.get("DLVNM")
          else:
            if porttoportschedule_row.get("POD4") != None:
              portinfo.DischargingPortCode = porttoportschedule_row.get("POD4")
              portinfo.DischargingPortName = porttoportschedule_row.get("PODNM4")
            elif porttoportschedule_row.get("POD3") != None:
              portinfo.DischargingPortCode = porttoportschedule_row.get("POD3")
              portinfo.DischargingPortName = porttoportschedule_row.get("PODNM3")
            elif porttoportschedule_row.get("POD2") != None:
              portinfo.DischargingPortCode = porttoportschedule_row.get("POD2")
              portinfo.DischargingPortName = porttoportschedule_row.get("PODNM2")
            else:
              portinfo.DischargingPortCode = porttoportschedule_row.get("POD1")
              portinfo.DischargingPortName = porttoportschedule_row.get("PODNM1")
          portinfo.DepartureDate = porttoportschedule_row.get("ETD1")
          if porttoportschedule_row.get("ETA4") != None:
            portinfo.ArrivalDate = porttoportschedule_row.get("ETA4")
          elif porttoportschedule_row.get("ETA3") != None:
            portinfo.ArrivalDate = porttoportschedule_row.get("ETA3")
          elif porttoportschedule_row.get("ETA2") != None:
            portinfo.ArrivalDate = porttoportschedule_row.get("ETA2")
          else:
            portinfo.ArrivalDate = porttoportschedule_row.get("ETA1")
          
          vslSeq = 1
          lastPod = ""
          lastPodNm = ""
          
          if porttoportschedule_row.get("POR") != None:
            vesselinfo = {  # vessel 항목에 넣기 위한 set
              "VesselSequence": vslSeq,
              "ServiceCode": "",
              "VesselCode": "",
              "VesselName": "Barge" if porttoportschedule_row.get("PORWAY") == "B" else "Rail" if porttoportschedule_row.get("PORWAY") == "R" else "Truck",
              "VoyageNumber": "",
              "LoadingPortCode": porttoportschedule_row.get("POR"),
              "LoadingPortName": porttoportschedule_row.get("PORNM"),
              "LoadingTerminalCode": "",
              "LoadingTerminalName": "",
              "DischargingPortCode": porttoportschedule_row.get("POL1"),
              "DischargingPortName": porttoportschedule_row.get("POLNM1"),
              "DischargingTerminalCode": "",
              "DischargingTerminalName": "",
              "DepartureDate": "",
              "ArrivalDate": "",
            }
            portinfo.VesselInformation.append(vesselinfo)
            vslSeq += 1
            lastPod = porttoportschedule_row.get("POL1")
            lastPodNm = porttoportschedule_row.get("POLNM1")
              
          vesselinfo = {  # vessel 항목에 넣기 위한 set
            "VesselSequence": vslSeq,
            "ServiceCode": porttoportschedule_row.get("SVC1"),
            "VesselCode": porttoportschedule_row.get("VSL1"),
            "VesselName": porttoportschedule_row.get("VSLNM1"),
            "VoyageNumber": porttoportschedule_row.get("VYG1"),
            "LoadingPortCode": porttoportschedule_row.get("POL1"),
            "LoadingPortName": porttoportschedule_row.get("POLNM1"),
            "LoadingTerminalCode": porttoportschedule_row.get("POLW1"),
            "LoadingTerminalName": porttoportschedule_row.get("POLWNM1"),
            "DischargingPortCode": porttoportschedule_row.get("POD1"),
            "DischargingPortName": porttoportschedule_row.get("PODNM1"),
            "DischargingTerminalCode": porttoportschedule_row.get("PODW1"),
            "DischargingTerminalName": porttoportschedule_row.get("PODWNM1"),
            "DepartureDate": porttoportschedule_row.get("ETD1"),
            "ArrivalDate": porttoportschedule_row.get("ETA1"),
          }
          portinfo.VesselInformation.append(vesselinfo)
          vslSeq += 1
          lastPod = porttoportschedule_row.get("POD1")
          lastPodNm = porttoportschedule_row.get("PODNM1")
          
          if porttoportschedule_row.get("VSL2") != None:
            vesselinfo = {  # vessel 항목에 넣기 위한 set
              "VesselSequence": 2,
              "ServiceCode": porttoportschedule_row.get("SVC2"),
              "VesselCode": porttoportschedule_row.get("VSL2"),
              "VesselName": porttoportschedule_row.get("VSLNM2"),
              "VoyageNumber": porttoportschedule_row.get("VYG2"),
              "LoadingPortCode": porttoportschedule_row.get("POL2"),
              "LoadingPortName": porttoportschedule_row.get("POLNM2"),
              "LoadingTerminalCode": porttoportschedule_row.get("POLW2"),
              "LoadingTerminalName": porttoportschedule_row.get("POLWNM2"),
              "DischargingPortCode": porttoportschedule_row.get("POD2"),
              "DischargingPortName": porttoportschedule_row.get("PODNM2"),
              "DischargingTerminalCode": porttoportschedule_row.get("PODW2"),
              "DischargingTerminalName": porttoportschedule_row.get("PODWNM2"),
              "DepartureDate": porttoportschedule_row.get("ETD2"),
              "ArrivalDate": porttoportschedule_row.get("ETA2"),
            }
            portinfo.VesselInformation.append(vesselinfo)
            vslSeq += 1
            lastPod = porttoportschedule_row.get("POD2")
            lastPodNm = porttoportschedule_row.get("PODNM2")
              
          if porttoportschedule_row.get("VSL3") != None:
            vesselinfo = {  # vessel 항목에 넣기 위한 set
              "VesselSequence": 3,
              "ServiceCode": porttoportschedule_row.get("SVC3"),
              "VesselCode": porttoportschedule_row.get("VSL3"),
              "VesselName": porttoportschedule_row.get("VSLNM3"),
              "VoyageNumber": porttoportschedule_row.get("VYG3"),
              "LoadingPortCode": porttoportschedule_row.get("POL3"),
              "LoadingPortName": porttoportschedule_row.get("POLNM3"),
              "LoadingTerminalCode": porttoportschedule_row.get("POLW3"),
              "LoadingTerminalName": porttoportschedule_row.get("POLWNM3"),
              "DischargingPortCode": porttoportschedule_row.get("POD3"),
              "DischargingPortName": porttoportschedule_row.get("PODNM3"),
              "DischargingTerminalCode": porttoportschedule_row.get("PODW3"),
              "DischargingTerminalName": porttoportschedule_row.get("PODWNM3"),
              "DepartureDate": porttoportschedule_row.get("ETD3"),
              "ArrivalDate": porttoportschedule_row.get("ETA3"),
            }
            portinfo.VesselInformation.append(vesselinfo)
            vslSeq += 1
            lastPod = porttoportschedule_row.get("POD3")
            lastPodNm = porttoportschedule_row.get("PODNM3")
              
          if porttoportschedule_row.get("VSL4") != None:
            vesselinfo = {  # vessel 항목에 넣기 위한 set
              "VesselSequence": 4,
              "ServiceCode": porttoportschedule_row.get("SVC4"),
              "VesselCode": porttoportschedule_row.get("VSL4"),
              "VesselName": porttoportschedule_row.get("VSLNM4"),
              "VoyageNumber": porttoportschedule_row.get("VYG4"),
              "LoadingPortCode": porttoportschedule_row.get("POL4"),
              "LoadingPortName": porttoportschedule_row.get("POLNM4"),
              "LoadingTerminalCode": porttoportschedule_row.get("POLW4"),
              "LoadingTerminalName": porttoportschedule_row.get("POLWNM4"),
              "DischargingPortCode": porttoportschedule_row.get("POD4"),
              "DischargingPortName": porttoportschedule_row.get("PODNM4"),
              "DischargingTerminalCode": porttoportschedule_row.get("PODW4"),
              "DischargingTerminalName": porttoportschedule_row.get("PODWNM4"),
              "DepartureDate": porttoportschedule_row.get("ETD4"),
              "ArrivalDate": porttoportschedule_row.get("ETA4"),
            }
            portinfo.VesselInformation.append(vesselinfo)
            vslSeq += 1
            lastPod = porttoportschedule_row.get("POD4")
            lastPodNm = porttoportschedule_row.get("PODNM4")
              
          if porttoportschedule_row.get("DLV") != None:
            vesselinfo = {  # vessel 항목에 넣기 위한 set
              "VesselSequence": vslSeq,
              "ServiceCode": "",
              "VesselCode": "",
              "VesselName": "Barge" if porttoportschedule_row.get("DLVWAY") == "B" else "Rail" if porttoportschedule_row.get("DLVWAY") == "R" else "Truck",
              "VoyageNumber": "",
              "LoadingPortCode": lastPod,
              "LoadingPortName": lastPodNm,
              "LoadingTerminalCode": "",
              "LoadingTerminalName": "",
              "DischargingPortCode": porttoportschedule_row.get("DLV"),
              "DischargingPortName": porttoportschedule_row.get("DLVNM"),
              "DischargingTerminalCode": "",
              "DischargingTerminalName": "",
              "DepartureDate": "",
              "ArrivalDate": "",
            }
            portinfo.VesselInformation.append(vesselinfo)

          self.ResultData.append(portinfo)  # 최종
    except Exception as ex:
      raise HTTPException(status_code=500, detail=str(ex))

  def __setattr__(self, name, value):
    if value == None:
      return object.__setattr__(self, name, "")
    else:
      return object.__setattr__(self, name, value)

class CallingSchedule:
  class CallingScheduleInfo:
    def __init__(self, row):
      self.ServiceCode = row.get("SERVICECODE", "") or ""
      self.Sequence = row.get("SEQ") or ""
      self.PortCode = row.get("PORTCODE") or ""
      self.PortName = row.get("PORTNAME") or ""
      self.TerminalName = row.get("TERMINALNAME") or ""
      self.EstimateTimeOfArrival = row.get("ESTIMATETIMEOFARRIVAL") or ""
      self.EstimateTimeOfDeparture = row.get("ESTIMATETIMEOFDEPARTURE") or ""
      self.ActualTimeOfArrival = row.get("ACTUALTIMEOFARRIVAL") or ""
      self.ActualTimeOfDeparture = row.get("ACTUALTIMEOFDEPARTURE") or ""

  def __init__(self, db: DBContext, apikey, vslnm, vyg):
    try:
      callingschedule = db.call_proc("Pkg_API.getVslRoute", [apikey, vslnm, vyg])[0]

      self.ResultData = []
      for callingschedule_row in callingschedule:
        apistatus = callingschedule_row.get("APISTATUS")
        if apistatus == "N":
          apimsg = callingschedule_row.get("APIMSG")
          raise Exception(apimsg)
        else:
          self.ResultData.append(
            self.CallingScheduleInfo(callingschedule_row)
          )

    except Exception as ex:
      raise HTTPException(status_code=500, detail=str(ex))

  def __setattr__(self, name, value):
    if value is None:
      return object.__setattr__(self, name, "")
    else:
      return object.__setattr__(self, name, value)

class GetMySchedule:
  class GetMyScheduleInfo:
    def __init__(self, row):
      self.id = row.get("USERID", "") or ""
      self.seq = row.get("SEQ") or ""
      self.pol = row.get("POL") or ""
      self.polnm = row.get("POLNM") or ""
      self.pod = row.get("POD") or ""
      self.podnm = row.get("PODNM") or ""
          
  def __init__(self, db: DBContext, token):
    try:
      mySchedule = db.call_proc("skr_mobile.Pkg_Schedule.GetMySchedule", [token])[0]

      self.ResultData = []
      for mySchedule_row in mySchedule:
        myscheduleinfo = self.GetMyScheduleInfo(mySchedule_row)
        self.ResultData.append(myscheduleinfo)
    except Exception as ex:
      raise HTTPException(status_code=500, detail=str(ex))

  def __setattr__(self, name, value):
    if value is None:
      return object.__setattr__(self, name, "")
    else:
      return object.__setattr__(self, name, value)
      
class AddMySchedule:
  class AddMyScheduleInfo:
    def __init__(self, row):
      self.STATUS = row.get("STATUS", "") or ""
      self.MSG = row.get("MSG") or ""
          
  def __init__(self, db: DBContext, token, pol, pod):
    try:
      mySchedule = db.call_proc("skr_mobile.Pkg_Schedule.AddMySchedule", [token, pol, pod])[0]

      self.ResultData = []
      for mySchedule_row in mySchedule:
        myscheduleinfo = self.AddMyScheduleInfo(mySchedule_row)
        self.ResultData.append(myscheduleinfo)
    except Exception as ex:
      raise HTTPException(status_code=500, detail=str(ex))

  def __setattr__(self, name, value):
    if value is None:
      return object.__setattr__(self, name, "")
    else:
      return object.__setattr__(self, name, value)
      
class DelMySchedule:
  class DelMyScheduleInfo:
    def __init__(self, row):
      self.STATUS = row.get("STATUS", "") or ""
      self.MSG = row.get("MSG") or ""
          
  def __init__(self, db: DBContext, token, pol, pod):
    try:
      mySchedule = db.call_proc("skr_mobile.Pkg_Schedule.DelMySchedule", [token, pol, pod])[0]

      self.ResultData = []
      for mySchedule_row in mySchedule:
        myscheduleinfo = self.DelMyScheduleInfo(mySchedule_row)
        self.ResultData.append(myscheduleinfo)
    except Exception as ex:
      raise HTTPException(status_code=500, detail=str(ex))

  def __setattr__(self, name, value):
    if value is None:
      return object.__setattr__(self, name, "")
    else:
      return object.__setattr__(self, name, value)