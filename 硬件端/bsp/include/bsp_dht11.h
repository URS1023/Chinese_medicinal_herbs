/**
 ****************************************************************************************************
 * @file        bsp_dht11.h
 * @author      普中科技
 * @version     V1.0
 * @date        2024-06-05
 * @brief       DHT11温湿度传感器实验
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

#ifndef BSP_DHT11_H
#define BSP_DHT11_H

#include "cmsis_os2.h"
#include "hi_io.h"
#include "hi_gpio.h"

//管脚定义
#define DHT11_PIN         HI_IO_NAME_GPIO_7
#define DHT11_GPIO_FUN    HI_IO_FUNC_GPIO_7_GPIO

#define DHT11_DQ_OUT(a)   hi_gpio_set_ouput_val(DHT11_PIN,a)

//函数声明
void dht11_io_out(void);
void dht11_io_in(void);
void dht11_reset(void);
uint8_t dht11_check(void);
uint8_t dht11_read_bit(void);
uint8_t dht11_read_byte(void);
uint8_t dht11_read_data(uint8_t *temp,uint8_t *humi) ;
uint8_t dht11_init(void);

#endif
