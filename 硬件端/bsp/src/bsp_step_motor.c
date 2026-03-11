/**
 ****************************************************************************************************
 * @file        bsp_step_motor.c
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

#include "bsp_step_motor.h"


//步进电机初始化
void step_motor_init(void)
{
    hi_gpio_init();                                     // GPIO初始化
    hi_io_set_pull(IN1_PIN, HI_IO_PULL_UP);             // 设置GPIO上拉
    hi_io_set_func(IN1_PIN, IN1_GPIO_FUN);              // 设置IO为GPIO功能
    hi_gpio_set_dir(IN1_PIN, HI_GPIO_DIR_OUT);          // 设置GPIO为输出模式

    hi_io_set_pull(IN2_PIN, HI_IO_PULL_UP);             // 设置GPIO上拉
    hi_io_set_func(IN2_PIN, IN2_GPIO_FUN);              // 设置IO为GPIO功能
    hi_gpio_set_dir(IN2_PIN, HI_GPIO_DIR_OUT);          // 设置GPIO为输出模式

    hi_io_set_pull(IN3_PIN, HI_IO_PULL_UP);             // 设置GPIO上拉
    hi_io_set_func(IN3_PIN, IN3_GPIO_FUN);              // 设置IO为GPIO功能
    hi_gpio_set_dir(IN3_PIN, HI_GPIO_DIR_OUT);          // 设置GPIO为输出模式

    hi_io_set_pull(IN4_PIN, HI_IO_PULL_UP);             // 设置GPIO上拉
    hi_io_set_func(IN4_PIN, IN4_GPIO_FUN);              // 设置IO为GPIO功能
    hi_gpio_set_dir(IN4_PIN, HI_GPIO_DIR_OUT);          // 设置GPIO为输出模式
}

/*******************************************************************************
* 函 数 名       : step_motor_run
* 函数功能		 : 输出一个数据给ULN2003从而实现向步进电机发送一个脉冲
	    		   步进角为5.625/64度，如果需要转动一圈，那么需要360/5.625*64=4096个脉冲信号，
				   假如需要转动90度，需要的脉冲数=90*4096/360=1024脉冲信号。
				   如果任意角度对应多少脉冲呢？脉冲=angle*64/(8*5.625)
				   正好对应下面计算公式
				   (64*angle/45)*8，这个angle就是转动90度，45表示5.625*8，8代表8个脉冲，for循环。
* 输    入       : step：指定步进控制节拍，可选值4或8
				   dir：方向选择,1：顺时针,0：逆时针
				   speed：速度1-5
				   angle：角度选择0-360
				   sta：电机运行状态，1启动，0停止
* 输    出    	 : 无
*******************************************************************************/
void step_motor_run(uint8_t step,uint8_t dir,uint8_t speed,uint16_t angle,uint8_t sta)
{
	char i=0;
	uint16_t j=0;

	if(sta==1)
	{
		if(dir==0)	//如果为逆时针旋转
		{
			for(j=0;j<64*angle/45;j++) 
			{
				for(i=0;i<8;i+=(8/step))
				{
					switch(i)//8个节拍控制：A->AB->B->BC->C->CD->D->DA
					{
						case 0: MOTOR_IN1(1);MOTOR_IN2(0);MOTOR_IN3(0);MOTOR_IN4(0);break;
						case 1: MOTOR_IN1(1);MOTOR_IN2(1);MOTOR_IN3(0);MOTOR_IN4(0);break;
						case 2: MOTOR_IN1(0);MOTOR_IN2(1);MOTOR_IN3(0);MOTOR_IN4(0);break;
						case 3: MOTOR_IN1(0);MOTOR_IN2(1);MOTOR_IN3(1);MOTOR_IN4(0);break;
						case 4: MOTOR_IN1(0);MOTOR_IN2(0);MOTOR_IN3(1);MOTOR_IN4(0);break;
						case 5: MOTOR_IN1(0);MOTOR_IN2(0);MOTOR_IN3(1);MOTOR_IN4(1);break;
						case 6: MOTOR_IN1(0);MOTOR_IN2(0);MOTOR_IN3(0);MOTOR_IN4(1);break;
						case 7: MOTOR_IN1(1);MOTOR_IN2(0);MOTOR_IN3(0);MOTOR_IN4(1);break;	
					}
					usleep(speed*1000);		
				}	
			}
		}
		else	//如果为顺时针旋转
		{
			for(j=0;j<64*angle/45;j++)
			{
				for(i=0;i<8;i+=(8/step))
				{
					switch(i)//8个节拍控制：A->AB->B->BC->C->CD->D->DA
					{
						case 0: MOTOR_IN1(1);MOTOR_IN2(0);MOTOR_IN3(0);MOTOR_IN4(1);break;
						case 1: MOTOR_IN1(0);MOTOR_IN2(0);MOTOR_IN3(0);MOTOR_IN4(1);break;
						case 2: MOTOR_IN1(0);MOTOR_IN2(0);MOTOR_IN3(1);MOTOR_IN4(1);break;
						case 3: MOTOR_IN1(0);MOTOR_IN2(0);MOTOR_IN3(1);MOTOR_IN4(0);break;
						case 4: MOTOR_IN1(0);MOTOR_IN2(1);MOTOR_IN3(1);MOTOR_IN4(0);break;
						case 5: MOTOR_IN1(0);MOTOR_IN2(1);MOTOR_IN3(0);MOTOR_IN4(0);break;
						case 6: MOTOR_IN1(1);MOTOR_IN2(1);MOTOR_IN3(0);MOTOR_IN4(0);break;
						case 7: MOTOR_IN1(1);MOTOR_IN2(0);MOTOR_IN3(0);MOTOR_IN4(0);break;	
					}
					usleep(speed*1000);		
				}	
			}	
		}		
	}
	else
	{
		MOTOR_IN1(0);MOTOR_IN2(0);MOTOR_IN3(0);MOTOR_IN4(0);	
	}		
}
