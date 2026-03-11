/**
 ****************************************************************************************************
 * @file        bsp_step_motor.h
 * @author      普中科技
 * @version     V1.0
 * @date        2024-06-05
 * @brief       步进电机实验
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

#ifndef BSP_STEP_MOTOR_H
#define BSP_STEP_MOTOR_H

#include "cmsis_os2.h"
#include "hi_io.h"
#include "hi_gpio.h"

// 定义步进电机速度，值越小，速度越快
// 最小不能小于1
#define STEPMOTOR_MAXSPEED        1  
#define STEPMOTOR_MINSPEED        5  

//管脚定义
#define IN1_PIN             HI_IO_NAME_GPIO_1
#define IN1_GPIO_FUN        HI_IO_FUNC_GPIO_1_GPIO

#define IN2_PIN             HI_IO_NAME_GPIO_5
#define IN2_GPIO_FUN        HI_IO_FUNC_GPIO_5_GPIO

#define IN3_PIN             HI_IO_NAME_GPIO_6
#define IN3_GPIO_FUN        HI_IO_FUNC_GPIO_6_GPIO

#define IN4_PIN             HI_IO_NAME_GPIO_7
#define IN4_GPIO_FUN        HI_IO_FUNC_GPIO_7_GPIO

#define MOTOR_IN1(a)        hi_gpio_set_ouput_val(IN1_PIN,a)
#define MOTOR_IN2(a)        hi_gpio_set_ouput_val(IN2_PIN,a)
#define MOTOR_IN3(a)        hi_gpio_set_ouput_val(IN3_PIN,a)
#define MOTOR_IN4(a)        hi_gpio_set_ouput_val(IN4_PIN,a)

//函数声明
void step_motor_init(void);
void step_motor_run(uint8_t step,uint8_t dir,uint8_t speed,uint16_t angle,uint8_t sta);

#endif
