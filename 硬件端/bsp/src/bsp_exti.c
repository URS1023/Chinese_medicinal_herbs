/**
 ****************************************************************************************************
 * @file        bsp_exti.c
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

#include "bsp_exti.h"
#include <unistd.h>
#include "bsp_led.h"


//key1按键回调函数
hi_void key1_exti_callback(void)
{
    static uint8_t key1=0;
    usleep(10*1000);//消抖
    hi_gpio_get_input_val(KEY1_PIN,&key1);
    if(key1==0)
    {
        LED(1);
    }
}

//key2按键回调函数
hi_void key2_exti_callback(void)
{
    static uint8_t key2=0;
    usleep(10*1000);//消抖
    hi_gpio_get_input_val(KEY2_PIN,&key2);
    if(key2==0)
    {
        LED(0);
    }
}

//外部中断初始化
void exti_init(void)
{
    hi_gpio_init();                                            // GPIO初始化
    hi_io_set_pull(KEY1_PIN, HI_IO_PULL_UP);                   // 设置GPIO上拉
    hi_io_set_func(KEY1_PIN, KEY1_GPIO_FUN);                   // 设置IO为GPIO功能
    hi_gpio_set_dir(KEY1_PIN, HI_GPIO_DIR_IN);                // 设置GPIO为输入模式
    hi_gpio_register_isr_function(KEY1_PIN,                         // 按键引脚
                                  HI_INT_TYPE_EDGE,            // 下降沿检测
                                  HI_GPIO_EDGE_FALL_LEVEL_LOW, // 低电平时触发
                                  &key1_exti_callback,         // 触发后调用的回调函数
                                  NULL);                       // 回调函数的传参值

    hi_io_set_pull(KEY2_PIN, HI_IO_PULL_UP);                   // 设置GPIO上拉
    hi_io_set_func(KEY2_PIN, KEY2_GPIO_FUN);                   // 设置IO为GPIO功能
    hi_gpio_set_dir(KEY2_PIN, HI_GPIO_DIR_IN);                // 设置GPIO为输入模式
    hi_gpio_register_isr_function(KEY2_PIN,                         // 按键引脚
                                  HI_INT_TYPE_EDGE,            // 下降沿检测
                                  HI_GPIO_EDGE_FALL_LEVEL_LOW, // 低电平时触发
                                  &key2_exti_callback,         // 触发后调用的回调函数
                                  NULL);                       // 回调函数的传参值
}

