/**
 ****************************************************************************************************
 * @file        template.c
 * @author      普中科技
 * @version     V1.0
 * @date        2024-06-05
 * @brief       WIFI 华为IoTDA设备接入实验
 * @license     Copyright (c) 2024-2034, 深圳市普中科技有限公司
 ****************************************************************************************************
 * @attention
 *
 * 实验平台:普中-Hi3861
 * 在线视频:https://space.bilibili.com/2146492485
 * 公司网址:www.prechin.cn
 * 购买地址:
 *
 ****************************************************************************************************
 * 实验现象：开发板连接路由器热点，在浏览器输入www.huaweicloud.com，注册账号，添加产品和设备等属性，
 *          打开串口调试助手，观察输出结果，连接好后，设备变为在线状态，可显示温度值，也可通过云端控制
 *          板载LED亮灭。
 *
 ****************************************************************************************************
 */

#include <stdio.h>
#include <unistd.h>

#include "ohos_init.h"
#include "cmsis_os2.h"

#include "bsp_led.h"
#include "bsp_ds18b20.h"
#include "bsp_wifi.h"
#include "bsp_mqtt.h"

#include "lwip/netifapi.h"
#include "lwip/sockets.h"
#include "lwip/api_shell.h"

#include "cJSON.h"
#include "test1.c"

#include "bsp_dht11.h"
//WIFI连接热点和密码
#define WIFI_SSID "10234"
#define WIFI_PAWD "12345689.@"

//注册华为云后需要更新的信息
// 产品ID
#define DEVICE_ID "6749b788ef99673c8ad11961"
// 设备密匙 78b6f8eb8882be41f6844b29bdab5eb2
// MQTT客户端ID  clientId
#define MQTT_CLIENT_ID "6749b788ef99673c8ad11961_hi3861_led_0_0_2024112914" 
// MQTT用户名
#define MQTT_USER_NAME "6749b788ef99673c8ad11961_hi3861_led"
// MQTT密码
#define MQTT_PASS_WORD "5718f386f38801aa3ebc572c7439bf23d976e059c40768a6fbe0fa62c6f3a79b"
// 华为云平台的IP地址
#define SERVER_IP_ADDR "117.78.5.125"
// 华为云平台的IP端口号
#define SERVER_IP_PORT 1883
// 订阅 接收控制命令的主题
#define MQTT_TOPIC_SUB_COMMANDS "$oc/devices/%s/sys/commands/#"
// 发布 成功接收到控制命令后的主题
#define MQTT_TOPIC_PUB_COMMANDS_REQ "$oc/devices/%s/sys/commands/response/request_id=%s"
#define MALLOC_MQTT_TOPIC_PUB_COMMANDS_REQ "$oc/devices//sys/commands/response/request_id="

// 发布 设备属性数据的主题
#define MQTT_TOPIC_PUB_PROPERTIES "$oc/devices/%s/sys/properties/report"
#define MALLOC_MQTT_TOPIC_PUB_PROPERTIES "$oc/devices//sys/properties/report"

#define TASK_STACK_SIZE (1024 * 10)
#define MsgQueueObjectNumber 16 // 定义消息队列对象的个数



typedef struct message_sensorData {
    uint8_t led;        // LED灯当前的状态
    float temperature;  // 当前的温度值
    uint8_t humi;
    uint8_t sound;
    uint8_t tilt;
    uint8_t vibrate;
    uint8_t fire;
    uint8_t smoke;
    uint8_t light_sense;
    // uint8_t fire;
    
} msg_sensorData_t;

msg_sensorData_t sensorData = {0}; // 传感器的数据
osThreadId_t mqtt_send_task_id; // mqtt 发布数据任务ID
osThreadId_t mqtt_recv_task_id; // mqtt 接收数据任务ID
#define MQTT_SEND_TASK_TIME 3 // s
#define MQTT_RECV_TASK_TIME 1 // s
#define TASK_INIT_TIME 2 // s
#define DISPLAY_BUFF_MAX 64
#define MQTT_DATA_MAX 256
uint8_t publish_topic[MQTT_DATA_MAX] = {0};
uint8_t mqtt_data[MQTT_DATA_MAX] = {0};


/**
 * @brief 组JSON数据
 */
