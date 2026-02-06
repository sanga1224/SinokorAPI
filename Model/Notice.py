from fastapi import HTTPException

class getList:
  class getListInfo:
    def __init__(self, row):
      self.nacd = row.get("NACD")
      self.seq = row.get("NUM")
      self.title = row.get("TITLE")
      self.inpdate = row.get("INPDATE")

  def __init__(self, db: DBContext, nacd, pageIndex):
    try:
      notice = db.call_proc("skr_mobile.Pkg_Account.GetNoticeList", [nacd])[0]            

      self.ResultData = []
      for notice_row in notice:
        noticeinfo = self.getListInfo(notice_row)
        self.ResultData.append(noticeinfo)
    except Exception as ex:
      raise HTTPException(status_code=500, detail=str(ex))

  def __setattr__(self, name, value):
    if value == None:
      return object.__setattr__(self, name, "")
    else:
      return object.__setattr__(self, name, value)