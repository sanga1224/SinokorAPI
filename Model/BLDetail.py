from fastapi import HTTPException

class GetBlDetail:
  class BlDetailInfo:
    def __init__(self, row):
      self.blno = row.get("BLNO")
      self.hblno = row.get("HBLNO")
      self.refNo = row.get("REFNO")
      self.freightNo = row.get("FREIGHTNO")
      self.commodity = row.get("COMMODITY")
      self.commodityLocal = row.get("COMMODITYLOCAL")
      self.shipperRemark = row.get("SHIPPERREMARK")
      self.linerRemark = row.get("LINERREMARK")
      self.forwarder = row.get("FORWARDER")
      self.orgShipper = row.get("ORGSHIPPER")
      self.selfTrans = row.get("SELFTRANS")
      self.selfTransNm = row.get("SELFTRANSNM")
      self.pickupArea = row.get("PICKUPAREA")
      self.pickupDate = row.get("PICKUPDATE")
      self.selfTransPic = row.get("SELFTRANSPIC")
      self.selfTransTel = row.get("SELFTRANSTEL")
      self.cfs = row.get("CFS")
      self.cfsNm = row.get("CFSNM")
      self.cfsPaid = row.get("CFSPAID")
      self.cfsDate = row.get("CFSDATE")
      self.lineTrans = row.get("LINETRANS")
      self.factoryNm = row.get("FACTORYNM")
      self.factoryArea = row.get("FACTORYAREA")
      self.lineTransDate = row.get("LINETRANSDATE")
      self.lineTransPic = row.get("LINETRANSPIC")
      self.lineTransTel = row.get("LINETRANSTEL")
      self.returnTml = row.get("RETURNTML")
      self.onBoardDate = row.get("ONBOARDDATE")
      self.blIssueDate = row.get("BLISSUEDATE")
      self.blIssueType = row.get("BLISSUETYPE")
      self.blIssueArea = row.get("BLISSUEAREA")
      self.blReceiptType = row.get("BLRECEIPTTYPE")
      self.blReceiptArea = row.get("BLRECEIPTAREA")
      self.HHSTCD = row.get("HHSTCD")
      self.HHSTNM = row.get("HHSTNM")
      self.HHBJCD = row.get("HHBJCD")
      self.HHBJNM = row.get("HHBJNM")
      self.HHPASS_CD = row.get("HHPASS_CD")
      self.HHPASS_NM = row.get("HHPASS_NM")
      self.lineTransNm = row.get("LINETRANSNM")
      self.shipperNm = row.get("SHIPPERNM")
      self.consigneeNm = row.get("CONSIGNEENM")
      self.notifyNm = row.get("NOTIFYNM")
      self.vslCd = row.get("VSLCD")
      self.vslNm = row.get("VSLNM")
      self.vyg = row.get("VYG")
      self.porCd = row.get("PORCD")
      self.porNm = row.get("PORNM")
      self.polCd = row.get("POLCD")
      self.polNm = row.get("POLNM")
      self.podCd = row.get("PODCD")
      self.podNm = row.get("PODNM")
      self.dlvCd = row.get("DLVCD")
      self.dlvNm = row.get("DLVNM")
      self.fdCd = row.get("FDCD")
      self.fdNm = row.get("FDNM")
      self.blType = row.get("BLTYPE")
      self.cargoTerm = row.get("CARGOTERM")
      self.cargoType = row.get("CARGOTYPE")
      self.freightTerm = row.get("FREIGHTTERM")
      self.pkg = row.get("PKG")
      self.wgt = row.get("WGT")
      self.cbm = row.get("CBM")
      self.mainItem = row.get("MAINITEM")
      self.say = row.get("SAY")
      self.bkPicGender = row.get("BKPICGENDER")
      self.bkPicInfo = row.get("BKPICINFO")
      self.docuPicGender = row.get("DOCUPICGENDER")
      self.docuPicInfo = row.get("DOCUPICINFO")
      self.salesPicGender = row.get("SALESPICGENDER")
      self.salesPicInfo = row.get("SALESPICINFO")
      self.vslMainPicGender = row.get("VSLMAINPICGENDER")
      self.vslMainPicInfo = row.get("VSLMAINPICINFO")
      self.vslSubPicGender = row.get("VSLSUBPICGENDER")
      self.vslSubPicInfo = row.get("VSLSUBPICINFO")
      self.afrSnaCd = row.get("AFR_SNA")
      self.afrSnaNm = row.get("AFR_SNANM")
      self.afrStel = row.get("AFR_STEL")
      self.afrSregType = row.get("AFR_SREGTYPE")
      self.afrSregNo = row.get("AFR_SREGNO")
      self.afrSexportNo = row.get("AFR_SEXPORTNO")
      self.afrSgstNo = row.get("AFR_SGSTNO")
      self.afrCnaCd = row.get("AFR_CNA")
      self.afrCnaNm = row.get("AFR_CNANM")
      self.afrCtel = row.get("AFR_CTEL")
      self.afrCregType = row.get("AFR_CREGTYPE")
      self.afrCregNo = row.get("AFR_CREGNO")
      self.afrCpic = row.get("AFR_CPIC")
      self.afrCpicTel = row.get("AFR_CPICTEL")
      self.afrCemail = row.get("AFR_CEMAIL")
      self.afrScrap = row.get("AFR_SCRAP")
      self.afrCimportNo = row.get("AFR_CIMPORTNO")
      self.afrCdepositNo = row.get("AFR_CDEPOSITNO")
      self.afrNnaCd = row.get("AFR_NNA")
      self.afrNnaNm = row.get("AFR_NNANM")
      self.afrNtel = row.get("AFR_NTEL")
      self.afrNregType = row.get("AFR_NREGTYPE")
      self.afrNregNo = row.get("AFR_NREGNO")
      self.afrNemail = row.get("AFR_NEMAIL")
      self.afrSzipCode = row.get("AFR_SZIPCODE")
      self.afrScity = row.get("AFR_SCITY")
      self.afrSinvCur = row.get("AFR_SINVCUR")
      self.afrSinvAmt = row.get("AFR_SINVAMT")
      self.afrCzipCode = row.get("AFR_CZIPCODE")
      self.afrCcity = row.get("AFR_CCITY")
      self.afrCgstNo = row.get("AFR_CGSTNO")
      self.afrNzipCode = row.get("AFR_NZIPCODE")
      self.afrNcity = row.get("AFR_NCITY")
      self.afrNimportNo = row.get("AFR_NIMPORTNO")
      self.afrNgstNo = row.get("AFR_NGSTNO")
      self.qualifier = row.get("QUALIFIER")
      self.customsCode = row.get("CUSTOMS_CODE")
      self.docNo = row.get("DOC_NO")
      self.docDate = row.get("DOC_DATE")
      self.userNacd = row.get("USERNACD")
      self.lWharfNm = row.get("LWHARFNM")
      self.auth = row.get("AUTH")
      self.bkStatus = row.get("BKSTATUS")
      self.blStatus = row.get("BLSTATUS")
      self.prtInvoice = row.get("PRTINVOICE")
      self.lineCertiCnt = row.get("LINECERTICNT")
      self.prtAn = row.get("PRTAN")
      self.HHSTATUS = row.get("HHSTATUS")
      self.MFSEND = row.get("MFSEND")
      self.DO = row.get("DO")
      self.schedules = []
      self.trackings = []
      self.marks = []
      self.descs = []
      self.bkCntrs = []
      self.blCntrs = []
      self.dgSpecials = []
      self.freights = []
      self.managedCargos = []
              
  def __init__(self, db: DBContext, deviceid, token, nacd, blno):
    try:
      status = db.call_proc("skr_mobile.Pkg_BL.getBlDetail", [deviceid, token, nacd, blno])
      pResultBasicInfo = status[0]
      pResultSchedule = status[1]
      pResultTracking = status[2]
      pResultMark = status[3]
      pResultDesc = status[4]
      pResultBkCntr = status[5]
      pResultBlCntr = status[6]
      pResultDgSpecial = status[7]
      pResultFreight = status[8]
      pResultManagedCargos = status[9]

      self.ResultData = []
      for basicInfo_row in pResultBasicInfo:
        blDetailInfo = self.BlDetailInfo(basicInfo_row)
                  
      for schedule_row in pResultSchedule:
        schedules = {
          "GB": schedule_row.get("GB"),
          "SVC": schedule_row.get("SVC"),
          "VSL": schedule_row.get("VSL"),
          "VSLNM": schedule_row.get("VSLNM"),
          "VYG": schedule_row.get("VYG"),
          "SPAN": schedule_row.get("SPAN"),
          "POL": schedule_row.get("POL"),
          "POLNM": schedule_row.get("POLNM"),
          "POLW": schedule_row.get("POLW"),
          "POLWNM": schedule_row.get("POLWNM"),
          "POD": schedule_row.get("POD"),
          "PODNM": schedule_row.get("PODNM"),
          "PODW": schedule_row.get("PODW"),
          "PODWNM": schedule_row.get("PODWNM"),
          "ETD": schedule_row.get("ETD"),
          "ETA": schedule_row.get("ETA"),
          "DOCUDATE": schedule_row.get("DOCUDATE"),
          "CNTRDATE": schedule_row.get("CNTRDATE"),
          "VGMCLOSING": schedule_row.get("VGMCLOSING"),
          "AFRCLOSING": schedule_row.get("AFRCLOSING"),
          "MAINEMPGENDER": schedule_row.get("MAINEMPGENDER"),
          "MAINEMPINFO": schedule_row.get("MAINEMPINFO"),
          "SUBEMPGENDER": schedule_row.get("SUBEMPGENDER"),
          "SUBEMPINFO": schedule_row.get("SUBEMPINFO"),
          "MRN": schedule_row.get("MRN"),
          "CALLSGN": schedule_row.get("CALLSGN"),
          "VSLNACD": schedule_row.get("VSLNACD"),
          "DTMLINCOUNT": schedule_row.get("DTMLINCOUNT"),
          "ATMLINCOUNT": schedule_row.get("ATMLINCOUNT"),
          "DTMLVSLVYGCD": schedule_row.get("DTMLVSLVYGCD"),
          "ATMLVSLVYGCD": schedule_row.get("ATMLVSLVYGCD"),
          "TMLREMARK": schedule_row.get("TMLREMARK"),
        }
        blDetailInfo.schedules.append(schedules)
          
      for tracking_row in pResultTracking:
        opt = tracking_row.get("OPT")
        if opt == "EVENT": 
          trackings = {
            "EVENT": tracking_row.get("EVENT"),
            "MV": tracking_row.get("MV"),
            "UNIT": tracking_row.get("UNIT"),
            "LOCATION": tracking_row.get("LOCATION"),
            "EVENTDATE": tracking_row.get("EVENTDATE"),
            "EVENTTIME": tracking_row.get("EVENTTIME"),
          }
          blDetailInfo.trackings.append(trackings)
      
      for mark_row in pResultMark:
        marks = {
          "seq": mark_row.get("SEQ"),
          "txt": mark_row.get("TXT"),
        }
        blDetailInfo.marks.append(marks)
      
      for desc_row in pResultDesc:
        descs = {
          "seq": desc_row.get("SEQ"),
          "txt": desc_row.get("TXT"),
        }
        blDetailInfo.descs.append(descs)
          
      for bkCntr_row in pResultBkCntr:
        bkCntrs = {
          "seq": bkCntr_row.get("SEQ"),
          "tpsz": bkCntr_row.get("TPSZ"),
          "qty": bkCntr_row.get("QTY"),
          "soc": bkCntr_row.get("SOC"),
          "empty": bkCntr_row.get("EMPTY"),
          "dg": bkCntr_row.get("DG"),
          "rf": bkCntr_row.get("RF"),
          "awk": bkCntr_row.get("AWK"),
          "unno": bkCntr_row.get("UNNO"),
          "imdg": bkCntr_row.get("IMDG"),
          "temp": bkCntr_row.get("TEMP"),
          "cover": bkCntr_row.get("COVER"),
          "awk_x": bkCntr_row.get("AWK_X"),
          "awk_y": bkCntr_row.get("AWK_Y"),
          "awk_z": bkCntr_row.get("AWK_Z"),
          "wgt": bkCntr_row.get("WGT"),
          "dgMix": bkCntr_row.get("DGMIX"),
          "dgList": bkCntr_row.get("DGLIST"),
          "specialInfo": bkCntr_row.get("SPECIALINFO"),
        }
        blDetailInfo.bkCntrs.append(bkCntrs)
          
      for blCntr_row in pResultBlCntr:
        blCntrs = {
          "cntrNo": blCntr_row.get("CONTAINERNO"),
          "sz": blCntr_row.get("CONTAINERSIZE"),
          "tp": blCntr_row.get("CONTAINERTYPE"),
          "sealNo": blCntr_row.get("SEALNO"),
          "pkg": blCntr_row.get("PACKAGEQTY"),
          "pkgcd": blCntr_row.get("PACKAGECODE"),
          "wgt": blCntr_row.get("WEIGHT"),
          "cbm": blCntr_row.get("CBM"),
          "soc": blCntr_row.get("CONTAINEROWNER"),
          "vgm": blCntr_row.get("VGMWEIGHT"),
          "vgmType": blCntr_row.get("VGMMEASUREMETHOD"),
          "vgmSign": blCntr_row.get("VGMSIGN"),
          "vgmCert": blCntr_row.get("VGMCERTIFICATIONNO"),
          "outDemBasic": blCntr_row.get("OUTBOUNDDEMBASICFREEDAY"),
          "outDemAdd": blCntr_row.get("OUTBOUNDDEMADDITIONALFREEDAY"),
          "outDemLimit": blCntr_row.get("OUTBOUNDDEMLIMITDATE"),
          "inDemBasic": blCntr_row.get("INBOUNDDEMBASICFREEDAY"),
          "inDemAdd": blCntr_row.get("INBOUNDDEMADDITIONALFREEDAY"),
          "inDemLimit": blCntr_row.get("INBOUNDDEMLIMITDATE"),
        }
        blDetailInfo.blCntrs.append(blCntrs)
          
      for dg_row in pResultDgSpecial:
        dgSpecials = {
          "cntrSeq": dg_row.get("SEQ"),
          "dgSeq": dg_row.get("DSEQ"),
          "unno": dg_row.get("UNNO"),
          "imdg": dg_row.get("IMDG"),
          "subRisk": dg_row.get("SUBRISK"),
          "pGrade": dg_row.get("POTGRADE"),
          "netWgt": dg_row.get("NETWGT"),
          "grsWgt": dg_row.get("GRSWGT"),
          "pollutant": dg_row.get("POLLUTANT"),
          "limitedQty": dg_row.get("LIMITQTY"),
          "flashPoint": dg_row.get("FLASHPOINT"),
          "sapt": dg_row.get("SAPT"),
          "technicalNm": dg_row.get("TECHNICALNM"),
          "contactNo": dg_row.get("CONTACTNO"),
          "contactNm": dg_row.get("CONTACTNM"),
          "remark": dg_row.get("REMARK"),
          "oPkg": dg_row.get("OPKG"),
          "oPkgCd": dg_row.get("OPKGCD"),
          "oPkgNm": dg_row.get("OPKGNM"),
          "iPkg": dg_row.get("IPKG"),
          "iPkgCd": dg_row.get("IPKGCD"),
          "iPkgNm": dg_row.get("IPKGNM"),
          "casNoList": dg_row.get("CASNOLIST"),
          "isNeedFlashPoint": dg_row.get("ISNEEDFLASHPOINT"),
          "isNeedTechnicalNm": dg_row.get("ISNEEDTECHNICALNM"),
          "isNeedSapt": dg_row.get("ISNEEDSAPT"),
        }
        blDetailInfo.dgSpecials.append(dgSpecials)
          
      for frt_row in pResultFreight:
        freights = {
          "init": frt_row.get("INIT"),
          "name": frt_row.get("NAME"),
          "cur": frt_row.get("CUR"),
          "unit": frt_row.get("UNIT"),
          "usdAmt": frt_row.get("USDAMT"),
          "locAmt": frt_row.get("LOCAMT"),
        }
        blDetailInfo.freights.append(freights)

      for mc_row in pResultManagedCargos:
        managedCargos = {
          "cntrNo": mc_row.get("CNTRNO"),
          "inspectionCargo": mc_row.get("INSPECTION_CARGO"),
          "stNm": mc_row.get("STNM"),
          "xRayNo": mc_row.get("XRAY_NO"),
          "xRayNm": mc_row.get("XRAY_NM"),
        }
        blDetailInfo.managedCargos.append(managedCargos)
          
      self.ResultData.append(blDetailInfo)
    except Exception as ex:
      raise HTTPException(status_code=500, detail=str(ex))
      
  def __setattr__(self, name, value):
    if value == None:
      return object.__setattr__(self, name, "")
    else:
      return object.__setattr__(self, name, value)

