东南大学绩点计算
感觉数智东南的绩点计算不好用 所以在这里自己写了一个
数据来源于东南大学网上办事服务大厅
因为本人没有转专业 挂科 重修 补考这些特殊情况 所以某些情况可能会报错
如果有这些情况愿意提供一卡通号和密码进行测试 我可以在以后更新上

将main.py中的第134行
web.login(" 一卡通号", "密码")
一卡通号和密码修改为自己的一卡通号和密码
然后运行 即可正常使用

chromedriver.exe需要换成适配自己chrome浏览器的版本
这里使用的是126版本
