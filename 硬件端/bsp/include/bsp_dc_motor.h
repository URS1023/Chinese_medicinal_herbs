/**
 ****************************************************************************************************
 * @file        bsp_dc_motor.h
 * @author      普中科技
 * @version     V1.0
 * @date        2024-06-05
 * @brief       直流电机实验
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

#ifndef BSP_DC_MOTOR_H
#define BSP_DC_MOTOR_H

#include "cmsis_os2.h"
#include "hi_io.h"
#include "hi_gpio.h"

//管脚定义
#define DC_MOTOR_PIN         HI_IO_NAME_GPIO_14
#define DC_MOTOR_GPIO_FUN    HI_IO_FUNC_GPIO_14_GPIO

#define DC_MOTOR(a)          hi_gpio_set_ouput_val(DC_MOTOR_PIN,a)

//函数声明
void dc_motor_init(void);


#endif
