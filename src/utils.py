import os
import shutil

def dir_copy(from_dir, to_dir):
    if os.path.exists(to_dir):
        shutil.rmtree(to_dir)
    shutil.copytree(from_dir, to_dir)

