/**
 ****************************************************************************************************
 * @file        bsp_dht11.c
 * @author      普中科技
 * @version     V1.0
 * @date        2024-06-05
 * @brief       DHT11温湿度传感器实验
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

#include "bsp_dht11.h"
#include <unistd.h>
#include "hi_time.h"


//DHT11输出配置
void dht11_io_out(void)
{
    hi_gpio_init();                                        // GPIO初始化
    hi_io_set_pull(DHT11_PIN, HI_IO_PULL_UP);              // 设置GPIO上拉
    hi_io_set_func(DHT11_PIN, DHT11_GPIO_FUN);             // 设置IO为GPIO功能
    hi_gpio_set_dir(DHT11_PIN, HI_GPIO_DIR_OUT);           // 设置GPIO为输出模式
}

//DHT11输入配置
void dht11_io_in(void)
{
    hi_io_set_pull(DHT11_PIN, HI_IO_PULL_NONE);             // 设置GPIO浮空
    hi_gpio_set_dir(DHT11_PIN, HI_GPIO_DIR_IN);             // 设置GPIO为输入模式
}

/******************************************************
 * 函数名   ：GPIO_GetInputValue
 * 功能     ：获取GPIO输入状态
 * 输入     ：id, *val
 * 输出     ：0/1
 *******************************************************/
hi_gpio_value DHT11_DQ_IN = {0};
uint8_t GPIO_GetInputValue(hi_gpio_idx id,hi_gpio_value *val)
{
    hi_gpio_get_input_val(id,val);
    return *val;
}

//dht11复位
void dht11_reset(void)	   
{                 
	hi_gpio_set_dir(DHT11_PIN, HI_GPIO_DIR_OUT);             // 设置GPIO为输出模式
	DHT11_DQ_OUT(0); //拉低DQ
	hi_udelay(20*1000);    //拉低至少18ms
	DHT11_DQ_OUT(1); //DQ=1 
	hi_udelay(30);     //30US
}

//等待DHT11的回应
//返回1:未检测到DHT11的存在
//返回0:存在
uint8_t dht11_check(void) 	   
{   
	uint8_t retry=0;
	dht11_io_in(); 
    while (GPIO_GetInputValue(DHT11_PIN,&DHT11_DQ_IN)&&retry<100)//DHT11会拉低40~50us
	{
		retry++;
		hi_udelay(1);
	};	 
	if(retry>=100)return 1;
	else retry=0;
    while ((!GPIO_GetInputValue(DHT11_PIN,&DHT11_DQ_IN))&&retry<100)//DHT11拉低后会再次拉高40~50us
	{
		retry++;
		hi_udelay(1);
	};
	if(retry>=100)return 1;	    
	return 0;
}

//从DHT11读取一个位
//返回值：1/0
uint8_t dht11_read_bit(void) 			 
{
 	uint8_t retry=0;
    dht11_io_in();
	while(GPIO_GetInputValue(DHT11_PIN,&DHT11_DQ_IN)&&retry<100)//等待变为低电平 12-14us 开始
	{
		retry++;
		hi_udelay(1);
	}
	retry=0;
	while((!GPIO_GetInputValue(DHT11_PIN,&DHT11_DQ_IN))&&retry<100)//等待变高电平	 26-28us表示0,116-118us表示1
	{
		retry++;
		hi_udelay(1);
	}
	hi_udelay(40);//等待40us
	if(GPIO_GetInputValue(DHT11_PIN,&DHT11_DQ_IN))return 1;
	else return 0;		   
}

//从DHT11读取一个字节
//返回值：读到的数据
uint8_t dht11_read_byte(void)    
{        
    uint8_t i,dat;
    dat=0;
	for (i=0;i<8;i++) 
	{
   		dat<<=1; 
	    dat|=dht11_read_bit();
    }						    
    return dat;
}

//从DHT11读取一次数据
//temp:温度值(范围:0~50°)
//humi:湿度值(范围:20%~90%)
//返回值：0,正常;1,读取失败
uint8_t dht11_read_data(uint8_t *temp,uint8_t *humi)    
{        
 	uint8_t buf[5];
	uint8_t i;
	dht11_reset();
	if(dht11_check()==0)
	{
		for(i=0;i<5;i++)//读取40位数据
		{
			buf[i]=dht11_read_byte();
		}
		if((buf[0]+buf[1]+buf[2]+buf[3])==buf[4])
		{
			*humi=buf[0];
			*temp=buf[2];
		}
		
	}else return 1;
	return 0;	    
}

//DHT11初始化 
//返回0：初始化成功，1：失败
uint8_t dht11_init(void)
{
    hi_gpio_init();                                            // GPIO初始化
    hi_io_set_pull(DHT11_PIN, HI_IO_PULL_UP);                // 设置GPIO上拉
    hi_io_set_func(DHT11_PIN, DHT11_GPIO_FUN);             // 设置IO为GPIO功能
    hi_gpio_set_dir(DHT11_PIN, HI_GPIO_DIR_OUT);             // 设置GPIO为输出模式

    dht11_reset();
	return dht11_check();
}
