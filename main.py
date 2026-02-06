from fastapi import FastAPI, Query
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse, JSONResponse
import DBContext
from datetime import datetime

import Model.Schedule as Schedule
import Model.Port as Port
import Model.BL as BL
import Model.Tracking as Tracking
import Model.Login as Login
import Model.User as User
import Model.BLDetail as BLDetail
import Model.Map as Map
import Model.Notice as Notice
import Model.Alarm as Alarm
import Model.Print as Print
import Model.Crawling as Crawling

#B/L Detail API
pageApp1 = FastAPI()
@pageApp1.post("/bl-detail/")
async def getData(
  apikey: str = Query("", description="API Key"),
  blno: str = Query("", description="B/L No.", min_length=16, max_length=16)
):
  db = DBContext.DBContext()
  db.open()
  result = BL.BLDetail(db, apikey, blno)
  db.close()
  return result

#Vessel Schedule API
pageApp2 = FastAPI()
@pageApp2.post("/vessel-schedule")
async def getData(
  apikey: str = Query("", description="API Key"),
  vslnm: str = Query("", description="Vessel Name", examples="OSAKA VOYAGER"),
  etd: str = Query("", description="Departure Month(YYYYMM)", min_length=6, max_length=6, examples=datetime.today().strftime("%Y%m"))
):
  db = DBContext.DBContext()
  db.open()
  result = Schedule.VSLSchedule(db, apikey, vslnm, etd)
  db.close()
  return result

#Port Schedule API
pageApp3 = FastAPI()
@pageApp3.post("/port-schedule")
async def getData(
  apikey: str = Query("", description="API Key"),
  portcd: str = Query("", description="Port Code(ISO)", min_length=5, max_length=5, examples="KRPUS"),
  etd: str = Query("", description="Departure Month(YYYYMM)", min_length=6, max_length=6, examples=datetime.today().strftime("%Y%m")),
  wharfcd: str = Query("", description="Wharf Code (Conditional)", min_length=0, max_length=5, examples="PUS05")
):
  db = DBContext.DBContext()
  db.open()
  result = Schedule.PortSchedule(db, apikey, portcd, etd, wharfcd)
  db.close()
  return result

#Port To Port Schedule API
pageApp4 = FastAPI()
@pageApp4.post("/port-to-port-schedule")
async def getData(
  apikey: str = Query("", description="API Key"),
  pol: str = Query("", description="Loading Port Code(ISO)", min_length=5, max_length=5, examples="KRPUS"),
  pod: str = Query("", description="Discharging Port Code(ISO)", min_length=5, max_length=5, examples="CNSHA"),
  etd: str = Query("", description="Departure Month(YYYYMM)", min_length=6, max_length=6, examples=datetime.today().strftime("%Y%m"))
):
  db = DBContext.DBContext()
  db.open()
  result = Schedule.PortToPortSchedule(db, apikey, pol, pod, etd)
  db.close()
  return result

#Tracking API
pageApp5 = FastAPI()
@pageApp5.post("/tracking")
async def getData(
  apikey: str = Query("", description="API Key"),
  blno: str = Query("", description="B/L No.", min_length=16, max_length=16),
  cntrno: str = Query("", description="Container No.", min_length=0, max_length=11)
):
  db = DBContext.DBContext()
  db.open()
  result = Tracking.Tracking(db, apikey, blno, cntrno)
  db.close()
  return result

#Calling Schedule API
pageApp6 = FastAPI()
@pageApp6.post("/calling-schedule")
async def getData(
  apikey: str = Query("", description="API Key"),
  vslnm: str = Query("", description="Vessel Name", examples="OSAKA VOYAGER"),
  vyg: str = Query("", description="Voyage", examples="2339W"),
):
  db = DBContext.DBContext()
  db.open()
  result = Schedule.CallingSchedule(db, apikey, vslnm, vyg)
  db.close()
  return result

#Port List API
pageApp7 = FastAPI()
@pageApp7.post("/portlist")
async def getData():
  db = DBContext.DBContext()
  db.open()
  result = Port.Port(db)
  db.close()
  return result

#Get Login API
pageApp8 = FastAPI()
@pageApp8.post("/getlogin")
async def getData(
  uid: str = Query("", description="User ID"),
  upwd: str = Query("", description="Password")
):
  db = DBContext.DBContext()
  db.open()
  result = Login.GetLogin(db, uid, upwd)
  db.close()
  return result

