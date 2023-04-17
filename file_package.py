import os
import zipfile
import socket
import datetime

# 获取本机IP地址
ip = socket.gethostbyname(socket.gethostname())
ip_last = ip.split('.')[-1]

# 获取当前日期
today = datetime.datetime.now().strftime('%Y%m%d')

# 文件路径字典
file_paths = {
    '1': 'D:/测试/temp',
    '2': 'd:/temp1',
    '3': 'd:/temp2'
}

# 用户选择要打包的文件
print('请选择要打包的文件：')
for key in file_paths:
    print(key)
file_choice = input()

# 指定目录
source_dir = file_paths[file_choice]

# 压缩文件输出地址1
output_dir = 'd:/temp'

# 压缩文件命名方式
output_name = ip_last + '_' + today + '.zip'

# 创建压缩文件对象
zf = zipfile.ZipFile(os.path.join(output_dir, output_name), mode='w')

# 遍历指定目录下的所有文件和子目录
for root, dirs, files in os.walk(source_dir):
    for file in files:
        # 获取文件路径
        filepath = os.path.join(root, file)
        # 获取文件修改时间
        modified_date = datetime.datetime.fromtimestamp(os.path.getmtime(filepath)).strftime('%Y%m%d')
        # 如果文件修改时间等于当天日期，则将其添加到压缩文件中
        if modified_date == today:
            zf.write(filepath, arcname=os.path.relpath(filepath, source_dir))

# 关闭压缩文件对象
zf.close()

print('压缩完成！')