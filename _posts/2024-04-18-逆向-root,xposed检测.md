---
categories: [逆向]
tags: [Xposed]
---
# **检查文件系统中的根目录路径**：
+ `/system/app/SuperSU/`
+ `/system/xbin/su`
+ `/sbin/su`
+ `/system/bin/su`

# 检查 `su` 命令
`su` 命令是 Android 上 root 权限的标志，检测设备是否有 `su` 命令可以执行。

# **常见的 Xposed 文件路径**：
+ `/data/data/de.robv.android.xposed.installer/`
+ `/system/framework/XposedBridge.jar`
+ `/system/xposed/`

# **检查系统属性**：
+ `ro.xposed.installed`
+ `xposed.loaded`

# 检查类加载
Xposed 框架使用自定义的类加载器，可以通过反射或类加载来检测是否存在 Xposed 框架。

