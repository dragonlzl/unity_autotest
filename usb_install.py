from airtest.core.api import *
from airtest.core.android.android import *
import threading
import time
import getimagepath
from info import *


button = getimagepath.png_dict()

oppo_info = phone_info['oppo']
device_info =devices_info


# 装包用的线程
class usb_install_thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        try :
            usb_install()
        except Exception:
            raise AssertionError



def usb_install(phone='oppo'):
    phone = phone_info[phone]
    try:
        sleep(10)
        if exists(Template(button['install']['pw_btn'])):
            touch(Template(button['install']['pw_btn']))
            sleep(1)
            text(phone['pw'])
            sleep(2)
            # touch(Template("image/install/button_image/install.png"))
        if exists(Template(button['install']['install'])):
            touch(Template(button['install']['install']))
            sleep(5)

        if exists(Template(button['install']['c_install'])):
            sleep(4)
            touch(Template(button['install']['c_install']))
            sleep(2)

        assert_exists(Template(button['install']['app_install']))
        # assert_exists(Template(button['install']['pw_btn']))
    # assert_exists(Template(button['install']['app_install']), filename=str(int(time.time())))

        touch(Template(button['install']['app_install']))

        sleep(10)
    except Exception as e:
        # screenhot()
        print('install err: ', e)
        raise Exception


# def screenhot():
#     path = os.getcwd()
#     dir = os.path.join(path, 'bug_image', now)
#     isExists = os.path.exists(dir)
#     if not isExists:
#         os.makedirs(dir)
#         print(dir)
#     snapshot(os.path.join(dir, str(int(time.time())) + '.png'))


# 选择设备（旧版）
def devices_choice(i=0):
    devicesList = get_devices()
    if len(devicesList) >= 2:

        # 连接手机 默认连接方式
        connect_device("android:///")

        # 指定设备号连接
        connect_device("android:///" + devicesList[i][0])


# 获取设备列表
def get_devices():
    adb = ADB()
    adb.check_app()
    devicesList = adb.devices()
    return devicesList


# 检查包体是否存在
def checkapp(pakge):
    adb = ADB()
    if adb.check_app(pakge):
        return True
    else:
        return False



# 选择设备
def connect(devices=None):
    try:
        print('正在连接设备：', devices)
        if devices in device_info.keys():
            connect_device("android:///")
            connect_device("android:///" + device_info[devices])
        elif devices in device_info.values():
            connect_device("android:///")
            connect_device("android:///" + devices)
        elif devices == None:
            devicesList = get_devices()
            if len(devicesList) >= 2:
                # 连接手机 默认连接方式
                connect_device("android:///")

                # 指定设备号连接
                connect_device("android:///" + devicesList[0][0])
    except Exception as e:
        print('connect to adb error: ', e)
        raise AssertionError


if __name__ == '__main__':
    print(get_devices())