with open('D:\Doc\ChatGIS\\zhiwiki.txt', 'r', encoding='utf-8') as f:
    # 读取前500行
    lines = f.readlines()[:500]

# 打开新文件
with open('D:\Doc\ChatGIS\\new.txt', 'w', encoding='utf-8') as f:
    # 写入前500行
    f.writelines(lines)