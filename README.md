# zzu-jksb

郑州大学健康上报自动打卡系统

- [X] 打卡成功邮件提醒🔔
- [X] 打卡失败邮件提醒🔔
- [X] 多用户使用
- [X] 环境变量配置
- [X] 兼容系统证书出错问题
- [X] 绿码自动选择(value g)

~~健康码上传提醒🔔~~

## 使用方法

1. fork 本仓库
2. 在 Github action 里面的 `Secrets` > `Actions secrets` > `Environment secrets` 按下面的示例给出对应的环境变量信息。

### 配置用户信息

1. ~~直接编辑 `config.py (不建议因为会暴露个人信息)`~~
2. 通过环境变量给出所需信息（在GitHub action中给出）
   1. 每个信息中间由逗号隔开（密码中不能有逗号）

```text
USER_NAMES=1111,2222
USER_PWDS=1111,2222
USER_EMAILS=me@expoli.tech,me@expoli.tech
EMAIL_SERVER=smtp.163.com
EMAIL_USER=3333@163.com
EMAIL_PWD=1234567890
EMAIL_ADMIN=me@expoli.tech
```

### 开始运行

```shell
pip install -r ./requirements.txt
python ./main.py
```

### 贡献者列表

[@cyberl0afing](https://github.com/cyberl0afing)