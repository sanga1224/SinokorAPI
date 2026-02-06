import oracledb
from fastapi import HTTPException

class BLDetail:
  class BLInfo:
    def __init__(self, row):
      self.BLNO = row.get("BLNO") or ""
      self.ShipperName = row.get("SHIPPERNAME") or ""
      self.ShipperAddress = row.get("SHIPPERADDRESS") or ""
      self.ConsigneeName = row.get("CONSIGNEENAME") or ""
      self.ConsigneeAddress = row.get("CONSIGNEEADDRESS") or ""
      self.NotifyName = row.get("NOTIFYNAME") or ""
      self.NotifyAddress = row.get("NOTIFYADDRESS") or ""
      self.VesselCode = row.get("VESSELCODE") or ""
      self.VesselName = row.get("VESSELNAME") or ""
      self.VoyageNumber = row.get("VOYAGENUMBER") or ""
      self.ETD = row.get("ETD") or ""
      self.ETA = row.get("ETA") or ""
      self.ReceiptportCode = row.get("RECEIPTPORTCODE") or ""
      self.ReceiptportName = row.get("RECEIPTPORTNAME") or ""
      self.LoadingPortCode = row.get("LOADINGPORTCODE") or ""
      self.LoadingPortName = row.get("LOADINGPORTNAME") or ""
      self.DischargingPortCode = row.get("DISCHARGINGPORTCODE") or ""
      self.DischargingPortName = row.get("DISCHARGINGPORTNAME") or ""
      self.DeliveryPortCode = row.get("DELIVERYPORTCODE") or ""
      self.DeliveryPortName = row.get("DELIVERYPORTNAME") or ""
      self.FinalDestinationPortCode = row.get("FINALDESTINATIONPORTCODE") or ""
      self.FinaldestinationPortName = row.get("FINALDESTINATIONPORTNAME") or ""
      self.CargoTerm = row.get("CARGOTERM") or ""
      self.FreightTerm = row.get("FREIGHTTERM") or ""
      self.CargoType = row.get("CARGOTYPE") or ""
      self.IssuedType = row.get("ISSUEDTYPE") or ""
      self.PackageQuantity = row.get("PACKAGEQTY") or ""
      self.PackageUnitCode = row.get("PACKAGEUNITCODE") or ""
      self.PackageUnitName = row.get("PACKAGEUNITNAME") or ""
      self.Weight = row.get("WEIGHT") or ""
      self.CBM = row.get("CBM") or ""
      self.Mark = None  # CLOB 타입 변환하여 사용하였으나 변환 시간이 오래걸려 초기화 후 나중에 매칭
      self.Description = None  # CLOB 타입 변환하여 사용하였으나 변환 시간이 오래걸려 초기화 후 나중에 매칭
      self.SAY = row.get("SAY") or ""
      self.MainItem = row.get("MAINITEM") or ""
      self.HS_Code = row.get("HSCODE") or ""
      self.HS_Name = row.get("HSNAME") or ""
      self.AFR_ShipperNationCode = row.get("AFRSHIPPERNATIONCODE") or ""
      self.AFR_ShipperTelNo = row.get("AFRSHIPPERTELNO") or ""
      self.AFR_ShipperBizType = row.get("AFRSHIPPERBIZTYPE") or ""
      self.AFR_ShipperBizNo = row.get("AFRSHIPPERBIZNO") or ""
      self.AFR_ShipperExportNo = row.get("AFRSHIPPEREXPORTNO") or ""
      self.AFR_ShipperGstNo = row.get("AFRSHIPPERGSTNO") or ""
      self.AFR_ConsigneeNationCode = row.get("AFRCONSIGNEENATIONCODE") or ""
      self.AFR_ConsigneeTelNo = row.get("AFRCONSIGNEETELNO") or ""
      self.AFR_ConsigneeBizType = row.get("AFRCONSIGNEEBIZTYPE") or ""
      self.AFR_ConsigneeBizNo = row.get("AFRCONSIGNEEBIZNO") or ""
      self.AFR_ConsigneePIC = row.get("AFRCONSIGNEEPIC") or ""
      self.AFR_ConsigneePICTelNo = row.get("AFRCONSIGNEEPICTELNO") or ""
      self.AFR_ConsigneeEmail = row.get("AFRCONSIGNEEEMAIL") or ""
      self.AFR_ConsigneeImportNo = row.get("AFRCONSIGNEEIMPORTNO") or ""
      self.AFR_ConsigneedePositNo = row.get("AFRCONSIGNEEDEPOSITNO") or ""
      self.AFR_NotifyNationCode = row.get("AFRNOTIFYNATIONCODE") or ""
      self.AFR_NotifyTelNo = row.get("AFRNOTIFYTELNO") or ""
      self.AFR_NotifyBizType = row.get("AFRNOTIFYBIZTYPE") or ""
      self.AFR_NotifyBizNo = row.get("AFRNOTIFYBIZNO") or ""
      self.AFR_NotifyEmail = row.get("AFRNOTIFYEMAIL") or ""
      self.AFR_ShipperPostNo = row.get("AFRSHIPPERPOSTNO") or ""
      self.AFR_ShipperCityName = row.get("AFRSHIPPERCITYNAME") or ""
      self.AFR_InvoiceCurrency = row.get("AFRINVOICECURRENCY") or ""
      self.AFR_InvoiceAmount = row.get("AFRINVOICEAMOUNT") or ""
      self.AFR_ConsigneePostNo = row.get("AFR_CONSIGNEEPOSTNO") or ""
      self.AFR_ConsigneeCityName = row.get("AFRCONSIGNEECITYNAME") or ""
      self.AFR_ConsigneeGstNo = row.get("AFRCONSIGNEEGSTNO") or ""
      self.AFR_NotifyPostNo = row.get("AFRNOTIFYPOSTNO") or ""
      self.AFR_NotifyCityName = row.get("AFRNOTIFYCITYNAME") or ""
      self.AFR_NotifyImportNo = row.get("AFRNOTIFYIMPORTNO") or ""
      self.AFR_NotifyGstNo = row.get("AFRNOTIFYGSTNO") or ""
      self.ContainerInfo = []

      self.handle_lob(row)

    def handle_lob(self, row):
      # CLOB 값을 문자열로 변환하여 저장
      self.Mark = self.handle_clob(row.get("MARK"))
      self.Description = self.handle_clob(row.get("DESCRIPTION"))

    def handle_clob(self, lob):
      if isinstance(lob, oracledb.LOB):
        return lob.read()
      else:
        return lob

    @property
    def MARK(self):
      if isinstance(self._Mark, oracledb.LOB):
        self._Mark = self._Mark.read()
      return self._Mark

    @MARK.setter
    def MARK(self, value):
      self._Mark = value

    @property
    def DESCRIPTION(self):
      if isinstance(self._Description, oracledb.LOB):
        self._Description = self._Description.read()
      return self._Description

    @DESCRIPTION.setter
    def DESCRIPTION(self, value):
      self._Description = value

  class ContainerInfo:
    def __init__(self, row):
      # self.apistatus = row.get("APISTATUS")
      self.ContainerNo = row.get("CONTAINERNO") or ""
      self.ContainerSize = row.get("CONTAINERSIZE") or ""
      self.ContainerType = row.get("CONTAINERTYPE") or ""
      self.SealNo = row.get("SEALNO") or ""
      self.PackageQuantity = row.get("PACKAGEQTY") or ""
      self.PackageCode = row.get("PACKAGECODE") or ""
      self.Weight = row.get("WEIGHT") or ""
      self.CBM = row.get("CBM") or ""
      self.TareWeight = row.get("TAREWEIGHT") or ""
      self.Cargo = row.get("CARGO") or ""
      self.ContainerOwner = row.get("CONTAINEROWNER") or ""
      self.VGM_Weight = row.get("VGMWEIGHT") or ""
      self.VGM_Sign = row.get("VGMSIGN") or ""
      self.VGM_MeasureMethod = row.get("VGMMEASUREMETHOD") or ""
      self.VGM_CertificationNo = row.get("VGMCERTIFICATIONNO") or ""
      self.OutboundDEMBasicFreeday = row.get("OUTBOUNDDEMBASICFREEDAY") or ""
      self.OutboundDEMAdditionalFreeday = (
          row.get("OUTBOUNDDEMADDITIONALFREEDAY") or ""
      )
      self.OutboundDEMLimitDate = row.get("OUTBOUNDDEMLIMITDATE") or ""
      self.InboundDEMBasicFreeday = row.get("INBOUNDDEMBASICFREEDAY") or ""
      self.InboundDEMAdditionalFreeday = (
          row.get("INBOUNDDEMADDITIONALFREEDAY") or ""
      )
      self.InboundDEMLimitDate = row.get("INBOUNDDEMLIMITDATE") or ""

  def __init__(self, db: DBContext, apikey, blno):
    try:
      bldetail = db.call_proc("Pkg_API.getBL", [apikey, blno])[0]
      self.ResultData = []

      for bl_row in bldetail:
        apistatus = bl_row.get("APISTATUS")
        if apistatus == "N":
          apimsg = bl_row.get("APIMSG")
          raise Exception(apimsg)
        else:
          # self.ResultData.append(self.BLInfo(bl_row))
          blinfo = self.BLInfo(bl_row)
          cntrdetail = db.call_proc("Pkg_API.getCNTR", [blno])[0]
          for cntr_row in cntrdetail:
            cntrinfo = self.ContainerInfo(cntr_row)
            blinfo.ContainerInfo.append(cntrinfo)  # ContainerInfo 항목에 넣어줌.
        self.ResultData.append(blinfo)

    except Exception as ex:
      raise HTTPException(status_code=500, detail=str(ex))

  def __setattr__(self, name, value):
    if value is None:
      return object.__setattr__(self, name, "")
    else:
      return object.__setattr__(self, name, value)