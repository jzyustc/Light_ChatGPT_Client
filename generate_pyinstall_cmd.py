import os
import shutil

if __name__ == "__main__":
    # set these params
    py_path = "GUI"
    main_py_name = "qt"
    data_path = "data"
    python_path = "D:\Programs\Anaconda\envs\pyqt5\Lib\site-packages"

    # install
    def get_py_files(folder_path):
        py_files = []
        for p in os.listdir(folder_path):
            path = os.path.join(folder_path, p)

            if os.path.isdir(path):
                py_files += get_py_files(path)
            elif os.path.isfile(path) and p.endswith(".py"):
                py_files += [path]
        return py_files

    py_files = [main_py_name + ".py"] + get_py_files(py_path)

    # generate cmd
    cmd = "pyinstaller -y -w "
    cmd += " -i " + data_path + "/images/icon.ico "
    for py_file in py_files:
        cmd += f"{py_file} "
    cmd += " -p " + python_path

    print(cmd)
    os.system(cmd)

    source_path = os.path.abspath(data_path)
    target_path = os.path.abspath(os.path.join(".", "dist", main_py_name, data_path))

    os.makedirs(target_path, exist_ok=True)

    if os.path.exists(source_path):
        shutil.rmtree(target_path)

    shutil.copytree(source_path, target_path)
    print('copy data folder finished!')