#Check Login API
pageApp9 = FastAPI()
@pageApp9.post("/chklogin")
async def getData(
  token: str = Query("", description="token")
):
  db = DBContext.DBContext()
  db.open()
  result = Login.ChkLogin(db, token)
  db.close()
  return result

#Profile API
pageApp10 = FastAPI()
@pageApp10.post("/getProfile")
async def getData(
  deviceId: str = Query("", description="device Id"),
  token: str = Query("", description="token"),
  fcmToken: str = Query("", description="fcm token"),
  profile_seq: str = Query("", description="profile sequence"),
):
  db = DBContext.DBContext()
  db.open()
  result = User.GetProfile(db, deviceId, token, fcmToken, profile_seq)
  db.close()
  return result

#Profiles API
pageApp11 = FastAPI()
@pageApp11.post("/getProfiles")
async def getData(
  token: str = Query("", description="token"),
):
  db = DBContext.DBContext()
  db.open()
  result = User.GetProfiles(db, token)
  db.close()
  return result

#Profile Save API
pageApp12 = FastAPI()
@pageApp12.post("/saveProfile")
async def getData(
  token: str = Query("", description="token"),
  profile_seq: str = Query("", description="profile sequence"),
  icon: str = Query("", description="icon"),
  nickname: str = Query("", description="nickname"),
  name: str = Query("", description="name"),
  cellno: str = Query("", description="cellno"),
  email: str = Query("", description="email"),
  telno: str = Query("", description="telno"),
  faxno: str = Query("", description="faxno")
):
  db = DBContext.DBContext()
  db.open()
  result = User.SaveProfile(db, token, profile_seq, icon, nickname, name, cellno, email, telno, faxno)
  db.close()
  return result

#Profile Set API
pageApp13 = FastAPI()
@pageApp13.post("/setProfile")
async def getData(
  deviceid: str = Query("", description="device id"),
  token: str = Query("", description="token"),
  fcmToken: str = Query("", description="fcm token"),
  profile_seq: str = Query("", description="profile sequence"),
):
  db = DBContext.DBContext()
  db.open()
  result = User.SetProfile(db, deviceid, token, fcmToken, profile_seq)
  db.close()
  return result

#Profile Delete API
pageApp14 = FastAPI()
@pageApp14.post("/deleteProfile")
async def getData(
  token: str = Query("", description="token"),
  profile_seq: str = Query("", description="profile sequence"),
):
  db = DBContext.DBContext()
  db.open()
  result = User.DeleteProfile(db, token, profile_seq)
  db.close()
  return result

#User Info API
pageApp15 = FastAPI()
@pageApp15.post("/getUserInfo")
async def getData(
  deviceId: str = Query("", description="device Id"),
  token: str = Query("", description="token"),
):
  db = DBContext.DBContext()
  db.open()
  result = User.GetUserInfo(db, deviceId, token)
  db.close()
  return result

#Mobile Profile Delete API
pageApp16 = FastAPI()
@pageApp16.post("/delMobileProfileInfo")
async def getData(
  deviceId: str = Query("", description="device Id"),
  token: str = Query("", description="token"),
):
  db = DBContext.DBContext()
  db.open()
  result = User.DelMobileProfile(db, deviceId, token)
  db.close()
  return result

#B/L Detail API
pageApp17 = FastAPI()
@pageApp17.post("/getBlDetail")
async def getData(
  deviceId: str = Query("", description="device Id"),
  token: str = Query("", description="token"),
  nacd: str = Query("", description="country code"),
  blno: str = Query("", description="B/L No."),
):
  db = DBContext.DBContext()
  db.open()
  result = BLDetail.GetBlDetail(db, deviceId, token, nacd, blno)
  db.close()
  return result

#Map API
pageApp18 = FastAPI()
@pageApp18.post("/getTrackingMap")
async def getData(
  blno: str = Query("", description="B/L No."),
):
  db = DBContext.DBContext()
  db.open()
  result = Map.TrackingMap(db, blno)
  db.close()
  return result

