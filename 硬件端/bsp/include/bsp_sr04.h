/**
 ****************************************************************************************************
 * @file        bsp_sr04.h
 * @author      普中科技
 * @version     V1.0
 * @date        2024-06-05
 * @brief       HC-SR04超声波测距实验
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

#ifndef BSP_SR04_H
#define BSP_SR04_H

#include "cmsis_os2.h"
#include "hi_io.h"
#include "hi_gpio.h"

//管脚定义
#define TRIG_PIN            HI_IO_NAME_GPIO_13
#define TRIG_GPIO_FUN       HI_IO_FUNC_GPIO_13_GPIO

#define ECHO_PIN            HI_IO_NAME_GPIO_14
#define ECHO_GPIO_FUN       HI_IO_FUNC_GPIO_14_GPIO

#define TRIG(a)             hi_gpio_set_ouput_val(TRIG_PIN,a)

//函数声明
void sr04_init(void);
float sr04_read_distance(void);

#endif
