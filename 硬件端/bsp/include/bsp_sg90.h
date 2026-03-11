/**
 ****************************************************************************************************
 * @file        bsp_sg90.h
 * @author      普中科技
 * @version     V1.0
 * @date        2024-06-05
 * @brief       SG90舵机实验
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

#ifndef BSP_SG90_H
#define BSP_SG90_H

#include "cmsis_os2.h"
#include "hi_io.h"
#include "hi_gpio.h"


//管脚定义
#define SG90_PIN         HI_IO_NAME_GPIO_5
#define SG90_GPIO_FUN    HI_IO_FUNC_GPIO_5_GPIO


//函数声明
void sg90_init(void);
void set_sg90_angle(uint16_t angle);

#endif