#B/L List API
pageApp19 = FastAPI()
@pageApp19.post("/getBlList")
async def getData(
  token: str = Query("", description="token"),
  bound: str = Query("", description="bound"),
  fmdt: str = Query("", description="from date"),
  todt: str = Query("", description="to date"),
  pol: str = Query("", description="pol"),
  pod: str = Query("", description="pod"),
):
  db = DBContext.DBContext()
  db.open()
  result = BLList.BLList(db, token, bound, fmdt, todt, pol, pod)
  db.close()
  return result

#My Schedule Get API
pageApp20 = FastAPI()
@pageApp20.post("/getMySchedule")
async def getData(
  token: str = Query("", description="token")
):
  db = DBContext.DBContext()
  db.open()
  result = Schedule.GetMySchedule(db, token)
  db.close()
  return result

#My Schedule Add API
pageApp21 = FastAPI()
@pageApp21.post("/addMySchedule")
async def getData(
  token: str = Query("", description="token"),
  pol: str = Query("", description="pol"),
  pod: str = Query("", description="pod")
):
  db = DBContext.DBContext()
  db.open()
  result = Schedule.AddMySchedule(db, token, pol, pod)
  db.close()
  return result

#My Schedule Delete API
pageApp22 = FastAPI()
@pageApp22.post("/delMySchedule")
async def getData(
  token: str = Query("", description="token"),
  pol: str = Query("", description="pol"),
  pod: str = Query("", description="pod")
):
  db = DBContext.DBContext()
  db.open()
  result = Schedule.DelMySchedule(db, token, pol, pod)
  db.close()
  return result

#Favorite B/L Get API
pageApp23 = FastAPI()
@pageApp23.post("/getFavoriteBL")
async def getData(
  deviceid: str = Query("", description="device id"),
  token: str = Query("", description="token")
):
  db = DBContext.DBContext()
  db.open()
  result = BLDetail.GetFavoriteBL(db, deviceid, token)
  db.close()
  return result

#Favorite B/L Add API
pageApp24 = FastAPI()
@pageApp24.post("/addFavoriteBL")
async def getData(
  deviceid: str = Query("", description="device id"),
  token: str = Query("", description="token"),
  blno: str = Query("", description="blno"),
  msg: str = Query("", description="msg")
):
  db = DBContext.DBContext()
  db.open()
  result = BLDetail.AddFavoriteBL(db, deviceid, token, blno, msg)
  db.close()
  return result

#Favorite B/L Delete API
pageApp25 = FastAPI()
@pageApp25.post("/delFavoriteBL")
async def getData(
  deviceid: str = Query("", description="device id"),
  token: str = Query("", description="token"),
  blno: str = Query("", description="blno")
):
  db = DBContext.DBContext()
  db.open()
  result = BLDetail.DelFavoriteBL(db, deviceid, token, blno)
  db.close()
  return result

#Recent B/L Get API
pageApp26 = FastAPI()
@pageApp26.post("/getRecentBL")
async def getData(
  deviceid: str = Query("", description="device id"),
  token: str = Query("", description="token")
):
  db = DBContext.DBContext()
  db.open()
  result = BLDetail.GetRecentBL(db, deviceid, token)
  db.close()
  return result

#Recent B/L Add API
pageApp27 = FastAPI()
@pageApp27.post("/addRecentBL")
async def getData(
  deviceid: str = Query("", description="device id"),
  token: str = Query("", description="token"),
  blno: str = Query("", description="blno")
):
  db = DBContext.DBContext()
  db.open()
  result = BLDetail.AddRecentBL(db, deviceid, token, blno)
  db.close()
  return result

#Recent B/L Delete API
pageApp28 = FastAPI()
@pageApp28.post("/delRecentBL")
async def getData(
  deviceid: str = Query("", description="device id"),
  token: str = Query("", description="token"),
  blno: str = Query("", description="blno")
):
  db = DBContext.DBContext()
  db.open()
  result = BLDetail.DelRecentBL(db, deviceid, token, blno)
  db.close()
  return result

#Find B/L No. API
pageApp29 = FastAPI()
@pageApp29.post("/findBlNo")
async def getData(
  token: str = Query("", description="token"),
  postfix: str = Query("", description="post fix"),
):
  db = DBContext.DBContext()
  db.open()
  result = BLDetail.FindBlNo(db, token, postfix)
  db.close()
  return result