class GetFavoriteBL:
  class GetFavoriteBLInfo:
    def __init__(self, row):
      self.BLNO = row.get("BLNO", "") or ""
      self.MSG = row.get("MSG") or ""
      self.CNTR = row.get("CNTR") or ""
      self.POL = row.get("POL") or ""
      self.POD = row.get("POD") or ""
      self.VSL = row.get("VSL") or ""
      self.VSLNM = row.get("VSLNM") or ""
      self.VYG = row.get("VYG") or ""
          
  def __init__(self, db: DBContext, deviceid, token):
    try:
      myBL = db.call_proc("skr_mobile.Pkg_BL.GetFavoriteBL", [deviceid, token])[0]

      self.ResultData = []
      for myBL_row in myBL:
        myBLinfo = self.GetFavoriteBLInfo(myBL_row)
        self.ResultData.append(myBLinfo)
    except Exception as ex:
      raise HTTPException(status_code=500, detail=str(ex))

  def __setattr__(self, name, value):
    if value is None:
      return object.__setattr__(self, name, "")
    else:
      return object.__setattr__(self, name, value)
      
class AddFavoriteBL:
  class AddFavoriteBLInfo:
    def __init__(self, row):
      self.STATUS = row.get("STATUS", "") or ""
      self.MSG = row.get("MSG") or ""
          
  def __init__(self, db: DBContext, deviceid, token, blno, msg):
    try:
      myBL = db.call_proc("skr_mobile.Pkg_BL.AddFavoriteBL", [deviceid, token, blno, msg])[0]

      self.ResultData = []
      for myBL_row in myBL:
        myBLinfo = self.AddFavoriteBLInfo(myBL_row)
        self.ResultData.append(myBLinfo)
    except Exception as ex:
      raise HTTPException(status_code=500, detail=str(ex))

  def __setattr__(self, name, value):
    if value is None:
      return object.__setattr__(self, name, "")
    else:
      return object.__setattr__(self, name, value)
      
