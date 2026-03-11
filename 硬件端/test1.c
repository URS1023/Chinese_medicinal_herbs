/**
 ****************************************************************************************************
 * @file        template.c
 * @author      普中科技
 * @version     V1.0
 * @date        2024-06-05
 * @brief       倾斜传感器模块实验
 * @license     Copyright (c) 2024-2034, 深圳市普中科技有限公司
 ****************************************************************************************************
 * @attention
 *
 * 实验平台:普中-Hi3861
 * 在线视频:https://space.bilibili.com/2146492485
 * 公司网址:www.prechin.cn
 * 购买地址:
 *
 ****************************************************************************************************
 * 实验现象：倾斜传感器模块，检测到有倾斜时，指示灯亮，否则灭。
 *
 ****************************************************************************************************
 */
#include <stdio.h>
#include <unistd.h>

#include "ohos_init.h"
#include "cmsis_os2.h"

#include "bsp_led.h"
#include "bsp_dht11.h"
#include "bsp_adc_6.c"
#include "bsp_adc_0.c"

//管脚定义
#define MODULE_PIN1         HI_IO_NAME_GPIO_11
#define MODULE_GPIO_FUN1    HI_IO_FUNC_GPIO_11_GPIO
//管脚定义
#define MODULE_PIN2         HI_IO_NAME_GPIO_8
#define MODULE_GPIO_FUN2    HI_IO_FUNC_GPIO_8_GPIO
//管脚定义
#define MODULE_PIN3         HI_IO_NAME_GPIO_14
#define MODULE_GPIO_FUN3    HI_IO_FUNC_GPIO_14_GPIO
//管脚定义
#define MODULE_PIN4         HI_IO_NAME_GPIO_0
#define MODULE_GPIO_FUN4    HI_IO_FUNC_GPIO_0_GPIO
osThreadId_t sound_Task_ID; //任务ID


//传感器模块初始化，声音
void pz_sound_init(void)
{
    hi_gpio_init();                                            // GPIO初始化
    hi_io_set_pull(MODULE_PIN1, HI_IO_PULL_NONE);                   // 设置GPIO上拉
    hi_io_set_func(MODULE_PIN1, MODULE_GPIO_FUN1);                   // 设置IO为GPIO功能
    hi_gpio_set_dir(MODULE_PIN1, HI_GPIO_DIR_IN);                // 设置GPIO为输入模式
}
//传感器模块初始化，倾斜
void pz_tilt_init(void)
{
    hi_io_set_pull(MODULE_PIN2, HI_IO_PULL_NONE);                   // 设置GPIO上拉
    hi_io_set_func(MODULE_PIN2, MODULE_GPIO_FUN2);                   // 设置IO为GPIO功能
    hi_gpio_set_dir(MODULE_PIN2, HI_GPIO_DIR_IN);                // 设置GPIO为输入模式
}
//传感器模块初始化，振动
void pz_vibrate_init(void)
{
    hi_io_set_pull(MODULE_PIN3, HI_IO_PULL_NONE);                   // 设置GPIO上拉
    hi_io_set_func(MODULE_PIN3, MODULE_GPIO_FUN3);                   // 设置IO为GPIO功能
    hi_gpio_set_dir(MODULE_PIN3, HI_GPIO_DIR_IN);                // 设置GPIO为输入模式
}
//传感器模块初始化，火焰
void pz_fire_init(void)
{
    hi_io_set_pull(MODULE_PIN4, HI_IO_PULL_NONE);                   // 设置GPIO上拉
    hi_io_set_func(MODULE_PIN4, MODULE_GPIO_FUN4);                   // 设置IO为GPIO功能
    hi_gpio_set_dir(MODULE_PIN4, HI_GPIO_DIR_IN);                // 设置GPIO为输入模式
}

// 返回temp温度
uint8_t re_temp(void)
{
    uint8_t temp;  	    
	uint8_t humi;
    dht11_read_data(&temp,&humi);
    return temp;
}

// 返回humi湿度
uint8_t re_humi(void)
{
    uint8_t temp;  	    
	uint8_t humi;
    dht11_read_data(&temp,&humi);
    return humi;
}

// 返回声音是否超出强度
hi_u32 re_sound(void)
{
    hi_u32 key_1=0;
    pz_sound_init();
    hi_gpio_get_input_val(MODULE_PIN1,&key_1);
    return key_1;
}

// 返回倾斜角度是否超出
hi_u32 re_tilt(void)
{
    pz_tilt_init();
    hi_u32 key_2=0;
    hi_gpio_get_input_val(MODULE_PIN2,&key_2);
    return key_2;
}

// 返回振动强度是否超出
hi_u32 re_vibrate(void)
{
    hi_u32 key_3=0;
    pz_vibrate_init();//传感器模块初始化
    hi_gpio_get_input_val(MODULE_PIN3,&key_3);
    return key_3;
}

// 返回是否监测到火焰
hi_u32 re_fire(void)
{
    hi_u32 key_4=0;
    pz_fire_init();//传感器模块初始化
    hi_gpio_get_input_val(MODULE_PIN4,&key_4);
    return key_4;
}

// 返回监测到的烟雾值大小
hi_u32 re_somke(void)
{
    hi_u32 key_5=0;
    adc6_init();
    key_5=get_adc6_value();
    return key_5;
}

// 返回光敏的大小
hi_u32 re_light(void)
{
    hi_u32 key_6=0;
    adc0_init();
    key_6=get_adc0_value();
    return key_6;
}

void sound_Task(void)
{
    uint8_t temp;  	    
	uint8_t humi;
    uint8_t value=0;
    uint8_t key_1=0;
    uint8_t key_2=0;
    uint8_t key_3=0;
    uint8_t key_4=0;

    led_init();//LED初始化
    pz_sound_init();//传感器模块初始化
    pz_tilt_init();//传感器模块初始化
    pz_vibrate_init();//传感器模块初始化
    pz_fire_init();

    hi_gpio_get_input_val(MODULE_PIN1,&key_1);
    hi_gpio_get_input_val(MODULE_PIN2,&key_2);
    hi_gpio_get_input_val(MODULE_PIN3,&key_3);
    hi_gpio_get_input_val(MODULE_PIN4,&key_4);
    dht11_read_data(&temp,&humi);
    printf("温度=%d°C  湿度=%d%%RH\r\n",temp,humi);
    printf("sound = %d, tilt = %d, vibrate=%d, fire=%d \n", key_1, key_2, key_3, key_4);
    sleep(1);
    return key_1, key_2, key_3, key_4;
}



