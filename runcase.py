#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from AutoTest import *
import sys

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
def suite_case():
     testsuite = unittest.TestSuite()
     testsuite.addTest(dungeonTest("test01_login1"))
     testsuite.addTest(dungeonTest("test02_login"))
     return testsuite


if __name__ == '__main__':

    # unittest.main()

    # 1、获取当前时间，这样便于下面的使用。
    now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    print("自动化测试开始:", now)

    # 2、html报告文件路径
    result_path = os.path.join(report_path,  "result_" + now + ".html")

    # 3、打开一个文件，将result写入此file中
    fp = open(result_path, "wb")
    runner = HTMLTestRunner.HTMLTestRunner(
        stream=fp,
        verbosity=2,
        title=u'自动化测试报告,测试结果如下：',
        description=u'用例执行情况：'
    )

    # 4、调用add_case函数返回值
    runner.run(all_case())  # 参数为选择全部还是选择单独
    fp.close()
    end = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    print("自动化测试结束:", end)
    print("报告路径:", result_path)