class DelFavoriteBL:
  class DelFavoriteBLInfo:
    def __init__(self, row):
      self.STATUS = row.get("STATUS", "") or ""
      self.MSG = row.get("MSG") or ""
          
  def __init__(self, db: DBContext, deviceid, token, blno):
    try:
      myBL = db.call_proc("skr_mobile.Pkg_BL.DelFavoriteBL", [deviceid, token, blno])[0]

      self.ResultData = []
      for myBL_row in myBL:
        myBLinfo = self.DelFavoriteBLInfo(myBL_row)
        self.ResultData.append(myBLinfo)
    except Exception as ex:
      raise HTTPException(status_code=500, detail=str(ex))

  def __setattr__(self, name, value):
    if value is None:
      return object.__setattr__(self, name, "")
    else:
      return object.__setattr__(self, name, value)
      
class GetRecentBL:
  class GetRecentBLInfo:
    def __init__(self, row):
      self.BLNO = row.get("BLNO", "") or ""
      self.CNTR = row.get("CNTR") or ""
      self.POL = row.get("POL") or ""
      self.POD = row.get("POD") or ""
      self.VSL = row.get("VSL") or ""
      self.VSLNM = row.get("VSLNM") or ""
      self.VYG = row.get("VYG") or ""
          
  def __init__(self, db: DBContext, deviceid, token):
    try:
      recentBL = db.call_proc("skr_mobile.Pkg_BL.GetRecentBL", [deviceid, token])[0]

      self.ResultData = []
      for recentBL_row in recentBL:
        recentBLinfo = self.GetRecentBLInfo(recentBL_row)
        self.ResultData.append(recentBLinfo)
    except Exception as ex:
      raise HTTPException(status_code=500, detail=str(ex))

  def __setattr__(self, name, value):
    if value is None:
      return object.__setattr__(self, name, "")
    else:
      return object.__setattr__(self, name, value)
      
