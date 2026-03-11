/**
 ****************************************************************************************************
 * @file        bsp_time.c
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

#include "bsp_time.h"
#include <unistd.h>
#include "bsp_led.h"
#include "hi_timer.h"


hi_u32 timer_handle;
uint16_t g_times=0;

//定时器回调函数
void time_isr_fun(void)
{
    static uint8_t i=0;
    i=!i; 
    LED(i);
}

//定时器初始化
//times：定时时间，ms
void time_init(uint16_t times)
{
    hi_u32 ret;
    g_times=times; 
    ret = hi_timer_create(&timer_handle);
    if(ret!=HI_ERR_SUCCESS)
    {
        printf("Timer_Create failed\r\n");
    }
    hi_timer_start(timer_handle,HI_TIMER_TYPE_PERIOD,times,(hi_timer_callback_f)time_isr_fun,NULL);
}

//定时器开关
void time_onoff(uint8_t sta)
{
    if(sta==0)hi_timer_stop(timer_handle);
    else hi_timer_start(timer_handle,HI_TIMER_TYPE_PERIOD,g_times,(hi_timer_callback_f)time_isr_fun,NULL);
}

