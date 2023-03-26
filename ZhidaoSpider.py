from fake_useragent import UserAgent
import requests
import time

Session = requests.Session()
ua = UserAgent()

LoginUrl = "https://passport.zhihuishu.com/user/validateCodeAndPassword"
LoginRe = Session.post(url=LoginUrl, data={"code": 2020080301005, "password": "bmw-m3gtr", "schoolId": 1473}, headers={"User-Agent": ua.random})
print("pwd: "+LoginRe.json()["pwd"]+"\n"+"uuid: "+LoginRe.json()["uuid"]+"\n"+"*"*50)

# 所有课程
CourseInfoUrl = "https://onlineservice.zhihuishu.com/student/course/share/queryShareCourseInfo"
CourseInfoRe = Session.post(url=CourseInfoUrl, data={
    "status": 0,
    "pageNo": 1,
    "pageSize": 5,
    "uuid": LoginRe.json()["uuid"],
    "date": "2021-05-23T14:42:59.674Z"
})
ListSize = 0
for CourseInfo in CourseInfoRe.json()["result"]["courseOpenDtos"]:
    ListSize += 1
    CourseName = CourseInfo["courseName"]
    Progress = CourseInfo["progress"]
    print(str(ListSize)+". "+CourseName+": 已完成"+Progress)

