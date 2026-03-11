/**
 ****************************************************************************************************
 * @file        bsp_mqtt.h
 * @author      普中科技
 * @version     V1.0
 * @date        2024-06-05
 * @brief       WIFI MQTT实验
 * @license     Copyright (c) 2024-2034, 深圳市普中科技有限公司
 ****************************************************************************************************
 * @attention
 *
 * 实验平台:普中-Hi3861
 * 在线视频:https://space.bilibili.com/2146492485
 * 公司网址:www.prechin.cn
 * 购买地址:
 *
 */

#ifndef BSP_MQTT_H
#define BSP_MQTT_H

#include "cmsis_os2.h"
#include "hi_io.h"
#include "hi_gpio.h"


//函数声明
int MQTTClient_connectServer(const char *ip_addr, int ip_port);
int MQTTClient_unConnectServer(void);
int MQTTClient_subscribe(char *subTopic);
int MQTTClient_init(char *clientID, char *userName, char *password);
int MQTTClient_pub(char *pub_Topic, unsigned char *payloadData, int payloadLen);
int MQTTClient_sub(void);
extern int8_t(*p_MQTTClient_sub_callback)(unsigned char *topic, unsigned char *payload);

#endif
