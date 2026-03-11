/**
 ****************************************************************************************************
 * @file        bsp_pwm.c
 * @author      普中科技
 * @version     V1.0
 * @date        2024-06-05
 * @brief       呼吸灯实验
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

#include "bsp_pwm.h"
#include <unistd.h>
#include "bsp_led.h"
#include "hi_pwm.h"


//PWM初始化
void pwm_init(void)
{
    hi_gpio_init();                                            // GPIO初始化
    hi_io_set_func(LED_PIN, HI_IO_FUNC_GPIO_2_PWM2_OUT);       // 设置IO为GPIO功能
    hi_gpio_set_dir(LED_PIN, HI_GPIO_DIR_OUT);                 // 设置GPIO为输出模式
    hi_pwm_init(HI_PWM_PORT_PWM2);
}

//pwm占空比输出调节
void pwm_set_duty(uint16_t duty)
{
    hi_pwm_start(HI_PWM_PORT_PWM2,duty,40000);
}