int Packaged_json_data(void)
{
    cJSON *root = NULL, *array = NULL, *services = NULL;
    cJSON *properties = NULL;
    int ret = 0;

    // 组JSON数据
    root = cJSON_CreateObject(); // 创建一个对象
    services = cJSON_CreateArray();
    cJSON_AddItemToObject(root, "services", services);
    array = cJSON_CreateObject();
    cJSON_AddStringToObject(array, "service_id", "attribute");
    properties = cJSON_CreateObject();
    cJSON_AddItemToObject(array, "properties", properties);
    cJSON_AddStringToObject(properties, "led", sensorData.led ? "ON" : "OFF");
    // cJSON_AddNumberToObject(properties, "temperature", (int)sensorData.temperature);
    cJSON_AddNumberToObject(properties, "temp", (int)sensorData.temperature);
    cJSON_AddNumberToObject(properties, "humi", (int)sensorData.humi);
    cJSON_AddNumberToObject(properties, "sound", (int)sensorData.sound);
    cJSON_AddNumberToObject(properties, "tilt", (int)sensorData.tilt);
    cJSON_AddNumberToObject(properties, "vibrate", (int)sensorData.vibrate);
    cJSON_AddNumberToObject(properties, "fire", (int)sensorData.fire);
    cJSON_AddNumberToObject(properties, "smoke", (int)sensorData.smoke);
    cJSON_AddNumberToObject(properties, "light_sense", (int)sensorData.light_sense);
    cJSON_AddItemToArray(services, array);  // 将对象添加到数组中

    /* 格式化打印创建的带数组的JSON对象 */
    char *str_print = cJSON_PrintUnformatted(root);
    if (str_print != NULL) {
        // printf("%s\n", str_print);
        if (strcpy_s(mqtt_data, strlen(str_print) + 1, str_print) == 0) {
            ret = 0;
        } else {
            ret = -1;
        }
        cJSON_free(str_print);
    } else {
        ret = -1;
    }
    if (root != NULL) {
        cJSON_Delete(root);
    } else {
        ret = -1;
    }
    properties = str_print = root = array = services = NULL;

    return ret;
}

int get_jsonData_value(const cJSON *const object, uint8_t *value)
{
    cJSON *json_value = NULL;
    int ret = -1;
    json_value = cJSON_GetObjectItem(object, "value");
    if (json_value) {
        if (!strcmp(json_value->valuestring, "ON")) {
            *value = 1;
            json_value = NULL;
            ret = 0; // 0为成功
        } else if (!strcmp(json_value->valuestring, "OFF")) {
            *value = 0;
            json_value = NULL;
            ret = 0;
        }
    }
    json_value = NULL;
    return ret; // -1为失败
}

/**
 * @brief 解析JSON数据
 */
int Parsing_json_data(const char *payload)
{
    cJSON *root = NULL, *command_name = NULL, *paras = NULL, *value = NULL;
    cJSON *red = NULL, *green = NULL, *blue = NULL;
    int ret_code = 1;
    root = cJSON_Parse((const char *)payload);
    if (root) {
        // 解析JSON数据
        command_name = cJSON_GetObjectItem(root, "command_name");
        paras = cJSON_GetObjectItem(root, "paras");
        if (command_name)
        {
            if (!strcmp(command_name->valuestring, "led")) 
            {
                ret_code = get_jsonData_value(paras, &sensorData.led);
            } 
        }
    }
    cJSON_Delete(root);
    root = command_name = paras = value = red = green = blue = NULL;
    (sensorData.led == 1) ? LED(1) : LED(0);

    return ret_code;
}


/**
 * @brief MQTT  发布消息任务
 */
void mqtt_send_task(void)
{
    while (1) 
    {
        // 获取传感器的数据
        sensorData.temperature=re_temp();
        sensorData.humi=re_humi();
        sensorData.sound=re_sound();
        sensorData.tilt=re_tilt();
        sensorData.vibrate=re_vibrate();
        sensorData.fire=re_fire();
        sensorData.smoke=re_somke();
        sensorData.light_sense=re_light();
        sleep(1.5);
        // // 组Topic
        memset_s(publish_topic, MQTT_DATA_MAX, 0, MQTT_DATA_MAX);
        if (sprintf_s(publish_topic, MQTT_DATA_MAX, MQTT_TOPIC_PUB_PROPERTIES, DEVICE_ID) > 1) 
        {
            // 组JSON数据
            Packaged_json_data();
            // 发布消息
            MQTTClient_pub(publish_topic, mqtt_data, strlen((char *)mqtt_data));
        }
    }
    sleep(MQTT_SEND_TASK_TIME);
}

