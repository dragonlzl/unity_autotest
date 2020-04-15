from airtest.core.api import *
from airtest.core.android.android import *
import threading
import unittest
import time
import getimagepath
import HTMLTestRunner


button = getimagepath.png_dict()
page_name = 'com.ChillyRoom.DungeonShooter'
apk_name = 'TapTap-2.6.1.apk'
oppo_info = {'pw': ''}
user_info = {'account':  '', 'pw': ''}

current_path = os.getcwd()
report_path = os.path.join(current_path, "report")
now = now


# 装包用的线程
class usb_install_thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        usb_install()


def usb_install():
    try:
        sleep(5)
        if exists(Template(button['install']['pw_btn'])):
            touch(Template(button['install']['pw_btn']))
            sleep(1)
            text(oppo_info['pw'])
            sleep(2)
            # touch(Template("image/install/button_image/install.png"))
            touch(Template(button['install']['install']))
            sleep(3)

        if exists(Template(button['install']['c_install'])):
            sleep(2)
            touch(Template(button['install']['c_install']))
            sleep(2)

        assert_exists(Template(button['install']['app_install']))
        # assert_exists(Template(button['install']['app_install']), filename=str(int(time.time())))
        # assertManager.assertPage(assert_exists(Template(button['install']['app_install']), filename=str(int(time.time()))))

        touch(Template(button['install']['app_install']))

        sleep(3)
    except Exception as e:
        screenhot()
        print('install err: ', e)
        raise Exception


def screenhot():
    path = os.getcwd()
    dir = os.path.join(path, 'bug_image', now)
    isExists = os.path.exists(dir)
    if not isExists:
        os.makedirs(dir)
        print(dir)
    snapshot(os.path.join(dir, str(int(time.time())) + '.png'))

# 选择设备
def devices_choice(i=0):
    # 获得当前设备列表
    adb = ADB()
    devicesList = adb.devices()
    if len(devicesList) >= 2:

        # 连接手机 默认连接方式
        connect_device("android:///")

        # 指定设备号连接
        connect_device("android:///" + devicesList[i][0])


class dungeonTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        devices_choice(1)
        init_device("Android")
        thread1 = usb_install_thread()
        thread1.start()
        install(apk_name)
        start_app(page_name)

    @classmethod
    def tearDownClass(cls):
        stop_app(page_name)
        uninstall(page_name)

    def test01_login1(self):
        raise AssertionError

    @unittest.Myskip
    def test02_login(self):
        # 断言弹出隐私协议弹窗，在断言的api中加入了截图功能
        # assert_exists(Template(button['firsttimeinstall']['title']), filename=str(int(time.time())))
        assert_exists(Template(button['firsttimeinstall']['title']))

        # 点击隐私协议的同意
        touch(Template(button['firsttimeinstall']['OK_bt']))

        # 点击云存档按钮
        touch(Template(button['titlepage']['cloudsave_bt']))

        # 断言弹出实名奖励（此手机已经进行过实名）

        # assert_exists(Template(button['realname']['link_close']), filename=str(int(time.time())))

        # # 关闭弹出来的链接
        # touch(Template(button['realname']['link_close']))

        # 如果有链接关闭弹出来的链接
        if exists(Template(button['realname']['link_close'])):
            touch(Template(button['realname']['link_close']))

        # 依次点击断言下一个奖励
        touch(Template(button['realname']['awark1']))
        # assert_exists(Template(button['realname']['awark2']), filename=str(int(time.time())))
        assert_exists(Template(button['realname']['awark2']))

        touch(Template(button['realname']['awark2']))
        assert_exists(Template(button['realname']['awark3']))
        # assert_exists(Template(button['realname']['awark3']), filename=str(int(time.time())))
        # creathtml('aaaa', 'bbbb')
        # debug
        # assert_exists(Template(button['realname']['awark2']), filename=str(int(time.time())))
        assert_exists(Template(button['realname']['awark1']))

        touch(Template(button['realname']['awark3']))

        # 断言是否弹出用户须知界面
        assert_exists(Template(button['userinstructionspage']['title']))
        # assert_exists(Template(button['userinstructionspage']['title']),
        #               filename=str(int(time.time())))

        # 等待5秒并点击同意按钮
        sleep(5)
        touch(Template(button['userinstructionspage']['OK_bt']))

        # 断言是否弹出登陆弹窗
        # assert_exists(Template(button['loginpage']['pw_bt']), filename=str(int(time.time())))
        assert_exists(Template(button['loginpage']['pw_bt']))

        # 输入账号密码
        touch(Template(button['loginpage']['account_bt']))
        text(user_info['account'])
        sleep(1)
        touch(Template(button['loginpage']['title']))

        touch(Template(button['loginpage']['pw_bt']))
        text(user_info['pw'])
        touch(Template(button['loginpage']['title']))
        sleep(1)

        touch(Template(button['loginpage']['login_bt']))

        # 断言登陆成功看到海豹宝宝并点击
        # assert_exists(Template(button['cloudsavepage']['haibao']), filename=str(int(time.time())))
        assert_exists(Template(button['cloudsavepage']['haibao']))
        touch(Template(button['cloudsavepage']['haibao']))
        # assert_exists(Template(button['cloudsavepage']['upload_bt']),
        #               filename=str(int(time.time())))
        # assert_exists(Template(button['cloudsavepage']['download_bt']),
        #               filename=str(int(time.time())))
        assert_exists(Template(button['cloudsavepage']['upload_bt']))
        assert_exists(Template(button['cloudsavepage']['download_bt']))
        # 断言登陆成功看到上传下载按钮

        sleep(10)

    def test03_test(self):
        print(123456)

    @unittest.Myskip
    def test04_test(self):
        print(654321)

