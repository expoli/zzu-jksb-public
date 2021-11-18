# zzu-jksb

郑州大学健康上报自动打卡系统

- [x] 打卡成功邮件提醒🔔
- [x] 打卡失败邮件提醒🔔
- [x] 健康码上传提醒🔔
- [x] 多用户使用
- [x] 环境变量配置
- [x] 兼容系统证书出错问题
- [x] 绿码自动选择(value g)

## 使用方法

### 配置用户信息

1. 直接编辑 `config.py`
2. 通过环境变量给出所需信息

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
