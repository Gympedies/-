import os
files=os.listdir(".")
for filename in files:
    portion = os.path.splitext(filename)
    # 如果后缀是.txt
    if portion[1] == ".png":  
        # 重新组合文件名和后缀名   
        newname = portion[0] + ".jpg"   
        os.rename(filename,newname)