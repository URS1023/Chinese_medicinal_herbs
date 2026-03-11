/**
 ****************************************************************************************************
 * @file        bsp_sr04.c
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

#include "bsp_sr04.h"
#include <unistd.h>
#include "hi_time.h"


//超声波初始化
void sr04_init(void)
{
	hi_gpio_init();                                            // GPIO初始化
    // hi_io_set_pull(TRIG_PIN, HI_IO_PULL_UP);                  // 设置GPIO下拉
    hi_io_set_func(TRIG_PIN, TRIG_GPIO_FUN);                      // 设置IO为GPIO功能
    hi_gpio_set_dir(TRIG_PIN, HI_GPIO_DIR_OUT);                 // 设置GPIO为输出模式

	// hi_io_set_pull(ECHO_PIN, HI_IO_PULL_DOWN);             // 设置GPIO下拉
	hi_io_set_func(ECHO_PIN, ECHO_GPIO_FUN);                      // 设置IO为GPIO功能
    hi_gpio_set_dir(ECHO_PIN, HI_GPIO_DIR_IN);             // 设置GPIO为输入模式
}

/******************************************************
 * 函数名   ：GPIO_GetInputValue
 * 功能     ：获取GPIO输入状态
 * 输入     ：id, *val
 * 输出     ：0/1
 *******************************************************/
hi_gpio_value ECHO = {0};
uint8_t GPIO_GetInputValue(hi_gpio_idx id,hi_gpio_value *val)
{
    hi_gpio_get_input_val(id,val);
    return *val;
}

//读取超声波测量距离
//返回值：测量距离cm
float sr04_read_distance(void)
{
	static unsigned long start_time = 0, time = 0;
	float distance = 0.0;
	unsigned int flag = 0;

	TRIG(1);	//拉高
	hi_udelay(20);
	TRIG(0);	//拉低
	
	while(1)
	{
		//判断高电平
		if(GPIO_GetInputValue(ECHO_PIN,&ECHO)==1 && flag==0)
		{
			start_time = hi_get_us();//获取系统时间
            flag = 1;
		}
		//判断低电平
		if(GPIO_GetInputValue(ECHO_PIN,&ECHO)==0 && flag==1)
		{
			time = hi_get_us() - start_time;//获取高电平持续时间
            break;
		}
	}
	//计算距离障碍物距离（340米/秒 转换为 0.034厘米/微秒, 2代表去来，两倍距离）
	distance = time * 0.034 / 2;

	return distance;
}
