import shutil
import sys
import os

def cp_imgs(src, dst):
    #get last image index of the source destination directory by sorting and getting last file, image filenames are in the format of '<index #>.jpg'
    prev_last_ind = int(sorted(os.listdir(os.path.join(dst, 'left/')))[-1][:-4])

    for img_dir in ('left', 'right', 'NoIR'):
        for img_path in os.listdir(os.path.join(src, img_dir)):

            #add the largest image index already in dst to the original index of the image
            new_img_path = os.path.join(dst, img_dir, str(prev_last_ind + int(img_path[:-4])) + '.jpg')

            shutil.copy(os.path.join(src, img_dir, img_path), new_img_path)

        print(sorted(os.listdir(os.path.join(dst, img_dir))))

if __name__ == "__main__":
    print('enter: src dir, dst dir\tin command line')
    SRC_DIR, DST_DIR = sys.argv[1], sys.argv[2]

    cp_imgs(SRC_DIR, DST_DIR)
