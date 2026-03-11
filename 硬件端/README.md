# WiFi开发项目文档

## 项目概述
本项目是一个基于HarmonyOS的WiFi开发项目，主要实现了WiFi的连接、扫描、配置等功能。项目采用模块化设计，提供了完整的WiFi服务接口。

## 项目结构
```
.
├── wifi_lite/                # WiFi核心服务组件
│   ├── interfaces/          # 对外接口定义
│   └── README_zh.md        # 中文说明文档
├── wifiservice/            # WiFi服务实现
│   ├── wifi_device.h       # WiFi设备接口定义
│   ├── wifi_hotspot.h      # WiFi热点接口定义
│   └── wifi_event.h        # WiFi事件处理接口
├── bsp/                    # 板级支持包
├── third_party/           # 第三方依赖
└── BUILD.gn               # 构建配置文件
```

## 功能特性
1. WiFi基础功能
   - WiFi开启/关闭
   - WiFi扫描
   - WiFi连接/断开
   - WiFi状态监控

2. WiFi热点功能
   - 热点创建/关闭
   - 热点配置
   - 热点状态管理

3. WiFi安全功能
   - WPA/WPA2加密支持
   - WAPI加密支持
   - 密码管理

## 开发环境要求
- 操作系统：支持Windows/Linux
- 开发板：wifi-iot开发板
- 编译工具：GN构建系统
- 编程语言：C语言

## 快速开始

### 1. 初始化WiFi
```c
WifiErrorCode error = EnableWifi();
if (error != WIFI_SUCCESS) {
    // 错误处理
    return;
}
```

### 2. 扫描WiFi网络
```c
WifiErrorCode error = Scan();
if (error != WIFI_SUCCESS) {
    // 错误处理
    return;
}
```

### 3. 获取扫描结果
```c
WifiScanInfo* infoList = malloc(sizeof(WifiScanInfo) * WIFI_SCAN_HOTSPOT_LIMIT);
unsigned int size = WIFI_SCAN_HOTSPOT_LIMIT;
error = GetScanInfoList(infoList, &size);
if (error != WIFI_SUCCESS || size == 0) {
    // 错误处理
    return;
}
```

### 4. 配置WiFi连接
```c
WifiDeviceConfig config = {0};
config.freq = 20;
config.securityType = WIFI_SEC_TYPE_PSK;
config.wapiPskType = WIFI_PSK_TYPE_ASCII;
memcpy_s(config.ssid, WIFI_MAX_SSID_LEN, "YourSSID", strlen("YourSSID"));
memcpy_s(config.preSharedKey, WIFI_MAX_KEY_LEN, "YourPassword", strlen("YourPassword"));
```

## API说明

### WiFi设备接口
- `EnableWifi()`: 启用WiFi
- `DisableWifi()`: 禁用WiFi
- `Scan()`: 扫描WiFi网络
- `GetScanInfoList()`: 获取扫描结果
- `ConnectTo()`: 连接到指定网络
- `Disconnect()`: 断开当前连接

### WiFi热点接口
- `EnableHotspot()`: 启用热点
- `DisableHotspot()`: 禁用热点
- `SetHotspotConfig()`: 配置热点参数
- `GetHotspotConfig()`: 获取热点配置

