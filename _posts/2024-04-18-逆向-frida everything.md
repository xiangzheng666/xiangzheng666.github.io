---
categories: [逆向]
tags: [frida]
---
# 使用
1.上传指定frida server

2.运行frida命令hook

## <font style="color:rgb(68, 68, 68);">1.基础指令</font>
<font style="color:rgb(68, 68, 68);">1.frida-ps -U  查看当前手机运行的进程  
</font><font style="color:rgb(68, 68, 68);">2.frida-ps --help 查看help指令</font>

<font style="color:rgb(68, 68, 68);">Spawn模式</font>

```plain
复制代码 隐藏代码
frida -U -f 进程名 -l hook.js
```

<font style="color:rgb(68, 68, 68);">attach模式 ：</font>

```plain
复制代码 隐藏代码
frida -U 进程名 -l hook.js
```

hook.js:

```javascript
function main(){
    Java.perform(function(){
        hookTest1();
    });
}
setImmediate(main);

function hookTest1(){
    let Demo = Java.use("com.zj.wuaipojie.Demo");
    Demo["a"].implementation = function (str) {
        console.log('a is called' + ', ' + 'str: ' + str);
        let ret = this.a(str);
        console.log('a ret value is ' + ret);
        return ret;
    };
}
```

# 常用API
## <font style="color:rgb(68, 68, 68);">1.Hook普通方法、打印参数和修改返回值</font>
```plain
复制代码 隐藏代码
//定义一个名为hookTest1的函数
function hookTest1(){
        //获取一个名为"类名"的Java类，并将其实例赋值给JavaScript变量utils
    var utils = Java.use("类名");
    //修改"类名"的"method"方法的实现。这个新的实现会接收两个参数（a和b）
    utils.method.implementation = function(a, b){
            //将参数a和b的值改为123和456。
        a = 123;
        b = 456;
        //调用修改过的"method"方法，并将返回值存储在`retval`变量中
        var retval = this.method(a, b);
        //在控制台上打印参数a，b的值以及"method"方法的返回值
        console.log(a, b, retval);
        //返回"method"方法的返回值
        return retval;
    }
}
```

## <font style="color:rgb(68, 68, 68);">2.Hook重载参数</font>
```plain
复制代码 隐藏代码
// .overload()
// .overload('自定义参数')
// .overload('int')
function hookTest2(){
    var utils = Java.use("com.zj.wuaipojie.Demo");
    //overload定义重载函数，根据函数的参数类型填
    utils.Inner.overload('com.zj.wuaipojie.Demo$Animal','java.lang.String').implementation = function(a，b){
        b = "aaaaaaaaaa";
        this.Inner(a,b);
        console.log(b);
    }
}
```

## <font style="color:rgb(68, 68, 68);">3.Hook构造函数</font>
```plain
复制代码 隐藏代码
function hookTest3(){
    var utils = Java.use("com.zj.wuaipojie.Demo");
    //修改类的构造函数的实现，$init表示构造函数
    utils.$init.overload('java.lang.String').implementation = function(str){
        console.log(str);
        str = "52";
        this.$init(str);
    }
}
```

## <font style="color:rgb(68, 68, 68);">4.Hook字段</font>
```plain
复制代码 隐藏代码
function hookTest5(){
    Java.perform(function(){
        //静态字段的修改
        var utils = Java.use("com.zj.wuaipojie.Demo");
        //修改类的静态字段"flag"的值
        utils.staticField.value = "我是被修改的静态变量";
        console.log(utils.staticField.value);
        //非静态字段的修改
        //使用`Java.choose()`枚举类的所有实例
        Java.choose("com.zj.wuaipojie.Demo", {
            onMatch: function(obj){
                    //修改实例的非静态字段"_privateInt"的值为"123456"，并修改非静态字段"privateInt"的值为9999。
                obj._privateInt.value = "123456"; //字段名与函数名相同 前面加个下划线
                obj.privateInt.value = 9999;
            },
            onComplete: function(){

            }
        });
    });

}
```

## <font style="color:rgb(68, 68, 68);">5.Hook内部类</font>
```plain
复制代码 隐藏代码
function hookTest6(){
    Java.perform(function(){
        //内部类
        var innerClass = Java.use("com.zj.wuaipojie.Demo$innerClass");
        console.log(innerClass);
        innerClass.$init.implementation = function(){
            console.log("eeeeeeee");
        }

    });
}
```

## <font style="color:rgb(68, 68, 68);">6.枚举所有的类与类的所有方法</font>
```plain
复制代码 隐藏代码
function hookTest7(){
    Java.perform(function(){
        //枚举所有的类与类的所有方法,异步枚举
        Java.enumerateLoadedClasses({
            onMatch: function(name,handle){
                    //过滤类名
                if(name.indexOf("com.zj.wuaipojie.Demo") !=-1){
                    console.log(name);
                    var clazz =Java.use(name);
                    console.log(clazz);
                    var methods = clazz.class.getDeclaredMethods();
                    console.log(methods);
                }
            },
            onComplete: function(){}
        })
    })
}
```

## <font style="color:rgb(68, 68, 68);">7.枚举所有方法</font>
```plain
复制代码 隐藏代码
function hookTest8(){
    Java.perform(function(){
        var Demo = Java.use("com.zj.wuaipojie.Demo");
        //getDeclaredMethods枚举所有方法
        var methods =Demo.class.getDeclaredMethods();
        for(var j=0; j < methods.length; j++){
            var methodName = methods[j].getName();
            console.log(methodName);
            for(var k=0; k<Demo[methodName].overloads.length;k++){
                Demo[methodName].overloads[k].implementation = function(){
                    for(var i=0;i<arguments.length;i++){
                        console.log(arguments[i]);
                    }
                    return this[methodName].apply(this,arguments);
                }
            }
        }
    })
}
```

## <font style="color:rgb(68, 68, 68);">8.主动调用</font>
<font style="color:rgb(68, 68, 68);">静态方法</font>

```plain
复制代码 隐藏代码
var ClassName=Java.use("com.zj.wuaipojie.Demo"); 
ClassName.privateFunc("传参");
```

<font style="color:rgb(68, 68, 68);">非静态方法</font>

```plain
复制代码 隐藏代码
    var ret = null;
    Java.perform(function () {
        Java.choose("com.zj.wuaipojie.Demo",{    //要hook的类
            onMatch:function(instance){
                ret=instance.privateFunc("aaaaaaa"); //要hook的方法
            },
            onComplete:function(){
                    //console.log("result: " + ret);
            }
        });
    })
    //return ret;
```

