from usb_install import *
from info import *
import ParamTestCase
import unittest

current_path = os.getcwd()
report_path = os.path.join(current_path, "report")

# page_name = info.page_name
# page_name = akp_info['tap']['page_name']
# apk_name = akp_info['tap']['apk_name']
# apk_info = akp_info['tap']
# userinfo = user_info['account1']


class dungeonTest(ParamTestCase.ParametrizedTestCase):

    # self.param -> list  [device, account, apk, phone]
    def init(self):
        print(self.param)
        device = self.param[0]
        account = self.param[1]
        target = self.param[2]
        phone = self.param[3]

        dungeonTest.userinfo = user_info[account]
        dungeonTest.apk_info = akp_info[target]
        # 正式使用时才启用
        # dungeonTest.phoneinfo = target

        # 测试时才启用
        dungeonTest.phone = phone
        dungeonTest.phoneinfo = phone_info[phone]

        connect(device)

    @classmethod
    def setUpClass(cls):
        # cls().init()
        pass

    @classmethod
    def tearDownClass(cls):
        stop_app(dungeonTest.apk_info['pakge_name'])
        uninstall(dungeonTest.apk_info['pakge_name'])

    @screenshot
    def test01_appinstall(self):
        self.init()
        init_device("Android")
        # 如果是oppo才执行这个oppo安装
        if dungeonTest.phone == 'oppo':
            thread1 = usb_install_thread()
            thread1.start()
        install(dungeonTest.apk_info['apk_name'])
        start_app(dungeonTest.apk_info['pakge_name'])

    # @screenshot
    @unittest.Myskip
    def test02_login(self):
        # 断言弹出隐私协议弹窗，在断言的api中加入了截图功能
        assert_exists(Template(button['firsttimeinstall']['title']))

        # 点击隐私协议的同意
        touch(Template(button['firsttimeinstall']['OK_bt']))

        # 点击云存档按钮
        touch(Template(button['titlepage']['cloudsave_bt']))

        # 断言弹出实名奖励（此手机已经进行过实名）

        # 如果有链接关闭弹出来的链接
        if exists(Template(button['realname']['link_close'])):
            touch(Template(button['realname']['link_close']))

        # 依次点击断言下一个奖励
        touch(Template(button['realname']['awark1']))
        assert_exists(Template(button['realname']['awark2']))

        touch(Template(button['realname']['awark2']))
        assert_exists(Template(button['realname']['awark3']))
        # assert_exists(Template(button['realname']['awark1']))

        touch(Template(button['realname']['awark3']))

        # 断言是否弹出用户须知界面
        assert_exists(Template(button['userinstructionspage']['title']))

        # debug
        # assert_exists(Template(button['firsttimeinstall']['title']))

        # 等待5秒并点击同意按钮
        sleep(5)
        touch(Template(button['userinstructionspage']['OK_bt']))

        # 断言是否弹出登陆弹窗
        assert_exists(Template(button['loginpage']['pw_bt']))

        # 输入账号密码
        touch(Template(button['loginpage']['account_bt']))
        text(dungeonTest.userinfo['account'])
        sleep(1)
        touch(Template(button['loginpage']['title']))

        touch(Template(button['loginpage']['pw_bt']))
        text(dungeonTest.userinfo['pw'])
        touch(Template(button['loginpage']['title']))
        sleep(1)

        touch(Template(button['loginpage']['login_bt']))

        # 断言登陆成功看到海豹宝宝并点击
        assert_exists(Template(button['cloudsavepage']['haibao']))
        touch(Template(button['cloudsavepage']['haibao']))

        assert_exists(Template(button['cloudsavepage']['upload_bt']))
        assert_exists(Template(button['cloudsavepage']['download_bt']))
        # 断言登陆成功看到上传下载按钮

    # @screenshot
    @unittest.Myskip
    def test03_infocheck(self):

        touch(Template(button['cloudsavepage']['info_bt']))

        assert_exists(Template(button['accountinfopage']['logout_bt']))

        assert_exists(Template(button['accountinfopage']['accounttarget']))

        touch(Template(button['accountinfopage']['close_bt']))

    # @screenshot
    @unittest.Myskip
    def test04_test(self):
        print(654321)


if __name__ == '__main__':

    # unittest.main()

    testsuite = unittest.TestSuite()
    # testsuite.addTest(dungeonTest("test01_appinstall"))
    device = devices_info['oppo_A5']
    account = 'account1'
    apk = 'tap'
    phone = 'oppo'

    param1 = [device, account, apk, phone]

    testsuite.addTest(ParamTestCase.ParametrizedTestCase.parametrize(dungeonTest, param=param1))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(testsuite)

    # 使用testloader
    # TestSuite = unittest.TestSuite()
    # TestLoad = unittest.TestLoader()
    # TestLoad.loadTestsFromTestCase(dungeonTest)
    # TestSuite.addTest(TestLoad.loadTestsFromTestCase(dungeonTest))
    # print(TestLoad.loadTestsFromTestCase(dungeonTest))
    # print(TestLoad.getTestCaseNames(dungeonTest))
    # runner = unittest.TextTestRunner(verbosity=2)
    # runner.run(TestSuite)

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