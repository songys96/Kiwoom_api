# -*- coding:utf-8 -*-
import os
import time

from pywinauto import application, timings

app = application.Application()

# 네이버 어플을 찾고 해당 다이얼로그를 찾고 거기에 타이핑하는 방법
# (이건 아님)handle = app.findwindows.find_windows(title_re="*")[0]
# 앱을 handle주소를 통해 연결 - SWAPY 어플
app.connect(handle=1049572)
# 원하는 부분에 접근
dlg = timings.wait_until_passes(10, 0.5, lambda:app.window(handle=1049572))
print(dlg)
# 원하는 액션
dlg.type_keys("Hello Naver")
dlg.click()
