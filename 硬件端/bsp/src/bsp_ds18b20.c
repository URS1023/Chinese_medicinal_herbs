/**
 ****************************************************************************************************
 * @file        bsp_ds18b20.c
 * @author      普中科技
 * @version     V1.0
 * @date        2024-06-05
 * @brief       DS18B20温度传感器实验
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

#include "bsp_ds18b20.h"
#include <unistd.h>
#include "hi_time.h"


//DS18B20输出配置
void ds18b20_io_out(void)
{
    hi_gpio_init();                                            // GPIO初始化
    hi_io_set_pull(DS18B20_PIN, HI_IO_PULL_UP);                // 设置GPIO上拉
    hi_io_set_func(DS18B20_PIN, DS18B20_GPIO_FUN);             // 设置IO为GPIO功能
    hi_gpio_set_dir(DS18B20_PIN, HI_GPIO_DIR_OUT);             // 设置GPIO为输出模式
}

//DS18B20输入配置
void ds18b20_io_in(void)
{
    hi_io_set_pull(DS18B20_PIN, HI_IO_PULL_NONE);                // 设置GPIO浮空
    hi_gpio_set_dir(DS18B20_PIN, HI_GPIO_DIR_IN);             // 设置GPIO为输入模式
}

/******************************************************
 * 函数名   ：GPIO_GetInputValue
 * 功能     ：获取GPIO输入状态
 * 输入     ：id, *val
 * 输出     ：0/1
 *******************************************************/
hi_gpio_value DS18B20_DQ_IN = {0};
uint8_t GPIO_GetInputValue(hi_gpio_idx id,hi_gpio_value *val)
{
    hi_gpio_get_input_val(id,val);
    return *val;
}

//ds18b20复位
void ds18b20_reset(void)	   
{                 
	hi_gpio_set_dir(DS18B20_PIN, HI_GPIO_DIR_OUT);             // 设置GPIO为输出模式
	DS18B20_DQ_OUT(0); //拉低DQ
	hi_udelay(750);    //拉低750us
	DS18B20_DQ_OUT(1); //DQ=1 
	hi_udelay(15);     //15US
}

/*******************************************************************************
* 函 数 名         : ds18b20_check
* 函数功能		   : 检测DS18B20是否存在
* 输    入         : 无
* 输    出         : 1:未检测到DS18B20的存在，0:存在
*******************************************************************************/
uint8_t ds18b20_check(void) 	   
{   
	uint8_t retry=0;
	ds18b20_io_in(); 
    while (GPIO_GetInputValue(DS18B20_PIN,&DS18B20_DQ_IN)&&retry<200)
	{
		retry++;
		hi_udelay(1);
	};
	if(retry>=200)return 1;
	else retry=0;
    while ((!GPIO_GetInputValue(DS18B20_PIN,&DS18B20_DQ_IN))&&retry<240)
	{
		retry++;
		hi_udelay(1);
	};
	if(retry>=240)return 1;	    
	return 0;
}

/*******************************************************************************
* 函 数 名         : ds18b20_read_bit
* 函数功能		   : 从DS18B20读取一个位
* 输    入         : 无
* 输    出         : 1/0
*******************************************************************************/
uint8_t ds18b20_read_bit(void) 			 // read one bit
{
	uint8_t data;

	hi_gpio_set_dir(DS18B20_PIN, HI_GPIO_DIR_OUT);
	DS18B20_DQ_OUT(0); 
	hi_udelay(2);
	DS18B20_DQ_OUT(1); 
	ds18b20_io_in();
	hi_udelay(12);
	if(GPIO_GetInputValue(DS18B20_PIN,&DS18B20_DQ_IN))data=1;
	else data=0;	 
	hi_udelay(50);           
	return data;
}

/*******************************************************************************
* 函 数 名         : ds18b20_read_byte
* 函数功能		   : 从DS18B20读取一个字节
* 输    入         : 无
* 输    出         : 一个字节数据
*******************************************************************************/
uint8_t ds18b20_read_byte(void)    // read one byte
{        
    uint8_t i,j,dat;
    dat=0;
	for (i=0;i<8;i++) 
	{
		j=ds18b20_read_bit();
        dat=(j<<7)|(dat>>1);
    }						    
    return dat;
}

/*******************************************************************************
* 函 数 名         : ds18b20_write_byte
* 函数功能		   : 写一个字节到DS18B20
* 输    入         : dat：要写入的字节
* 输    出         : 无
*******************************************************************************/
void ds18b20_write_byte(uint8_t dat)     
{             
	uint8_t j;
    uint8_t testb;
	hi_gpio_set_dir(DS18B20_PIN, HI_GPIO_DIR_OUT);
    for (j=1;j<=8;j++) 
	{
        testb=dat&0x01;
        dat=dat>>1;
        if (testb) 
        {
            DS18B20_DQ_OUT(0);// Write 1
            hi_udelay(2);                            
            DS18B20_DQ_OUT(1);
            hi_udelay(60);             
        }
        else 
        {
            DS18B20_DQ_OUT(0);// Write 0
            hi_udelay(60);             
            DS18B20_DQ_OUT(1);
            hi_udelay(2);                          
        }
    }
}

/*******************************************************************************
* 函 数 名         : ds18b20_start
* 函数功能		   : 开始温度转换
* 输    入         : 无
* 输    出         : 无
*******************************************************************************/
void ds18b20_start(void)// ds1820 start convert
{   						               
    ds18b20_reset();	   
	ds18b20_check();	 
    ds18b20_write_byte(0xcc);// skip rom
    ds18b20_write_byte(0x44);// convert
} 

//DS18B20初始化
uint8_t ds18b20_init(void)
{
    hi_gpio_init();                                            // GPIO初始化
    hi_io_set_pull(DS18B20_PIN, HI_IO_PULL_UP);                // 设置GPIO上拉
    hi_io_set_func(DS18B20_PIN, DS18B20_GPIO_FUN);             // 设置IO为GPIO功能
    hi_gpio_set_dir(DS18B20_PIN, HI_GPIO_DIR_OUT);             // 设置GPIO为输出模式

    ds18b20_reset();
	return ds18b20_check();
}

/*******************************************************************************
* 函 数 名         : ds18b20_gettemperture
* 函数功能		   : 从ds18b20得到温度值
* 输    入         : 无
* 输    出         : 温度数据
*******************************************************************************/ 
float ds18b20_gettemperture(void)
{
    uint16_t temp;
	uint8_t a,b;
	float value;
    ds18b20_start();                    // ds1820 start convert
    ds18b20_reset();
    ds18b20_check();	 
    ds18b20_write_byte(0xcc);// skip rom
    ds18b20_write_byte(0xbe);// convert	    
    a=ds18b20_read_byte(); // LSB   
    b=ds18b20_read_byte(); // MSB   
	temp=b;
	temp=(temp<<8)+a;
    if((temp&0xf800)==0xf800)
	{
		temp=(~temp)+1;
		value=temp*(-0.0625);
	}
	else
	{
		value=temp*0.0625;	
	}
	return value;    
}
