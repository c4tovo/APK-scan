from pathlib import Path
import json
import os
import zipfile

class APK_scan:
    def __init__(self) -> None:
        self.flag = {"data": False}
        self.load_json()
    
    def get_confuse(self, dir_path):
        """This is check confuse function

        Args:
            dir_path : you should put a dir path by apktool decompiled
        """
        black_name = ["R$anim.smali", "R$array.smali", "R$color.smali", "R$drawable.smali"]
        mark = []
        def tree(pathname):
            global tree_str
            if pathname.is_file():
                if pathname.name in black_name:
                    mark.append(pathname)
                    self.flag = {"data": True}
            elif pathname.is_dir():
                for cp in pathname.iterdir():
                    tree(cp)
        tree(Path(dir_path+"\smali"))
        if self.flag['data']:
            self.flag = {"data": self.flag['data'], "mark": mark}
        return self.flag
    
    def load_json(self):
        # json文件方式加载特征
        with open(os.path.join("pack.json"), 'r', encoding='utf-8') as f:
            markNameMap = json.load(f)
            self.markNameMap = dict(markNameMap)
            pass
    
    def check_jiagu(self, filename):
        azip = zipfile.ZipFile(filename)  # 默认模式r,读
        jigu = []
        for zippath in azip.namelist():
            if 'lib' in zippath or 'assets' in zippath:
                for key, value in self.markNameMap.items():
                    for mark in value:
                        if mark in zippath:
                            jigu.append({"key": key, "zippath": zippath, "mark": mark})
        if len(jigu) > 0:
            return {"data": jigu}
        for zippath in azip.namelist():
            for key, value in self.markNameMap.items():
                for mark in value:
                    if mark in zippath:
                        jigu.append({"key": key, "zippath": zippath, "mark": mark})
        if len(jigu) > 0:
            return {"data": jigu}
        return {"data": 0}
    
    def get_pack(self, files):
        """This is check pack function

        Args:
            filename : you should put a apk path 
        """
        try:
            with zipfile.ZipFile(files, 'r') as zf:
                if 'AndroidManifest.xml' in zf.namelist() and files[-4:] == '.apk':
                    return self.check_jiagu(files)
                else:
                    return {"data": -1}
        except:
            return False

a = APK_scan()
p = os.path.join("result\\demo")
print(a.get_confuse(p))
print(a.get_pack("\\demo.apk"))

    