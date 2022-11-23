"""
英辞郎が用意してるテキストデータをCSV形式に変換するプログラム
"""
import argparse
import json
import pathlib
import re

ENCODING_RAW_EIJIROU = "cp932"
ENCODING_OUTPUT = "utf-8"
OUTPUT_DIR = 'output'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("inputfile_path", help="変換対象となる英辞郎テキストデータのファイルpath")
    parser.add_argument("-j", "--json", help="json形式で出力する", default=False, action="store_true")
    args = parser.parse_args()
    inputfile_path = args.inputfile_path
    
    raw_eijirou = load_raw_eijirou(inputfile_path)
    arranged_eijirou = arrange_raw_eijirou(raw_eijirou)

    if args.json:
        to_json(arranged_eijirou, f"{pathlib.Path(inputfile_path).name[:-4]}.json")
    else:
        to_csv(arranged_eijirou, f"{pathlib.Path(inputfile_path).name[:-4]}.csv")


def load_raw_eijirou(file_path: str) -> list:
    """英辞郎の生データをロードする"""
    with open(file_path, encoding=ENCODING_RAW_EIJIROU) as f:
        return [l for l in f.readlines()]
    

def to_csv(eijirou_data: dict, filename: str):
    with open(pathlib.Path(OUTPUT_DIR, filename), 'w', encoding=ENCODING_OUTPUT) as f:
        for word in sorted(eijirou_data.keys()):
            f.write("{0}::{1}\n".format(word, '||'.join(eijirou_data[word])))


def to_json(eijirou_data: dict, filename: str):
    with open(pathlib.Path(OUTPUT_DIR, filename), 'w', encoding=ENCODING_OUTPUT) as f:
        json.dump(eijirou_data, f, indent=2, ensure_ascii=False)



def arrange_raw_eijirou(raw_eijirou_data: list) -> dict:
    """英辞郎の生データを整形する
    
    Note:
        以下の戦略に沿って、英辞郎の生データを整形しdict型に変換する。
        前提:
            - 英辞郎の生データは1行毎に「単語/熟語」と「その意味」が記載されている。
            - 1行の基本構成
            - ■<word>  {<tag>} : <meaning>
                - ex）■instead {副} : 代わりに、...
            - <tag>が存在しないこともある
            - ■<word> : <meaning>
        戦略:
            - <tag>が無い行は、{word: [meaning]}という形でdictに追加
            - <word>が完全一致する複数行は、一つにまとめて{word: [meaning1, meaning2, ...]}という形でdictに追加
    """
    result = {}

    for line in raw_eijirou_data:
        m = re.match(r"■(?P<word>[^\{:]+)(\{(?P<tag>.+)\}|.*) : (?P<meaning>.+)", line)
        word, tag, meaning = m.group('word').strip(), m.group('tag'), m.group('meaning').strip()
        if not result.get(word):
            result[word] = []
        if tag:
            result[word].append(f"[{tag.strip()}] {meaning}")
        else:
            result[word].append(meaning)
    
    return result


if __name__ == '__main__':
    main()
