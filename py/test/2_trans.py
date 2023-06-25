import opencc

# 设置转换器
converter = opencc.OpenCC('t2s')

# 打开要转换的文件
with open('D:\\Doc\\ChatGIS\\zhiwiki.txt', 'r', encoding='utf-8') as f:#更换自己的zhiwiki.txt文件路径
    # 逐块读取文件内容
    while True:
        content = f.read(100 * 1024 * 1024)  # 每次读取100MB
        if not content:
            break
        # 将繁体转换为简体
        converted_content = converter.convert(content)
        # 将转换后的内容写入新文件
        with open('D:\Doc\ChatGIS\wikisimple.txt', 'a', encoding='utf-8') as f_out:#更换自己的输出文件路径
            f_out.write(converted_content)