def creathtml(path, pic):
    html = ''
    if len(path) > 0:
        for i in range(len(path)):
            if i == 0:
                html = '<a href=' + path[i] + ' target="_blank">' + pic[i] + '</a>'
            else:
                html = html + '<br /><a href=' + path[i] + ' target="_blank">' + pic[i] + '</a>'
    else:
        html = ''
    htmls = 'htmlbegin<td>' + html +'</td>htmlend'
    return htmls

if __name__ == '__main__':

    # unittest.main()

    # 使用testloader
    TestSuite = unittest.TestSuite()
    TestLoad = unittest.TestLoader()
    TestLoad.loadTestsFromTestCase(dungeonTest)
    TestSuite.addTest(TestLoad.loadTestsFromTestCase(dungeonTest))
    print(TestLoad.loadTestsFromTestCase(dungeonTest))
    print(TestLoad.getTestCaseNames(dungeonTest))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(TestSuite)

    # result_path = os.path.join(report_path, str(int(time.time())) + "_result.html")
    #
    # fp = open(result_path, "wb")
    #
    # TestSuite = unittest.TestSuite()
    # TestSuite.addTest(dungeonTest('test01_login'))
    #
    # # runner = unittest.TextTestRunner(verbosity=2)
    # runner = HTMLTestRunner.HTMLTestRunner(stream=fp,
    #                                        title="测试报告",
    #                                        description="用例执行情况")
    #
    # runner.run(TestSuite)
    # fp.close()

# # connect an android phone with adb
# init_device("Android")
# # or use connect_device api
# # connect_device("Android:///")
#
# # install("path/to/your/apk")
# start_app("com.ChillyRoom.DungeonShooter")
# sleep(5)
# touch(Template("image/titlepage/button_image/cloudsave_bt.png"))
# assert_exists(Template("image/loginpage/button_image/logintext.png"))
# touch(Template("image/loginpage/button_image/pw_bt.png"))
# sleep(5)
# text('18680340380')
# sleep(5)
# touch(Template("image/loginpage/button_image/login_bt.png"))
# sleep(5)
# touch(Template("image/loginpage/button_image/login_bt.png"))
# sleep(5)
# try:
#     assert_exists(Template("image/cloudsavepage/accountinfopage/button_image/close_bt.png"))
# except AssertionError as a:
#     print('error: ', a)
# # swipe(Template("slide_start.png"), Template("slide_end.png"))
# # assert_exists(Template("success.png"))
# # keyevent("BACK")
# # home()
# # uninstall("package_name_of_your_apk")