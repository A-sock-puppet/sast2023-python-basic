import argparse
import json
from random import choice
import subprocess
import os

def parser_data():
    """
    从命令行读取用户参数
    做出如下约定：
    1. -f 可选参数，表示题库相对路径
    2. -l 可选参数，表示题库语言，默认中文
    3. -i 可选参数，表示指定文章编号，默认随机
    4. -g 可选参数，表示以何种 GUI 界面启动，默认 st

    :return: 参数
    """
    parser = argparse.ArgumentParser(
        prog="python main.py",
        description="A simple game",
        epilog="Example usage:\n"
            "python main.py || \n"
            "python main.py -f example.json -l en -i 2 -g tk",
        allow_abbrev=True
    )

    parser.add_argument("-f", "--file", nargs='?', default='example.json', const='example.json', help="题库文件相对路径，默认 example.json")
    parser.add_argument('-l', '--lang', nargs='?', default='zh', const='zh', help='选择语言 zh/en ，默认中文')
    parser.add_argument('-i', '--id', dest='uid', nargs='?', type=int, default=None, help='指定文章序号，默认随机')
    parser.add_argument('-g', '--gui', nargs='?', const='st', default=None, help='以何种 GUI 界面启动 tk/st ，默认 st')

    args = parser.parse_args()
    return args


def select_article(args, data):
    """
    读取题库文件

    :param args: 所有参数
    :param data: 题库内容

    :return: 一个字典，所选文章信息
    """
    if isinstance(args, dict):
        language, uid = args['lang'], args['uid']
    else:
        language, uid = args.lang, args.uid
    if language == '中文': language = 'zh'
    if language == 'English': language = 'en'
    assert language in ['zh', 'en'], 'No such language!'

    articles = [article for article_group in data for article in article_group['articles'] 
                if article_group['language'] == language]
    
    if uid == None:
        uid = choice(list(range(len(articles))))
    else:
        assert uid in range(len(articles)), f'Article id not in range! Range for language {language}: 0 - {len(articles)-1}'
    
    article = [article for article in articles if article['id'] == uid]
    return article[0]


def get_inputs(hints):
    """
    获取用户输入

    :param hints: 提示信息

    :return: 用户输入的单词
    """
    keys = []
    for hint in hints:
        print(f"请输入一个这样的词汇：{hint}")
        # TODO: 读取一个用户输入并且存储到 keys 当中
        keys.append(input())
    print('----------')
    return keys


def replace(article, keys):
    """
    替换文章内容

    :param article: 文章内容
    :param keys: 用户输入的单词

    :return: 替换后的文章内容

    """
    for i in range(len(keys)):
        # TODO: 将 article 中的 {{i}} 替换为 keys[i]
        # hint: 你可以用 str.replace() 函数，也可以尝试学习 re 库，用正则表达式替换
        placeholder = '{{' + str(i+1) + '}}'
        article = article.replace(placeholder, keys[i])

    return article


if __name__ == "__main__":
    main_dir = os.path.dirname(os.path.abspath(__file__))
    args = parser_data()
    filename = os.path.join(main_dir, args.file)
    with open(filename, 'r', encoding="utf-8") as f:
        data = json.load(f)

    if args.gui:
        if args.gui == 'st':
            articles = [article for article_group in data for article in article_group['articles'] 
                        if article_group['language'] == args.lang]
            if not args.uid:
                args.uid = choice(list(range(len(articles))))
            if not (0 <= args.uid < len(articles)):
                args.uid = 0
            os.environ['MAIN_ARGS'] = json.dumps(vars(args))
            os.environ['MAIN_DATA'] = json.dumps(data)
            gui_path = os.path.join(main_dir, 'gui_streamlit.py')
            subprocess.run(['streamlit', 'run', gui_path])
        else:
            gui_path = os.path.join(main_dir, 'gui_tkinter.py')
            args_dict = vars(args)
            subprocess.run(['python', gui_path, 
                            '--args', json.dumps(args_dict), 
                            '--data', json.dumps(data)])
    else:
        # TODO: 根据参数或随机从 articles 中选择一篇文章
        article = select_article(args, data)

        # TODO: 给出合适的输出，提示用户输入
        # TODO: 获取用户输入并进行替换
        keys = get_inputs(article['hints'])

        # TODO: 给出结果
        article_replaced = replace(article['article'], keys)
        print('最终的文章是：', article_replaced)
