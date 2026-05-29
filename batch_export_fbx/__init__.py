"""
batch_export_fbx
================

指定フォルダ以下の全 .casc を、同じディレクトリ・同じ basename で
FBX 書き出しするアドオン / コマンドラインツール。

公開 API（コンソールからの利用に便利）:
    from commands.batch_export_fbx import run_folder, export_folder_to_fbx
    run_folder(r"D:\\path\\to\\projects")
"""

from .core import export_folder_to_fbx, find_casc_files, fbx_path_for, make_fbx_settings
from .cli import run_folder, main, main_from_env

__all__ = [
    "export_folder_to_fbx",
    "find_casc_files",
    "fbx_path_for",
    "make_fbx_settings",
    "run_folder",
    "main",
    "main_from_env",
]
