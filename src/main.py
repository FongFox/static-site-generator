import os
import shutil


def copy_directory_contents(source_dir, dest_dir):
    cwd = os.getcwd()
    src_dir_path = os.path.join(cwd, source_dir)
    dest_dir_path = os.path.join(cwd, dest_dir)

    if not os.path.exists(src_dir_path):
        raise Exception("Folder path not existed!")

    if os.path.exists(dest_dir_path):
        shutil.rmtree(dest_dir_path)

    os.mkdir(dest_dir_path)

    src_dir = os.listdir(src_dir_path)
    for item in src_dir:
        cur_path = os.path.join(src_dir_path, item)
        if os.path.isfile(cur_path):
            shutil.copy(cur_path, dest_dir_path)
        else:
            new_des_dir_path = os.path.join(dest_dir_path, item)
            os.mkdir(new_des_dir_path)
            copy_directory_contents(cur_path, new_des_dir_path)


def main():
    copy_directory_contents("static", "public")
    pass


if __name__ == "__main__":
    main()
