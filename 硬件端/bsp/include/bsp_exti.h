/**
 ****************************************************************************************************
 * @file        bsp_exti.h
 * @author      普中科技
 * @version     V1.0
 * @date        2024-06-05
 * @brief       外部中断实验
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

#ifndef BSP_EXTI_H
#define BSP_EXTI_H

#include "cmsis_os2.h"
#include "hi_io.h"
#include "hi_gpio.h"


//管脚定义
#define KEY1_PIN         HI_IO_NAME_GPIO_11
#define KEY1_GPIO_FUN    HI_IO_FUNC_GPIO_11_GPIO

#define KEY2_PIN         HI_IO_NAME_GPIO_12
#define KEY2_GPIO_FUN    HI_IO_FUNC_GPIO_12_GPIO


//函数声明
void exti_init(void);

#endif
