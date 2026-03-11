/**
 ****************************************************************************************************
 * @file        bsp_ds18b20.h
 * @author      普中科技
 * @version     V1.0
 * @date        2024-06-05
 * @brief       DS18B20温度传感器实验
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

#ifndef BSP_DS18B20_H
#define BSP_DS18B20_H

#include "cmsis_os2.h"
#include "hi_io.h"
#include "hi_gpio.h"

//管脚定义
#define DS18B20_PIN         HI_IO_NAME_GPIO_7
#define DS18B20_GPIO_FUN    HI_IO_FUNC_GPIO_7_GPIO

#define DS18B20_DQ_OUT(a)   hi_gpio_set_ouput_val(DS18B20_PIN,a)

//函数声明
void ds18b20_io_out(void);
void ds18b20_io_in(void);
void ds18b20_reset(void);
uint8_t ds18b20_check(void);
uint8_t ds18b20_read_bit(void);
uint8_t ds18b20_read_byte(void);
void ds18b20_write_byte(uint8_t dat);
void ds18b20_start(void);
uint8_t ds18b20_init(void);
float ds18b20_gettemperture(void);

#endif