# Objection
## <font style="color:rgb(68, 68, 68);">注入命令</font>
```plain
复制代码 隐藏代码
objection -g 包名 explore

-   help：不知道当前命令的效果是什么，在当前命令前加help比如:help env，回车之后会出现当前命令的解释信息
-   按空格：不知道输入什么就按空格，会有提示出来
-   jobs：可以进行多项hook
-   日志：objection的日志文件生成在 C:\Users\Administrator\.objection
```

<font style="color:rgb(68, 68, 68);">启动前就hook</font>

```plain
复制代码 隐藏代码
objection -g 进程名 explore --startup-command "android hooking watch class 路径.类名"
```

## <font style="color:rgb(68, 68, 68);">objection基础api</font>
### <font style="color:rgb(68, 68, 68);">memory list modules   -查看内存中加载的库</font>
```plain
复制代码 隐藏代码
memory list modules
Save the output by adding `--json modules.json` to this command
Name                                                              Base          Size                 Path
----------------------------------------------------------------  ------------  -------------------  ------------------------------------------------------------------------------
app_process64                                                     0x57867c9000  40960 (40.0 KiB)     /system/bin/app_process64
linker64                                                          0x72e326a000  229376 (224.0 KiB)   /system/bin/linker64
libandroid_runtime.so                                             0x72e164e000  2113536 (2.0 MiB)    /system/lib64/libandroid_runtime.so
libbase.so                                                        0x72dfa67000  81920 (80.0 KiB)     /system/lib64/libbase.so
libbinder.so                                                      0x72dec1c000  643072 (628.0 KiB)   /system/lib64/libbinder.so
libcutils.so                                                      0x72de269000  86016 (84.0 KiB)     /system/lib64/libcutils.so
libhidlbase.so                                                    0x72df4cc000  692224 (676.0 KiB)   /system/lib64/libhidlbase.so
liblog.so                                                         0x72e0be1000  98304 (96.0 KiB)     /system/lib64/liblog
```

### <font style="color:rgb(68, 68, 68);">memory list exports so名称 - 查看库的导出函数</font>
```plain
复制代码 隐藏代码
memory list exports liblog.so
Save the output by adding `--json exports.json` to this command
Type      Name                                  Address
--------  ------------------------------------  ------------
function  android_log_write_int32               0x72e0be77c8
function  android_log_write_list_begin          0x72e0be76f0
function  __android_log_bswrite                 0x72e0be9bd8
function  __android_log_security                0x72e0bf2144
function  __android_log_bwrite                  0x72e0be9a18
function  android_log_reset                     0x72e0be75ec
function  android_log_write_string8             0x72e0be7a38
function  android_logger_list_free              0x72e0be8c04
function  __android_log_print                   0x72e0be9728
function  __android_logger_property_get_bool    0x72e0bf2248
function  android_logger_get_id                 0x72e0be8270
function  android_logger_set_prune_list         0x72e0be8948
```

