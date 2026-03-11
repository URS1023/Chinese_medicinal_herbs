/**
 ****************************************************************************************************
 * @file        bsp_time.h
 * @author      普中科技
 * @version     V1.0
 * @date        2024-06-05
 * @brief       定时器中断实验
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

#ifndef BSP_TIME_H
#define BSP_TIME_H

#include "cmsis_os2.h"
#include "hi_io.h"
#include "hi_gpio.h"



//函数声明
void time_init(uint16_t times);
void time_onoff(uint8_t sta);

#endif
