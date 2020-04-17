#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from AutoTest import *
import HTMLTestRunner
import sys
from multiprocessing.pool import Pool
from info import *

# 获取用例的执行路径
def getpath():

    # 当前文件路径
    case_path = os.path.join(sys.path[0])
    return case_path


# 指定名字的py文件，如果按照一定格式可以用'test*.py'
def all_case():
    case_path = getpath()
    discover = unittest.defaultTestLoader.discover(case_path, pattern="AutoTest.py", top_level_dir=None)

    print(discover)
    return discover


# 部分用例
def suite_case(info_list=None):
     testsuite = unittest.TestSuite()
     # testsuite.addTest(dungeonTest("test01_appinstall"))
     testsuite.addTest(ParamTestCase.ParametrizedTestCase.parametrize(dungeonTest, param=info_list))
     # testsuite.addTest(dungeonTest("test02_login"))
     return testsuite


def run(mode=1, info_list=None, now='1000', processId='0'):
    # now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    now = now
    processId = os.getpid()
    print('子进程ID：{0}，创建进程成功'.format(processId))
    print("自动化测试开始:", now)

    if mode == 1:
        test = suite_case(info_list)
    else:
        test = all_case()

    # 2、html报告文件路径
    result_path = os.path.join(report_path, "result_" + info_list[0] + '_' + now + ".html")

    # 3、打开一个文件，将result写入此file中
    fp = open(result_path, "wb")
    runner = HTMLTestRunner.HTMLTestRunner(
        stream=fp,
        verbosity=2,
        title=u'自动化测试报告,测试结果如下：',
        description=u'用例执行情况：'
    )

    # 4、调用add_case函数返回值
    runner.run(test)  # 参数为选择全部还是选择单独
    fp.close()
    end = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    print("自动化测试结束:", end)
    print("报告路径:", result_path)


if __name__ == '__main__':
    # suite = unittest.TestSuite()
    # suite.addTest(ParamTestCase.ParametrizedTestCase.parametrize(dungeonTest, param=None))
    # unittest.TextTestRunner(verbosity=2).run(suite)

    print("父进程开始")
    runinfo = run_info

    isrun = True

    adb = ADB()
    deviceslist = adb.devices()
    offline_device = None
    if len(deviceslist) >= 2:
        for i in range(len(runinfo)):
            if adb.devices()[i][0] not in devices_info.values():
                isrun = False
                offline_device = adb.devices()[i][0]
                print('{0} is not ready'.format(offline_device))
                break
            else:
                print('{0} devices is all ready'.format(devices_info.values()))

    # if isrun:
    p = Pool(8)

    now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))

    for i in range(1, len(runinfo) + 1):
        p.apply_async(run, args=(1, runinfo[i], now,))

    # for i in range(1, 3):
    #     p.apply_async(run, args=(1, runinfo[i], now,))

    p.close()
    p.join()
    print("父进程结束")




    # device1 = devices_info['oppo_A83']
    # device2 = devices_info['oppo_A5']
    #
    # account1 = user_info['account1']
    # account2 = user_info['account2']
    #
    # apk1 = user_info
    #
    # now1 = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    # p1 = Process(target=run, args=(1, [device1, ], now1))
    # p1.start()
    # time.sleep(5)
    # now2 = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    # p2 = Process(target=run, args=(1, device2, now2))
    # p2.start()

    # # unittest.main()
    #
    # # 1、获取当前时间，这样便于下面的使用。
    # now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    # print("自动化测试开始:", now)
    #
    # # 2、html报告文件路径
    # result_path = os.path.join(report_path,  "result_" + now + ".html")
    #
    # # 3、打开一个文件，将result写入此file中
    # fp = open(result_path, "wb")
    # runner = HTMLTestRunner.HTMLTestRunner(
    #     stream=fp,
    #     verbosity=2,
    #     title=u'自动化测试报告,测试结果如下：',
    #     description=u'用例执行情况：'
    # )
    #
    # # 4、调用add_case函数返回值
    # runner.run(suite_case())  # 参数为选择全部还是选择单独
    # fp.close()
    # end = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    # print("自动化测试结束:", end)
    # print("报告路径:", result_path)

