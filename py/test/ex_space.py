
# 打开原始文件和新文件
with open('C:.txt', 'r', encoding='utf-8') as f1, open('C:.txt', 'w', encoding='utf-8') as f2:
    # 逐行读取原始文件内容
    for line in f1:
        # 去除每行的空格和换行符
        line = line.replace('\n', '').replace(' ', '')
        # 将处理后的内容写入新文件
        f2.write(line)

# 关闭文件
f1.close()
f2.close()