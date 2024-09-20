
:apksigner sign --ks (签名地址) --ks-key-alias (别名) --out (签名后的apk地址) (待签名apk地址)
@echo on 
java -jar C:\Users\admin\AppData\Local\Android\Sdk\build-tools\33.0.1\lib\apksigner.jar sign --ks D:\3misc\3Kugou\my-release-key.keystore --ks-key-alias my-key-alias  --ks-pass pass:123456 --out  si.apk  2.apk
