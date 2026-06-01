"""
batch_export_fbx
================

Cascadeur GUI command (+ console helpers) that exports every .casc under a chosen
folder to FBX, into the same directory with the same base name.

Primary use: Commands menu -> "yozolab > Batch casc to FBX" (see command.py).

Console helpers:
    from commands.yozolab.batch_export_fbx import run_folder, run_file
    run_folder(r"D:\\path\\to\\projects")

NOTE: ASCII-only on purpose (Cascadeur's script loader can mis-decode multibyte
source bytes). Japanese docs live in README.md, which is not imported.
"""

from .core import export_folder_to_fbx, find_casc_files, fbx_path_for, make_fbx_settings
from .cli import run_folder, run_file

__all__ = [
    "export_folder_to_fbx",
    "find_casc_files",
    "fbx_path_for",
    "make_fbx_settings",
    "run_folder",
    "run_file",
]