#Notice API
pageApp30 = FastAPI()
@pageApp30.post("/getNotice")
async def getData(
  nacd: str = Query("", description="nacd"),
  pageIndex: str = Query("", description="page index"),
):
  db = DBContext.DBContext()
  db.open()
  result = Notice.getList(db, nacd, pageIndex)
  db.close()
  return result

#Alarm Update API
pageApp31 = FastAPI()
@pageApp31.post("/updateAlarm")
async def getData(
  deviceId: str = Query("", description="device id"),
  token: str = Query("", description="token"),
  gb: str = Query("", description="gb"),
  val: str = Query("", description="value")
):
  db = DBContext.DBContext()
  db.open()
  result = User.UpdateAlarm(db, deviceId, token, gb, val)
  db.close()
  return result

#Alarm List API
pageApp32 = FastAPI()
@pageApp32.post("/getAlarmList")
async def getData(
  fcm_token: str = Query("", description="fcm token")
):
  db = DBContext.DBContext()
  db.open()
  result = Alarm.GetMsgList(db, fcm_token)
  db.close()
  return result

#Alarm List (No Read) API
pageApp33 = FastAPI()
@pageApp33.post("/getNotReadAlarm")
async def getData(
  fcm_token: str = Query("", description="fcm token")
):
  db = DBContext.DBContext()
  db.open()
  result = Alarm.GetNotReadAlarm(db, fcm_token)
  db.close()
  return result

#Alarm Set Read API
pageApp34 = FastAPI()
@pageApp34.post("/setReadAlarm")
async def getData(
  fcm_token: str = Query("", description="fcm token"),
  refno: str = Query("", description="reference No.")
):
  db = DBContext.DBContext()
  db.open()
  result = Alarm.SetReadAlarm(db, fcm_token, refno)
  db.close()
  return result

#Print Data API
pageApp35 = FastAPI()
@pageApp35.post("/getPrintData")
async def getData(
  nacd: str = Query("", description="Nation code"),
  token: str = Query("", description="Token"),
  div: str = Query("", description="Division of document"),
  blno: str = Query("", description="B/L No.")
):
  db = DBContext.DBContext()
  db.open()
  result = Print.GetPrintData(db, nacd, token, div, blno)
  db.close()
  return result

#Terminal Data API
pageApp36 = FastAPI()
@pageApp36.post("/getTerminalData")
async def getData(
  vslnm: str = Query("", description="Vessel Name")
):
  result = await Crawling.search_ship_schedules(vslnm)
  return result

#Main FastAPI App 생성 및 페이지 앱 등록
app = FastAPI()
app.mount("/bl-detail", pageApp1)
app.mount("/vessel-schedule", pageApp2)
app.mount("/port-schedule", pageApp3)
app.mount("/port-to-port-schedule", pageApp4)
app.mount("/tracking", pageApp5)
app.mount("/calling-schedule", pageApp6)
app.mount("/getlogin", pageApp8)
app.mount("/chklogin", pageApp9)
app.mount("/getProfile", pageApp10)
app.mount("/getProfiles", pageApp11)
app.mount("/saveProfile", pageApp12)
app.mount("/setProfile", pageApp13)
app.mount("/deleteProfile", pageApp14)
app.mount("/getUserInfo", pageApp15)
app.mount("/delMobileProfileInfo", pageApp16)
app.mount("/getBlDetail", pageApp17)
app.mount("/getTrackingMap", pageApp18)
app.mount("/getBlList", pageApp19)
app.mount("/getMySchedule", pageApp20)
app.mount("/addMySchedule", pageApp21)
app.mount("/delMySchedule", pageApp22)
app.mount("/getFavoriteBL", pageApp23)
app.mount("/addFavoriteBL", pageApp24)
app.mount("/delFavoriteBL", pageApp25)
app.mount("/getRecentBL", pageApp26)
app.mount("/addRecentBL", pageApp27)
app.mount("/delRecentBL", pageApp28)
app.mount("/findBlNo", pageApp29)
app.mount("/getNotice", pageApp30)
app.mount("/updateAlarm", pageApp31)
app.mount("/getAlarmList", pageApp32)
app.mount("/getNotReadAlarm", pageApp33)
app.mount("/setReadAlarm", pageApp34)
app.mount("/getPrintData", pageApp35)
app.mount("/getTerminalData", pageApp36)