class AddRecentBL:
  class AddRecentBLInfo:
    def __init__(self, row):
      self.STATUS = row.get("STATUS", "") or ""
      self.MSG = row.get("MSG") or ""
          
  def __init__(self, db: DBContext, deviceid, token, blno):
    try:
      recentBL = db.call_proc("skr_mobile.Pkg_BL.AddRecentBL", [deviceid, token, blno])[0]

      self.ResultData = []
      for recentBL_row in recentBL:
        recentBLinfo = self.AddRecentBLInfo(recentBL_row)
        self.ResultData.append(recentBLinfo)
    except Exception as ex:
      raise HTTPException(status_code=500, detail=str(ex))

  def __setattr__(self, name, value):
    if value is None:
      return object.__setattr__(self, name, "")
    else:
      return object.__setattr__(self, name, value)
      
class DelRecentBL:
  class DelRecentBLInfo:
    def __init__(self, row):
      self.STATUS = row.get("STATUS", "") or ""
      self.MSG = row.get("MSG") or ""
          
  def __init__(self, db: DBContext, deviceid, token, blno):
    try:
      recentBL = db.call_proc("skr_mobile.Pkg_BL.DelRecentBL", [deviceid, token, blno])[0]

      self.ResultData = []
      for recentBL_row in recentBL:
        recentBLinfo = self.DelRecentBLInfo(recentBL_row)
        self.ResultData.append(recentBLinfo)
    except Exception as ex:
      raise HTTPException(status_code=500, detail=str(ex))

  def __setattr__(self, name, value):
    if value is None:
      return object.__setattr__(self, name, "")
    else:
      return object.__setattr__(self, name, value)

class FindBlNo:
  class FindBlNoInfo:
    def __init__(self, row):
      self.GB = row.get("GB", "") or ""
      self.BLNO = row.get("BLNO", "") or ""
      self.REFNO = row.get("REFNO", "") or ""
      self.POLCD = row.get("POLCD", "") or ""
      self.PODCD = row.get("PODCD", "") or ""
      self.CUSTCD = row.get("CUSTCD", "") or ""
          
  def __init__(self, db: DBContext, token, postfix):
    try:
      findBlNo = db.call_proc("skr_mobile.Pkg_BL.FindBlNo", [token, postfix])[0]

      self.ResultData = []
      for findBlNo_row in findBlNo:
        findBlNoinfo = self.FindBlNoInfo(findBlNo_row)
        self.ResultData.append(findBlNoinfo)
    except Exception as ex:
      raise HTTPException(status_code=500, detail=str(ex))

  def __setattr__(self, name, value):
    if value is None:
      return object.__setattr__(self, name, "")
    else:
      return object.__setattr__(self, name, value)