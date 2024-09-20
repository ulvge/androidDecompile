import subprocess
import time
import os
from tkinter import *
import tkinter.messagebox

deviceIP = " 192.168.0.140"
oriApkName = "zi"
outputDirName = oriApkName+"_dec"
# outputDirName = oriApkName[0 : len(oriApkName)-3 if len(oriApkName)-3 > 0 else len(oriApkName)]

bakDecApk = "1bakDec.apk"
alignApk = "2align.apk"
sigApk = "3sig.apk"

def deleteFile(file):
    try:
        os.remove(file)
    except:
        print(file+"is not exist")

    
def execute_command(command):
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        
        # 实时获取输出信息并打印
        while True:
            output = process.stdout.readline().decode("utf-8")
            if output == "" and process.poll() is not None:
                break
            if output:
                print(output.strip())
                
        # 等待命令执行完成
        process.communicate()
    except:
        print(command+"is not exist")

def decompilationCallBack():
    if os.path.isdir(outputDirName) == False:
        # os.makedirs(outputDirName)
        execute_command("apktool.bat d "+ oriApkName +".apk -o " + outputDirName)
    else:
        a=tkinter.messagebox.askyesnocancel('提示', '已经存在，是否覆盖原目录')
        if a == True:
            execute_command("apktool.bat d "+ oriApkName +".apk -f -o " + outputDirName)
        elif a == False:
            execute_command("apktool.bat d "+ oriApkName +".apk -o " + outputDirName)
        else:
            return

def backCompilationCallBack():
    print("************\n\nstep1 decomplie************")
    execute_command("apktool.bat b "+ outputDirName+" -o "+ bakDecApk)
    time.sleep(0.5)

    signerCallBack()

def signerCallBack():
    print("************\n\nstep2 align************")
    zipalignPath = r"C:\Users\admin\AppData\Local\Android\Sdk\build-tools\33.0.1\zipalign.exe"
    execute_command(zipalignPath + " -p -f -v 4 "+bakDecApk  +" "+ alignApk)
    time.sleep(0.5)

    print("************\n\nstep3 signer************")
    signerPath = r"C:\Users\admin\AppData\Local\Android\Sdk\build-tools\33.0.1\lib\apksigner.jar"
    mykeyPath = r"D:\3misc\3Kugou\my-release-key.keystore"
    execute_command("java -jar "+ signerPath +" sign --ks " + mykeyPath + " --ks-key-alias my-key-alias  --ks-pass pass:123456 --out   " + sigApk +" "+ alignApk)
    time.sleep(0.5)
    installCallBack()

def installCallBack():
    print("************\n\nstep4 install\n************")
    execute_command("adb connect "+deviceIP+":5555")
    execute_command("adb install " + sigApk)
    # execute_command("pause")
    
def createLayout():
    window = Tk()
    window.title("apk工具_by zb")
    window.geometry("+400+400")
    window.geometry("200x200")
    window.configure(bg='lightblue')  # 添加背景颜色

    Button(window, text ="反编译",bg='red', command = decompilationCallBack).place(relx=0.5, rely=0.2, anchor='center')
    Button(window, text ="回编译+签名+安装",bg='green', command = backCompilationCallBack).place(relx=0.5, rely=0.4, anchor='center')
    Button(window, text ="签名+安装",bg='red', command = backCompilationCallBack).place(relx=0.5, rely=0.6, anchor='center')
    Button(window, text ="安装",bg='green', command = installCallBack).place(relx=0.5, rely=0.8, anchor='center')

    window.mainloop()

def evnInit():
    # cmd charsets  HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Command Processor\   new vaule      autorun   =   chcp 65001
    curFullPath = os.path.realpath(__file__)
    curPath, file_name = os.path.split(curFullPath)
    print(curPath)
    os.chdir(curPath) 

    deleteFile(bakDecApk)
    deleteFile(alignApk)
    deleteFile(sigApk)

    createLayout()
     
evnInit()