// 向云端发送返回值
void send_cloud_request_code(const char *request_id, int ret_code, int request_len)
{
    char *request_topic = (char *)malloc(strlen(MALLOC_MQTT_TOPIC_PUB_COMMANDS_REQ) +
                                            strlen(DEVICE_ID) + request_len + 1);
    if (request_topic != NULL) 
    {
        memset_s(request_topic,
                 strlen(DEVICE_ID) + strlen(MALLOC_MQTT_TOPIC_PUB_COMMANDS_REQ) + request_len + 1,
                 0,
                 strlen(DEVICE_ID) + strlen(MALLOC_MQTT_TOPIC_PUB_COMMANDS_REQ) + request_len + 1);
        if (sprintf_s(request_topic,
                      strlen(DEVICE_ID) + strlen(MALLOC_MQTT_TOPIC_PUB_COMMANDS_REQ) + request_len + 1,
                      MQTT_TOPIC_PUB_COMMANDS_REQ, DEVICE_ID, request_id) > 0) 
        {
            if (ret_code == 0) 
            {
                MQTTClient_pub(request_topic, "{\"result_code\":0}", strlen("{\"result_code\":0}"));
            } 
            else if (ret_code == 1) 
            {
                MQTTClient_pub(request_topic, "{\"result_code\":1}", strlen("{\"result_code\":1}"));
            }
        }
        free(request_topic);
        request_topic = NULL;
    }
}

/**
 * @brief MQTT接收数据的回调函数
 */
int8_t mqttClient_sub_callback(unsigned char *topic, unsigned char *payload)
{
    if ((topic == NULL) || (payload == NULL)) 
    {
        return -1;
    } 
    else 
    {
        printf("topic: %s\r\n", topic);
        printf("payload: %s\r\n", payload);

        // 提取出topic中的request_id
        char request_id[50] = {0};
        int ret_code = 1; // 1为失败
        if (0 == strcpy_s(request_id, sizeof(request_id),
                          topic + strlen(DEVICE_ID) + strlen("$oc/devices//sys/commands/request_id="))) {
            printf("request_id: %s\r\n", request_id);
            // 解析JSON数据
            ret_code = Parsing_json_data(payload);
            send_cloud_request_code(request_id, ret_code, sizeof(request_id));
        }
    }
    return 0;
}

/**
 * @brief MQTT  接收消息任务
 */
void mqtt_recv_task(void)
{
    while (1) 
    {
        MQTTClient_sub();
        sleep(MQTT_RECV_TASK_TIME);
    }
}

//硬件初始化
void hardware_init(void)
{
    led_init();//LED初始化


    p_MQTTClient_sub_callback = &mqttClient_sub_callback;

    // 连接WiFi
    if (WiFi_connectHotspots(WIFI_SSID, WIFI_PAWD) != WIFI_SUCCESS) {
        printf("[error] connectWiFiHotspots\r\n");
    }
    sleep(TASK_INIT_TIME);

    // 连接MQTT服务器
    if (MQTTClient_connectServer(SERVER_IP_ADDR, SERVER_IP_PORT) != WIFI_SUCCESS) {
        printf("[error] mqttClient_connectServer\r\n");
    }
    sleep(TASK_INIT_TIME);

    // 初始化MQTT客户端
    if (MQTTClient_init(MQTT_CLIENT_ID, MQTT_USER_NAME, MQTT_PASS_WORD) != WIFI_SUCCESS) {
        printf("[error] mqttClient_init\r\n");
    }
    sleep(TASK_INIT_TIME); 

    // 订阅主题
    if (MQTTClient_subscribe(MQTT_TOPIC_SUB_COMMANDS) != WIFI_SUCCESS) {
        printf("[error] mqttClient_subscribe\r\n");
    }
    sleep(TASK_INIT_TIME);
}

//任务创建
void wifi_iotda_task_create(void)
{
    osThreadAttr_t taskOptions;
    taskOptions.name = "mqtt_send_task";       // 任务的名字
    taskOptions.attr_bits = 0;               // 属性位
    taskOptions.cb_mem = NULL;               // 堆空间地址
    taskOptions.cb_size = 0;                 // 堆空间大小
    taskOptions.stack_mem = NULL;            // 栈空间地址
    taskOptions.stack_size = TASK_STACK_SIZE;           // 栈空间大小 单位:字节
    taskOptions.priority = osPriorityNormal; // 任务的优先级

    mqtt_send_task_id = osThreadNew((osThreadFunc_t)mqtt_send_task, NULL, &taskOptions); // 创建任务
    if (mqtt_send_task_id != NULL)
    {
        printf("ID = %d, mqtt_send_task_id Create OK!\n", mqtt_send_task_id);
    }

    taskOptions.name = "mqtt_recv_task";
    taskOptions.stack_size = TASK_STACK_SIZE;
    mqtt_recv_task_id = osThreadNew((osThreadFunc_t)mqtt_recv_task, NULL, &taskOptions);
    if (mqtt_recv_task_id != NULL) {
        printf("ID = %d, Create mqtt_recv_task_id is OK!\r\n", mqtt_recv_task_id);
    }
}

/**
 * @description: 初始化并创建任务
 * @param {*}
 * @return {*}
 */
static void template_demo(void)
{
    printf("普中-Hi3861开发板--WIFI 华为IoTDA设备接入实验\r\n");
    hardware_init();//硬件初始化
    wifi_iotda_task_create();//任务创建
}
SYS_RUN(template_demo);