### <font style="color:rgb(68, 68, 68);">android hooking list activities -查看内存中加载的activity   </font>
### <font style="color:rgb(68, 68, 68);">android hooking list services -查看内存中加载的services  
</font>![](https://cdn.nlark.com/yuque/0/2024/png/38873034/1732189411186-b5c46b56-92b4-417c-8781-bdd19a325a36.png)
### <font style="color:rgb(68, 68, 68);">关闭ssl校验  android sslpinning disable</font>
### <font style="color:rgb(68, 68, 68);">关闭root检测  android root disable</font>
### <font style="color:rgb(68, 68, 68);">objection内存漫游</font>
1. <font style="color:rgb(68, 68, 68);">内存搜刮类实例</font>

```plain
复制代码 隐藏代码
android heap search instances 类名(命令)
Class instance enumeration complete for com.zj.wuaipojie.Demo  
 Hashcode  Class                  toString()
---------  ---------------------  -----------------------------
215120583  com.zj.wuaipojie.Demo  com.zj.wuaipojie.Demo@cd27ac7
```

1. <font style="color:rgb(68, 68, 68);">调用实例的方法</font>

```plain
复制代码 隐藏代码
android heap execute <handle> getPublicInt(实例的hashcode+方法名)
如果是带参数的方法，则需要进入编辑器环境  
android heap evaluate <handle>  
console.log(clazz.a("吾爱破解"));
按住esc+enter触发
```

1. <font style="color:rgb(68, 68, 68);">android hooking list classes -列出内存中所有的类(结果比静态分析的更准确)</font>

```plain
复制代码 隐藏代码
android hooking list classes 

tw.idv.palatis.xappdebug.MainApplication
tw.idv.palatis.xappdebug.xposed.HookMain
tw.idv.palatis.xappdebug.xposed.HookMain$a
tw.idv.palatis.xappdebug.xposed.HookMain$b
tw.idv.palatis.xappdebug.xposed.HookMain$c
tw.idv.palatis.xappdebug.xposed.HookMain$d
tw.idv.palatis.xappdebug.xposed.HookSelf
u
v
void
w
xposed.dummy.XResourcesSuperClass
xposed.dummy.XTypedArraySuperClass

Found 10798 classes
```

1. <font style="color:rgb(68, 68, 68);">android hooking search classes 关键类名 -在内存中所有已加载的类中搜索包含特定关键词的类</font>

```plain
复制代码 隐藏代码
android hooking search classes wuaipojie
Note that Java classes are only loaded when they are used, so if the expected class has not been found, it might not have been loaded yet.
com.zj.wuaipojie.Demo
com.zj.wuaipojie.Demo$Animal
com.zj.wuaipojie.Demo$Companion
com.zj.wuaipojie.Demo$InnerClass
com.zj.wuaipojie.Demo$test$1
com.zj.wuaipojie.MainApplication
com.zj.wuaipojie.databinding.ActivityMainBinding
... 

Found 38 classes
```

1. <font style="color:rgb(68, 68, 68);">android hooking search methods 关键方法名 -在内存中所有已加载的类的方法中搜索包含特定关键词的方法(一般不建议使用，特别耗时，还可能崩溃)</font>
2. <font style="color:rgb(68, 68, 68);">android hooking list class_methods 类名 -内存漫游类中的所有方法</font>

```plain
复制代码 隐藏代码
android hooking list class_methods com.zj.wuaipojie.ui.ChallengeSixth
private static final void com.zj.wuaipojie.ui.ChallengeSixth.onCreate$lambda-0(com.zj.wuaipojie.ui.ChallengeSixth,android.view.View)
private static final void com.zj.wuaipojie.ui.ChallengeSixth.onCreate$lambda-1(com.zj.wuaipojie.ui.ChallengeSixth,android.view.View)
private static final void com.zj.wuaipojie.ui.ChallengeSixth.onCreate$lambda-2(com.zj.wuaipojie.ui.ChallengeSixth,android.view.View)
private static final void com.zj.wuaipojie.ui.ChallengeSixth.onCreate$lambda-3(com.zj.wuaipojie.ui.ChallengeSixth,android.view.View)
protected void com.zj.wuaipojie.ui.ChallengeSixth.onCreate(android.os.Bundle)
public final java.lang.String com.zj.wuaipojie.ui.ChallengeSixth.hexToString(java.lang.String)
public final java.lang.String com.zj.wuaipojie.ui.ChallengeSixth.unicodeToString(java.lang.String)
public final void com.zj.wuaipojie.ui.ChallengeSixth.toastPrint(java.lang.String)
public static void com.zj.wuaipojie.ui.ChallengeSixth.$r8$lambda$1lrkrgiCEFWXZDHzLRibYURG1h8(com.zj.wuaipojie.ui.ChallengeSixth,android.view.View)
public static void com.zj.wuaipojie.ui.ChallengeSixth.$r8$lambda$IUqwMqbTKaOGiTaeOmvy_GjNBso(com.zj.wuaipojie.ui.ChallengeSixth,android.view.View)
public static void com.zj.wuaipojie.ui.ChallengeSixth.$r8$lambda$Kc_cRYZjjhjsTl6GYNHbgD-i6sE(com.zj.wuaipojie.ui.ChallengeSixth,android.view.View)
public static void com.zj.wuaipojie.ui.ChallengeSixth.$r8$lambda$PDKm2AfziZQo6Lv1HEFkJWkUsoE(com.zj.wuaipojie.ui.ChallengeSixth,android.view.View)

Found 12 method(s)
```

### <font style="color:rgb(68, 68, 68);">objectionHook</font>
1. <font style="color:rgb(68, 68, 68);">hook类的所有方法</font>

```plain
复制代码 隐藏代码
android hooking watch class 类名
```

2. <font style="color:rgb(68, 68, 68);">hook方法的参数、返回值和调用栈</font>

```plain
复制代码 隐藏代码
android hooking watch class_method 类名.方法名 --dump-args --dump-return --dump-backtrace
```

3. <font style="color:rgb(68, 68, 68);">hook 类的构造方法</font>

```plain
复制代码 隐藏代码
android hooking watch class_method 类名.$init
```

4. <font style="color:rgb(68, 68, 68);">hook 方法的所有重载</font>

```plain
复制代码 隐藏代码
android hooking watch class_method 类名.方法名
```

# frida Native Hook
## <font style="color:rgb(68, 68, 68);">1.Process、Module、Memory基础</font>
### <font style="color:rgb(68, 68, 68);">1.Process</font>
`<font style="color:rgb(68, 68, 68);">Process</font>`<font style="color:rgb(68, 68, 68);"> 对象代表当前被Hook的进程，能获取进程的信息，枚举模块，枚举范围等</font>

| **<font style="color:rgb(68, 68, 68);">API</font>** | ## **<font style="color:rgb(68, 68, 68);">含义</font>** |
| --- | --- |
| ## `<font style="color:rgb(68, 68, 68);">Process.id</font>` | ## <font style="color:rgb(68, 68, 68);">返回附加目标进程的</font><font style="color:rgb(68, 68, 68);"> </font>`<font style="color:rgb(68, 68, 68);">PID</font>` |
| ## `<font style="color:rgb(68, 68, 68);">Process.isDebuggerAttached()</font>` | ## <font style="color:rgb(68, 68, 68);">检测当前是否对目标程序已经附加</font> |
| ## `<font style="color:rgb(68, 68, 68);">Process.enumerateModules()</font>` | ## <font style="color:rgb(68, 68, 68);">枚举当前加载的模块，返回模块对象的数组</font> |
| ## `<font style="color:rgb(68, 68, 68);">Process.enumerateThreads()</font>` | ## <font style="color:rgb(68, 68, 68);">枚举当前所有的线程，返回包含</font><font style="color:rgb(68, 68, 68);"> </font>`<font style="color:rgb(68, 68, 68);">id</font>`<br/>## <font style="color:rgb(68, 68, 68);">,</font><font style="color:rgb(68, 68, 68);"> </font>`<font style="color:rgb(68, 68, 68);">state</font>`<br/>## <font style="color:rgb(68, 68, 68);">,</font><font style="color:rgb(68, 68, 68);"> </font>`<font style="color:rgb(68, 68, 68);">context</font>`<br/>## <font style="color:rgb(68, 68, 68);"> </font><font style="color:rgb(68, 68, 68);">等属性的对象数组</font> |


### <font style="color:rgb(68, 68, 68);">2.Module</font>
`<font style="color:rgb(68, 68, 68);">Module</font>`<font style="color:rgb(68, 68, 68);"> 对象代表一个加载到进程的模块(例如，在 Windows 上的 DLL，或在 Linux/Android 上的 .so 文件),能查询模块的信息，如模块的基址、名称、导入/导出的函数等</font>

| **<font style="color:rgb(68, 68, 68);">API</font>** | **<font style="color:rgb(68, 68, 68);">含义</font>** |
| --- | --- |
| `<font style="color:rgb(68, 68, 68);">Module.load()</font>` | <font style="color:rgb(68, 68, 68);">加载指定so文件，返回一个Module对象</font> |
| `<font style="color:rgb(68, 68, 68);">enumerateImports()</font>` | <font style="color:rgb(68, 68, 68);">枚举所有Import库函数，返回Module数组对象</font> |
| `<font style="color:rgb(68, 68, 68);">enumerateExports()</font>` | <font style="color:rgb(68, 68, 68);">枚举所有Export库函数，返回Module数组对象</font> |
| `<font style="color:rgb(68, 68, 68);">enumerateSymbols()</font>` | <font style="color:rgb(68, 68, 68);">枚举所有Symbol库函数，返回Module数组对象</font> |
| `<font style="color:rgb(68, 68, 68);">Module.findExportByName(exportName)、Module.getExportByName(exportName)</font>` | <font style="color:rgb(68, 68, 68);">寻找指定so中export库中的函数地址</font> |
| `<font style="color:rgb(68, 68, 68);">Module.findBaseAddress(name)、Module.getBaseAddress(name)</font>` | <font style="color:rgb(68, 68, 68);">返回so的基地址</font> |


### <font style="color:rgb(68, 68, 68);">3.Memory</font>
`<font style="color:rgb(68, 68, 68);">Memory</font>`<font style="color:rgb(68, 68, 68);">是一个工具对象，提供直接读取和修改进程内存的功能，能够读取特定地址的值、写入数据、分配内存等</font>

| ### **<font style="color:rgb(68, 68, 68);">方法</font>** | ### **<font style="color:rgb(68, 68, 68);">功能</font>** |
| --- | --- |
| ### `<font style="color:rgb(68, 68, 68);">Memory.copy()</font>` | ### <font style="color:rgb(68, 68, 68);">复制内存</font> |
| ### `<font style="color:rgb(68, 68, 68);">Memory.scan()</font>` | ### <font style="color:rgb(68, 68, 68);">搜索内存中特定模式的数据</font> |
| ### `<font style="color:rgb(68, 68, 68);">Memory.scanSync()</font>` | ### <font style="color:rgb(68, 68, 68);">同上，但返回多个匹配的数据</font> |
| ### `<font style="color:rgb(68, 68, 68);">Memory.alloc()</font>` | ### <font style="color:rgb(68, 68, 68);">在目标进程的堆上申请指定大小的内存，返回一个</font>`<font style="color:rgb(68, 68, 68);">NativePointer</font>` |
| ### `<font style="color:rgb(68, 68, 68);">Memory.writeByteArray()</font>` | ### <font style="color:rgb(68, 68, 68);">将字节数组写入一个指定内存</font> |
| ### `<font style="color:rgb(68, 68, 68);">Memory.readByteArray</font>` | ### <font style="color:rgb(68, 68, 68);">读取内存</font> |


## <font style="color:rgb(68, 68, 68);">2.枚举导入导出表</font>
1. **<font style="color:rgb(68, 68, 68);">导出表（Export Table）</font>**<font style="color:rgb(68, 68, 68);">：列出了库中可以被其他程序或库访问的所有公开函数和符号的名称。</font>
2. **<font style="color:rgb(68, 68, 68);">导入表（Import Table）</font>**<font style="color:rgb(68, 68, 68);">：列出了库需要从其他库中调用的函数和符号的名称。</font>

<font style="color:rgb(68, 68, 68);">简而言之，导出表告诉其他程序：“这些是我提供的功能。”，而导入表则表示：“这些是我需要的功能。”。</font>

```plain
复制代码 隐藏代码
function hookTest1(){
    Java.perform(function(){
        //打印导入表
        var imports = Module.enumerateImports("lib52pojie.so");
        for(var i =0; i < imports.length;i++){
            if(imports[i].name == "vip"){
                console.log(JSON.stringify(imports[i])); //通过JSON.stringify打印object数据
                console.log(imports[i].address);
            }
        }
        //打印导出表
        var exports = Module.enumerateExports("lib52pojie.so");
        for(var i =0; i < exports.length;i++){
            console.log(JSON.stringify(exports[i]));
        }

    })
}
```

## <font style="color:rgb(68, 68, 68);">3.Native函数的基础Hook打印</font>
1. <font style="color:rgb(68, 68, 68);">整数型、布尔值类型、char类型</font>

```plain
复制代码 隐藏代码
function hookTest2(){
Java.perform(function(){
    //根据导出函数名打印地址
    var helloAddr = Module.findExportByName("lib52pojie.so","Java_com_zj_wuaipojie_util_SecurityUtil_checkVip");
    console.log(helloAddr); 
    if(helloAddr != null){
            //Interceptor.attach是Frida里的一个拦截器
        Interceptor.attach(helloAddr,{
                //onEnter里可以打印和修改参数
            onEnter: function(args){  //args传入参数
                console.log(args[0]);  //打印第一个参数的值
                console.log(this.context.x1);  // 打印寄存器内容
                console.log(args[1].toInt32()); //toInt32()转十进制
                                    console.log(args[2].readCString()); //读取字符串 char类型
                                    console.log(hexdump(args[2])); //内存dump

            },
            //onLeave里可以打印和修改返回值
            onLeave: function(retval){  //retval返回值
                console.log(retval);
                console.log("retval",retval.toInt32());
            }
        })
    }
})
}
```

2. <font style="color:rgb(68, 68, 68);">字符串类型</font>

```plain
复制代码 隐藏代码
function hookTest2(){
    Java.perform(function(){
        //根据导出函数名打印地址
        var helloAddr = Module.findExportByName("lib52pojie.so","Java_com_zj_wuaipojie_util_SecurityUtil_vipLevel");
        if(helloAddr != null){
            Interceptor.attach(helloAddr,{
                //onEnter里可以打印和修改参数
                onEnter: function(args){  //args传入参数
                    // 方法一
                    var jString = Java.cast(args[2], Java.use('java.lang.String'));
                    console.log("参数:", jString.toString());
                    // 方法二
                    var JNIEnv = Java.vm.getEnv();
                    var originalStrPtr = JNIEnv.getStringUtfChars(args[2], null).readCString();        
                    console.log("参数:", originalStrPtr);                                
                },
                //onLeave里可以打印和修改返回值
                onLeave: function(retval){  //retval返回值
                    var returnedJString = Java.cast(retval, Java.use('java.lang.String'));
                    console.log("返回值:", returnedJString.toString());
                }
            })
        }
    })
}
```

## <font style="color:rgb(68, 68, 68);">4.Native函数的基础Hook修改</font>
1. <font style="color:rgb(68, 68, 68);">整数型修改</font>

```plain
复制代码 隐藏代码
function hookTest3(){
Java.perform(function(){
    //根据导出函数名打印地址
    var helloAddr = Module.findExportByName("lib52pojie.so","Java_com_zj_wuaipojie_util_SecurityUtil_checkVip");
    console.log(helloAddr);
    if(helloAddr != null){
        Interceptor.attach(helloAddr,{
            onEnter: function(args){  //args参数
                args[0] = ptr(1000); //第一个参数修改为整数 1000，先转为指针再赋值
                console.log(args[0]);

            },
            onLeave: function(retval){  //retval返回值
                retval.replace(20000);  //返回值修改
                console.log("retval",retval.toInt32());
            }
        })
    }
})
}
```

2. <font style="color:rgb(68, 68, 68);">字符串类型修改</font>

```plain
复制代码 隐藏代码
function hookTest2(){
Java.perform(function(){
    //根据导出函数名打印地址
    var helloAddr = Module.findExportByName("lib52pojie.so","Java_com_zj_wuaipojie_util_SecurityUtil_vipLevel");
    if(helloAddr != null){
        Interceptor.attach(helloAddr,{
            //onEnter里可以打印和修改参数
            onEnter: function(args){  //args传入参数
                var JNIEnv = Java.vm.getEnv();
                var originalStrPtr = JNIEnv.getStringUtfChars(args[2], null).readCString();        
                console.log("参数:", originalStrPtr);
                var modifiedContent = "至尊";
                var newJString = JNIEnv.newStringUtf(modifiedContent);
                args[2] = newJString;                                
            },
            //onLeave里可以打印和修改返回值
            onLeave: function(retval){  //retval返回值
                var returnedJString = Java.cast(retval, Java.use('java.lang.String'));
                console.log("返回值:", returnedJString.toString());
                var JNIEnv = Java.vm.getEnv();
                var modifiedContent = "无敌";
                var newJString = JNIEnv.newStringUtf(modifiedContent);
                retval.replace(newJString);
            }
        })
    }
})
}
```

## <font style="color:rgb(68, 68, 68);">5.SO基址的获取方式</font>
```plain
复制代码 隐藏代码
var moduleAddr1 = Process.findModuleByName("lib52pojie.so").base;  
var moduleAddr2 = Process.getModuleByName("lib52pojie.so").base;  
var moduleAddr3 = Module.findBaseAddress("lib52pojie.so");
```

## <font style="color:rgb(68, 68, 68);">6.Hook未导出函数与函数地址计算</font>
```plain
复制代码 隐藏代码
function hookTest6(){
    Java.perform(function(){
        //根据导出函数名打印基址
        var soAddr = Module.findBaseAddress("lib52pojie.so");
        console.log(soAddr);
        var funcaddr = soAddr.add(0x1071C);  
        console.log(funcaddr);
        if(funcaddr != null){
            Interceptor.attach(funcaddr,{
                onEnter: function(args){  //args参数

                },
                onLeave: function(retval){  //retval返回值
                    console.log(retval.toInt32());
                }
            })
        }
    })
}
```

<font style="color:rgb(68, 68, 68);">函数地址计算</font>

1. <font style="color:rgb(68, 68, 68);">安卓里一般32 位的 so 中都是</font>`<font style="color:rgb(68, 68, 68);">thumb</font>`<font style="color:rgb(68, 68, 68);">指令，64 位的 so 中都是</font>`<font style="color:rgb(68, 68, 68);">arm</font>`<font style="color:rgb(68, 68, 68);">指令</font>
2. <font style="color:rgb(68, 68, 68);">通过IDA里的opcode bytes来判断，arm 指令为 4 个字节(options -> general -> Number of opcode bytes (non-graph)  输入4)</font>
3. <font style="color:rgb(68, 68, 68);">thumb 指令，函数地址计算方式： so 基址 + 函数在 so 中的偏移 + 1  
</font><font style="color:rgb(68, 68, 68);">arm 指令，函数地址计算方式： so 基址 + 函数在 so 中的偏移</font>

## <font style="color:rgb(68, 68, 68);">7.Hook_dlopen</font>
[<font style="color:rgb(68, 68, 68);">dlopen源码</font>](http://aospxref.com/android-8.0.0_r36/xref/bionic/libdl/libdl.c?r=&mo=4035&fi=101#101)<font style="color:rgb(68, 68, 68);">  
</font>[<font style="color:rgb(68, 68, 68);">android_dlopen_ext源码</font>](http://aospxref.com/android-8.0.0_r36/xref/bionic/libdl/libdl.c#146)

```plain
复制代码 隐藏代码
function hook_dlopen() {
    var dlopen = Module.findExportByName(null, "dlopen");
    Interceptor.attach(dlopen, {
        onEnter: function (args) {
            var so_name = args[0].readCString();
            if (so_name.indexOf("lib52pojie.so") >= 0) this.call_hook = true;
        }, onLeave: function (retval) {
            if (this.call_hook) hookTest2();
        }
    });
    // 高版本Android系统使用android_dlopen_ext
    var android_dlopen_ext = Module.findExportByName(null, "android_dlopen_ext");
    Interceptor.attach(android_dlopen_ext, {
        onEnter: function (args) {
            var so_name = args[0].readCString();
            if (so_name.indexOf("lib52pojie.so") >= 0) this.call_hook = true;
        }, onLeave: function (retval) {
            if (this.call_hook) hookTest2();
        }
    });
}
```

# 基于r0tace的分析
[https://github.com/r0ysue/r0tracer](https://github.com/r0ysue/r0tracer)

# <font style="color:rgb(68, 68, 68);">Frida-Native-Hook读写、主动调用</font>
### <font style="color:rgb(68, 68, 68);">1.Frida写数据</font>
```plain
复制代码 隐藏代码
//一般写在app的私有目录里，不然会报错:failed to open file (Permission denied)(实际上就是权限不足)
var file_path = "/data/user/0/com.zj.wuaipojie/test.txt";
var file_handle = new File(file_path, "wb");
if (file_handle && file_handle != null) {
        file_handle.write(data); //写入数据
        file_handle.flush(); //刷新
        file_handle.close(); //关闭
}
```

### <font style="color:rgb(68, 68, 68);">2.Frida_inlineHook与读写汇编</font>
<font style="color:rgb(68, 68, 68);">什么是inlinehook？  
</font><font style="color:rgb(68, 68, 68);">Inline hook（内联钩子）是一种在程序运行时修改函数执行流程的技术。</font>**<font style="color:rgb(68, 68, 68);">它通过修改函数的原始代码，将目标函数的执行路径重定向到自定义的代码段，从而实现对目标函数的拦截和修改。</font>**<font style="color:rgb(68, 68, 68);">  
</font><font style="color:rgb(68, 68, 68);">简单来说就是可以对任意地址的指令进行hook读写操作  
</font><font style="color:rgb(68, 68, 68);">常见inlinehook框架:  
</font>[<font style="color:rgb(68, 68, 68);">Android-Inline-Hook</font>](https://github.com/ele7enxxh/Android-Inline-Hook)<font style="color:rgb(68, 68, 68);">  
</font>[<font style="color:rgb(68, 68, 68);">whale</font>](https://github.com/asLody/whale)<font style="color:rgb(68, 68, 68);">  
</font>[<font style="color:rgb(68, 68, 68);">Dobby</font>](https://github.com/jmpews/Dobby)<font style="color:rgb(68, 68, 68);">  
</font>[<font style="color:rgb(68, 68, 68);">substrate</font>](http://www.cydiasubstrate.com/)

<font style="color:rgb(68, 68, 68);">PS：Frida的inlinehook不是太稳定，崩溃是基操，另外新版的frida兼容性会比较好</font>

```plain
复制代码 隐藏代码
function inline_hook() {
    var soAddr = Module.findBaseAddress("lib52pojie.so");
    if (soAddr) {
        var func_addr = soAddr.add(0x10428);
        Java.perform(function () {
            Interceptor.attach(func_addr, {
                onEnter: function (args) {
                    console.log(this.context.x22); //注意此时就没有args概念了
                    this.context.x22 = ptr(1); //赋值方法参考上一节课
                },
                onLeave: function (retval) {
                }
            }
            )
        })
    }
}
```

1. <font style="color:rgb(68, 68, 68);">将地址的指令解析成汇编</font>

```plain
复制代码 隐藏代码
var soAddr = Module.findBaseAddress("lib52pojie.so");
var codeAddr = Instruction.parse(soAddr.add(0x10428));
console.log(codeAddr.toString());
```

2. <font style="color:rgb(68, 68, 68);">Frida Api  
</font>[<font style="color:rgb(68, 68, 68);">arm转hex</font>](https://armconverter.com/)

```plain
复制代码 隐藏代码
var soAddr = Module.findBaseAddress("lib52pojie.so");
var codeAddr = soAddr.add(0x10428);
Memory.patchCode(codeAddr, 4, function(code) {
const writer = new Arm64Writer(code, { pc: codeAddr });
writer.putBytes(hexToBytes("20008052"));
writer.flush();
});
function hexToBytes(str) {
var pos = 0;
var len = str.length;
if (len % 2 != 0) {
    return null;
}
len /= 2;
var hexA = new Array();
for (var i = 0; i < len; i++) {
    var s = str.substr(pos, 2);
    var v = parseInt(s, 16);
    hexA.push(v);
    pos += 2;
}
return hexA;
}
```

### <font style="color:rgb(68, 68, 68);">3.普通函数与jni函数的主动调用</font>
[<font style="color:rgb(68, 68, 68);">nativefunction</font>](https://frida.re/docs/javascript-api/#nativefunction)

| **<font style="color:rgb(68, 68, 68);">数据类型</font>** | **<font style="color:rgb(68, 68, 68);">描述</font>** |
| --- | --- |
| <font style="color:rgb(68, 68, 68);">void</font> | <font style="color:rgb(68, 68, 68);">无返回值</font> |
| <font style="color:rgb(68, 68, 68);">pointer</font> | <font style="color:rgb(68, 68, 68);">指针</font> |
| <font style="color:rgb(68, 68, 68);">int</font> | <font style="color:rgb(68, 68, 68);">整数</font> |
| <font style="color:rgb(68, 68, 68);">long</font> | <font style="color:rgb(68, 68, 68);">长整数</font> |
| <font style="color:rgb(68, 68, 68);">char</font> | <font style="color:rgb(68, 68, 68);">字符</font> |
| <font style="color:rgb(68, 68, 68);">float</font> | <font style="color:rgb(68, 68, 68);">浮点数</font> |
| <font style="color:rgb(68, 68, 68);">double</font> | <font style="color:rgb(68, 68, 68);">双精度浮点数</font> |
| <font style="color:rgb(68, 68, 68);">bool</font> | <font style="color:rgb(68, 68, 68);">布尔值</font> |


```plain
复制代码 隐藏代码
var funcAddr = Module.findBaseAddress("lib52pojie.so").add(0x1054C);
//声明函数指针
//NativeFunction的第一个参数是地址，第二个参数是返回值类型，第三个[]里的是传入的参数类型(有几个就填几个)
var aesAddr = new NativeFunction(funcAddr , 'pointer', ['pointer', 'pointer']);
var encry_text = Memory.allocUtf8String("OOmGYpk6s0qPSXEPp4X31g==");    //开辟一个指针存放字符串       
var key = Memory.allocUtf8String('wuaipojie0123456'); 
console.log(aesAddr(encry_text ,key).readCString());
```

# <font style="color:rgb(68, 68, 68);">frida-trace</font>
<font style="color:rgb(68, 68, 68);">一次性监控一堆函数地址。还能打印出比较漂亮的树状图，不仅可以显示调用流程，还能显示调用层次</font>

<font style="color:rgb(68, 68, 68);">frida-trace -U -F -I "lib52pojie.so" -i "Java_" </font>

<font style="color:rgb(68, 68, 68);">#附加当前进程并追踪lib52pojie.so里的所有Java_开头的jni导出函数</font>

![](https://cdn.nlark.com/yuque/0/2024/png/38873034/1732192252505-0eade7a1-5433-4eb9-961d-d1705fb921e1.png)

# <font style="color:rgb(68, 68, 68);">jnitrace</font>
```plain
复制代码 隐藏代码
pip install jnitrace==3.3.0
```

<font style="color:rgb(68, 68, 68);">使用方法</font>

```plain
复制代码 隐藏代码
jnitrace -m attach -l lib52pojie.so com.zj.wuaipojie -o trace.json //attach模式附加52pojie.so并输出日志
```

`<font style="color:rgb(68, 68, 68);">-l libnative-lib.so</font>`<font style="color:rgb(68, 68, 68);">- 用于指定要跟踪的库  
</font>`<font style="color:rgb(68, 68, 68);">-m <spawn|attach></font>`<font style="color:rgb(68, 68, 68);">- 用于指定要使用的 Frida 附加机制  
</font>`<font style="color:rgb(68, 68, 68);">-i <regex></font>`<font style="color:rgb(68, 68, 68);">- 用于指定应跟踪的方法名称，例如，</font>`<font style="color:rgb(68, 68, 68);">-i Get -i RegisterNatives</font>`<font style="color:rgb(68, 68, 68);">将仅包含名称中包含 Get 或 RegisterNatives 的 JNI 方法  
</font>`<font style="color:rgb(68, 68, 68);">-e <regex></font>`<font style="color:rgb(68, 68, 68);">- 用于指定跟踪中应忽略的方法名称，例如，</font>`<font style="color:rgb(68, 68, 68);">-e ^Find -e GetEnv</font>`<font style="color:rgb(68, 68, 68);">将从结果中排除所有以 Find 开头或包含 GetEnv 的 JNI 方法名称  
</font>`<font style="color:rgb(68, 68, 68);">-I <string></font>`<font style="color:rgb(68, 68, 68);">- 用于指定应跟踪的库的导出  
</font>`<font style="color:rgb(68, 68, 68);">-E <string></font>`<font style="color:rgb(68, 68, 68);">用于指定不应跟踪的库的导出  
</font>`<font style="color:rgb(68, 68, 68);">-o path/output.json</font>`<font style="color:rgb(68, 68, 68);">- 用于指定</font>`<font style="color:rgb(68, 68, 68);">jnitrace</font>`<font style="color:rgb(68, 68, 68);">存储所有跟踪数据的输出路径</font>

![](https://cdn.nlark.com/yuque/0/2024/png/38873034/1732192267958-9947d2a0-576c-40b5-bc22-2f9d8360030a.png)

# <font style="color:rgb(68, 68, 68);">sktrace</font>
```plain
python sktrace.py -m attach -l lib52pojie.so -i 0x103B4 com.zj.wuaipojie
```

![](https://cdn.nlark.com/yuque/0/2024/png/38873034/1732192339377-51a6bc8f-4248-49c7-9c01-57667bf827fa.png)

# <font style="color:rgb(68, 68, 68);">系统库的hook</font>
yang神hook3件套

[GitHub - lasting-yang/frida_hook_libart: Frida hook some jni functions](https://github.com/lasting-yang/frida_hook_libart)

## <font style="color:rgb(68, 68, 68);">1.Hook_Libart</font>
`<font style="color:rgb(68, 68, 68);">libart.so</font>`<font style="color:rgb(68, 68, 68);">: 在 Android 5.0（Lollipop）及更高版本中，</font>`<font style="color:rgb(68, 68, 68);">libart.so</font>`<font style="color:rgb(68, 68, 68);"> </font><font style="color:rgb(68, 68, 68);">是 Android 运行时（ART，Android Runtime）的核心组件，它取代了之前的 Dalvik 虚拟机。可以在</font><font style="color:rgb(68, 68, 68);"> </font>`<font style="color:rgb(68, 68, 68);">libart.so</font>`<font style="color:rgb(68, 68, 68);"> </font><font style="color:rgb(68, 68, 68);">里找到 JNI 相关的实现。  
</font><font style="color:rgb(68, 68, 68);">PS:在高于安卓10的系统里，so的路径是/apex/com.android.runtime/lib64/libart.so，低于10的则在system/lib64/libart.so</font>

| **<font style="color:rgb(68, 68, 68);">函数名称</font>** | **<font style="color:rgb(68, 68, 68);">参数</font>** | **<font style="color:rgb(68, 68, 68);">描述</font>** | **<font style="color:rgb(68, 68, 68);">返回值</font>** |
| --- | --- | --- | --- |
| `<font style="color:rgb(68, 68, 68);">RegisterNatives</font>` | `<font style="color:rgb(68, 68, 68);">JNIEnv *env, jclass clazz, const JNINativeMethod *methods, jint nMethods</font>` | <font style="color:rgb(68, 68, 68);">反注册类的本地方法。类将返回到链接或注册了本地方法函数前的状态。该函数不应在本地代码中使用。相反，它可以为某些程序提供一种重新加载和重新链接本地库的途径。</font> | <font style="color:rgb(68, 68, 68);">成功时返回0；失败时返回负数</font> |
| `<font style="color:rgb(68, 68, 68);">GetStringUTFChars</font>` | `<font style="color:rgb(68, 68, 68);">JNIEnv*env, jstring string, jboolean *isCopy</font>` | <font style="color:rgb(68, 68, 68);">通过JNIEnv接口指针调用，它将一个代表着Java虚拟机中的字符串jstring引用，转换成为一个UTF-8形式的C字符串</font> | <font style="color:rgb(68, 68, 68);">-</font> |
| `<font style="color:rgb(68, 68, 68);">NewStringUTF</font>` | `<font style="color:rgb(68, 68, 68);">JNIEnv *env, const char *bytes</font>` | <font style="color:rgb(68, 68, 68);">以字节为单位返回字符串的 UTF-8 长度</font> | <font style="color:rgb(68, 68, 68);">返回字符串的长度</font> |
| `<font style="color:rgb(68, 68, 68);">FindClass</font>` | `<font style="color:rgb(68, 68, 68);">JNIEnv *env, const char *name</font>` | <font style="color:rgb(68, 68, 68);">通过对象获取这个类。该函数比较简单，唯一注意的是对象不能为NULL，否则获取的class肯定返回也为NULL。</font> | <font style="color:rgb(68, 68, 68);">-</font> |
| `<font style="color:rgb(68, 68, 68);">GetMethodID</font>` | `<font style="color:rgb(68, 68, 68);">JNIEnv *env, jclass clazz, const char *name, const char *sig</font>` | <font style="color:rgb(68, 68, 68);">返回类或接口实例（非静态）方法的方法 ID。方法可在某个 clazz 的超类中定义，也可从 clazz 继承。GetMethodID() 可使未初始化的类初始化。</font> | <font style="color:rgb(68, 68, 68);">方法ID，如果找不到指定的方法，则为NULL</font> |
| `<font style="color:rgb(68, 68, 68);">GetStaticMethodID</font>` | `<font style="color:rgb(68, 68, 68);">JNIEnv *env, jclass clazz, const char *name, const char *sig</font>` | <font style="color:rgb(68, 68, 68);">获取类对象的静态方法ID</font> | <font style="color:rgb(68, 68, 68);">属性ID对象。如果操作失败，则返回NULL</font> |
| `<font style="color:rgb(68, 68, 68);">GetFieldID</font>` | `<font style="color:rgb(68, 68, 68);">JNIEnv *env, jclass clazz, const char *name, const char *sig</font>` | <font style="color:rgb(68, 68, 68);">回Java类（非静态）域的属性ID。该域由其名称及签名指定。访问器函数的Get<type>Field 及 Set<type>Field系列使用域 ID 检索对象域。GetFieldID() 不能用于获取数组的长度域。应使用GetArrayLength()。</font> | <font style="color:rgb(68, 68, 68);">-</font> |
| `<font style="color:rgb(68, 68, 68);">GetStaticFieldID</font>` | `<font style="color:rgb(68, 68, 68);">JNIEnv *env,jclass clazz, const char *name, const char *sig</font>` | <font style="color:rgb(68, 68, 68);">获取类的静态域ID方法</font> | <font style="color:rgb(68, 68, 68);">-</font> |
| `<font style="color:rgb(68, 68, 68);">Call<type>Method</font>`<br/><font style="color:rgb(68, 68, 68);">,</font><font style="color:rgb(68, 68, 68);"> </font>`<font style="color:rgb(68, 68, 68);">Call<type>MethodA</font>`<br/><font style="color:rgb(68, 68, 68);">,</font><font style="color:rgb(68, 68, 68);"> </font>`<font style="color:rgb(68, 68, 68);">Call<type>MethodV</font>` | `<font style="color:rgb(68, 68, 68);">JNIEnv *env, jobject obj, jmethodID methodID, .../jvalue *args/va_list args</font>` | <font style="color:rgb(68, 68, 68);">这三个操作的方法用于从本地方法调用Java 实例方法。它们的差别仅在于向其所调用的方法传递参数时所用的机制。</font> | <font style="color:rgb(68, 68, 68);">NativeType，具体的返回值取决于调用的类型</font> |


## <font style="color:rgb(68, 68, 68);">2.Hook_Libc</font>
`<font style="color:rgb(68, 68, 68);">libc.so</font>`<font style="color:rgb(68, 68, 68);">: 这是一个标准的 C 语言库，用于提供基本的系统调用和功能，如文件操作、字符串处理、内存分配等。在Android系统中，</font>`<font style="color:rgb(68, 68, 68);">libc</font>`<font style="color:rgb(68, 68, 68);"> </font><font style="color:rgb(68, 68, 68);">是最基础的库之一。</font>

| **<font style="color:rgb(68, 68, 68);">类别</font>** | **<font style="color:rgb(68, 68, 68);">函数名称</font>** | **<font style="color:rgb(68, 68, 68);">参数</font>** | **<font style="color:rgb(68, 68, 68);">描述</font>** |
| --- | --- | --- | --- |
| <font style="color:rgb(68, 68, 68);">字符串类操作</font> | <font style="color:rgb(68, 68, 68);">strcpy</font> | `<font style="color:rgb(68, 68, 68);">char *dest, const char *src</font>` | <font style="color:rgb(68, 68, 68);">将字符串 src 复制到 dest</font> |
| | <font style="color:rgb(68, 68, 68);">strcat</font> | `<font style="color:rgb(68, 68, 68);">char *dest, const char *src</font>` | <font style="color:rgb(68, 68, 68);">将字符串 src 连接到 dest 的末尾</font> |
| | <font style="color:rgb(68, 68, 68);">strlen</font> | `<font style="color:rgb(68, 68, 68);">const char *str</font>` | <font style="color:rgb(68, 68, 68);">返回 str 的长度</font> |
| | <font style="color:rgb(68, 68, 68);">strcmp</font> | `<font style="color:rgb(68, 68, 68);">const char *str1, const char *str2</font>` | <font style="color:rgb(68, 68, 68);">比较两个字符串</font> |
| <font style="color:rgb(68, 68, 68);">文件类操作</font> | <font style="color:rgb(68, 68, 68);">fopen</font> | `<font style="color:rgb(68, 68, 68);">const char *filename, const char *mode</font>` | <font style="color:rgb(68, 68, 68);">打开文件</font> |
| | <font style="color:rgb(68, 68, 68);">fread</font> | `<font style="color:rgb(68, 68, 68);">void *ptr, size_t size, size_t count, FILE *stream</font>` | <font style="color:rgb(68, 68, 68);">从文件读取数据</font> |
| | <font style="color:rgb(68, 68, 68);">fwrite</font> | `<font style="color:rgb(68, 68, 68);">const void *ptr, size_t size, size_t count, FILE *stream</font>` | <font style="color:rgb(68, 68, 68);">写入数据到文件</font> |
| | <font style="color:rgb(68, 68, 68);">fclose</font> | `<font style="color:rgb(68, 68, 68);">FILE *stream</font>` | <font style="color:rgb(68, 68, 68);">关闭文件</font> |
| <font style="color:rgb(68, 68, 68);">网络IO类操作</font> | <font style="color:rgb(68, 68, 68);">socket</font> | `<font style="color:rgb(68, 68, 68);">int domain, int type, int protocol</font>` | <font style="color:rgb(68, 68, 68);">创建网络套接字</font> |
| | <font style="color:rgb(68, 68, 68);">connect</font> | `<font style="color:rgb(68, 68, 68);">int sockfd, const struct sockaddr *addr, socklen_t addrlen</font>` | <font style="color:rgb(68, 68, 68);">连接套接字</font> |
| | <font style="color:rgb(68, 68, 68);">recv</font> | `<font style="color:rgb(68, 68, 68);">int sockfd, void *buf, size_t len, int flags</font>` | <font style="color:rgb(68, 68, 68);">从套接字接收数据</font> |
| | <font style="color:rgb(68, 68, 68);">send</font> | `<font style="color:rgb(68, 68, 68);">int sockfd, const void *buf, size_t len, int flags</font>` | <font style="color:rgb(68, 68, 68);">通过套接字发送数据</font> |
| <font style="color:rgb(68, 68, 68);">线程类操作</font> | <font style="color:rgb(68, 68, 68);">pthread_create</font> | `<font style="color:rgb(68, 68, 68);">pthread_t *thread, const pthread_attr_t *attr, void *(*start_routine)(void *), void *arg</font>` | <font style="color:rgb(68, 68, 68);">创建线程</font> |
| <font style="color:rgb(68, 68, 68);">进程控制操作</font> | <font style="color:rgb(68, 68, 68);">kill</font> | `<font style="color:rgb(68, 68, 68);">pid_t pid, int sig</font>` | <font style="color:rgb(68, 68, 68);">向指定进程发送信号</font> |
| <font style="color:rgb(68, 68, 68);">系统属性查询操作</font> | `<font style="color:rgb(68, 68, 68);">__system_property_get</font>` | `<font style="color:rgb(68, 68, 68);">const char *name, char *value</font>` | <font style="color:rgb(68, 68, 68);">从Android系统属性服务中读取指定属性的值</font> |
| | <font style="color:rgb(68, 68, 68);">uname</font> | `<font style="color:rgb(68, 68, 68);">struct utsname *buf</font>` | <font style="color:rgb(68, 68, 68);">获取当前系统的名称、版本和其他相关信息</font> |
| | <font style="color:rgb(68, 68, 68);">sysconf</font> | `<font style="color:rgb(68, 68, 68);">int name</font>` | <font style="color:rgb(68, 68, 68);">获取运行时系统的配置信息，如CPU数量、页大小</font> |


## <font style="color:rgb(68, 68, 68);">3.Hook_Libdl</font>
`<font style="color:rgb(68, 68, 68);">libdl.so</font>`<font style="color:rgb(68, 68, 68);">是一个处理动态链接和加载的标准库，它提供了</font>`<font style="color:rgb(68, 68, 68);">dlopen</font>`<font style="color:rgb(68, 68, 68);">、</font>`<font style="color:rgb(68, 68, 68);">dlclose</font>`<font style="color:rgb(68, 68, 68);">、</font>`<font style="color:rgb(68, 68, 68);">dlsym</font>`<font style="color:rgb(68, 68, 68);">等函数，用于在运行时动态地加载和使用共享库</font>

| **<font style="color:rgb(68, 68, 68);">类别</font>** | **<font style="color:rgb(68, 68, 68);">函数名称</font>** | **<font style="color:rgb(68, 68, 68);">参数</font>** | **<font style="color:rgb(68, 68, 68);">描述</font>** |
| --- | --- | --- | --- |
| <font style="color:rgb(68, 68, 68);">动态链接库操作</font> | <font style="color:rgb(68, 68, 68);">dlopen</font> | `<font style="color:rgb(68, 68, 68);">const char *filename, int flag</font>` | <font style="color:rgb(68, 68, 68);">打开动态链接库文件</font> |
| | <font style="color:rgb(68, 68, 68);">dlsym</font> | `<font style="color:rgb(68, 68, 68);">void *handle, const char *symbol</font>` | <font style="color:rgb(68, 68, 68);">从动态链接库中获取符号地址</font> |


# 
