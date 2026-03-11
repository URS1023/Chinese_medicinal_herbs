/**
 ****************************************************************************************************
 * @file        bsp_adc.h
 * @author      普中科技
 * @version     V1.0
 * @date        2024-06-05
 * @brief       ADC实验
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

#ifndef BSP_ADC_H
#define BSP_ADC_H

#include "cmsis_os2.h"
#include "hi_io.h"
#include "hi_gpio.h"

//管脚定义
#define ADC5_PIN         HI_IO_NAME_GPIO_11

//函数声明
void adc5_init(void);
uint16_t get_adc5_value(void);
float get_adc5_voltage(void);

#endif
