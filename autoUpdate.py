# -*- coding:utf-8 -*-
import os
import time

from pywinauto import application, timings

app = application.Application()
app.connect(timeout=3, retry_interval=0.5,process=133932912)
app.start("C:Kiwoom/KiwoomFalsh2/khministarter.exe")

title = '번개 Login'
dlg = timings.wait_until_passes(20,0.5, lambda:app.window(title=title))

pass_ctrl = dlg.Edit2
pass_ctrl.set_focus()
pass_ctrl.type_keys("ID")

cert_ctrl = dlg.Edit3
cert_ctrl.set_focus()
cert_ctrl.type_keys("PW")

btn_ctrl = dlg.Button0
btn_ctrl.click()

time.sleep(50)
os.system("taskkill /im khmini.exe")
