from pathlib import Path
from bs4 import BeautifulSoup
import configparser


class MediaSearch:
    def __init__(self, base_path):
        self.base_path = base_path
        self.soups = {}

    # HTMLファイル読み込み(既に同名ファイルを読み込んでいた場合はスキップ)
    def get_soup(self, media_type):
        file_path = self.base_path + f"{media_type}.htm"
        if file_path not in self.soups:
            try:
                hfile = Path(file_path)
                htext = hfile.read_text(encoding='utf-8')
                self.soups[file_path] = BeautifulSoup(htext, 'html.parser')
            except FileNotFoundError:
                print(f"ファイル[{file_path}]が見つかりませんでした。")
                return None
        return self.soups[file_path]

    # HTMLファイルから指定した単語でサーチ
    def search_media(self, media_type, search_text):
        soup = self.get_soup(media_type)
        if soup:
            # スペースで分割して配列に格納
            search_terms = search_text.split()
            target_elements = []

            for element in soup.find_all(['div', 'dir'], {'class': ['file', 'dir']}):
                text = element.text.strip()
                terms_found = all(term in text for term in search_terms)
                if terms_found:
                    target_elements.append(text)

            if target_elements:
                return '\n'.join(target_elements)
            else:
                return f"該当する要素は[{media_type}]では見つかりませんでした。"


# iniファイルから基本設定を読み込む関数
def read_settings_from_ini(file_path):
    config = configparser.ConfigParser()
    config.read(file_path, encoding='utf-8')
    base_path = config.get('Settings', 'base_path')
    return base_path


# iniファイルからリストを読み込む関数
def read_lists_from_ini(file_path):
    config = configparser.ConfigParser()
    config.read(file_path, encoding='utf-8')
    lists = dict(config['Lists'])
    return lists


# メイン関数
def main():
    # iniファイルから設定を読み込む
    base_path = read_settings_from_ini('Lists.ini')
    # iniファイルからリストを読み込む
    lists = read_lists_from_ini('Lists.ini')
    # MediaSearchクラスを初期化
    media_search = MediaSearch(base_path)

    while True:
        # 番号リストを表示
        print("検索したいリストを選んでください：")
        for key, value in lists.items():
            print(f"{key}: {value}")
        print("99: 全てのリストを読み込む")
        print("999: プログラムを終了")

        # 数値を入力してリストを選択
        option = input("番号を入力してください：")
        if option == "999":
            print("プログラムを終了します。")
            break

        try:
            # 選択したリストからサーチ
            if option == "99":
                for list_item in lists.values():
                    media_search.get_soup(list_item)
                print("すべてのHTMLファイルを読み込みました。")
            elif option in lists:
                media_type = lists[option]
                search_term = input("検索したいテキストを入力してください: ").strip()
                results = media_search.search_media(media_type, search_term)
                print(results)
                input("エンターキーを押して続けます。\n")
            else:
                print("無効な選択です。")
        except ValueError:
            print("無効な入力です。数値を入力してください。")
            continue


# メイン呼び出し
if __name__ == "__main__":
    main()
