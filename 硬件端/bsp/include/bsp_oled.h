/**
 ****************************************************************************************************
 * @file        bsp_oled.h
 * @author      普中科技
 * @version     V1.0
 * @date        2024-06-05
 * @brief       OLED液晶显示实验
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

#ifndef BSP_OLED_H
#define BSP_OLED_H

#include "cmsis_os2.h"
#include "hi_io.h"
#include "hi_gpio.h"


#define SSD1306_I2C_ADDR        0x78         // 器件的I2C从机地址
#define SSD1306_I2C_IDX         0             // 模块的I2C总线号
#define SSD1306_I2C_SPEED       100000       // 100KHz


#define SIZE 16
#define XLevelL		0x00
#define XLevelH		0x10
#define Max_Column	128
#define Max_Row		64
#define	Brightness	0xFF 
#define X_WIDTH 	128
#define Y_WIDTH 	64

#define OLED_CMD  0	//写命令
#define OLED_DATA 1	//写数据

//函数声明
void oled_wr_byte(uint8_t dat,uint8_t cmd);	    
void oled_display_on(void);
void oled_display_off(void);
void oled_set_pos(unsigned char x, unsigned char y);	   							   		    
void oled_init(void);
void oled_refresh_gram(void);
void oled_clear(void);
void oled_drawpoint(uint8_t x,uint8_t y,uint8_t t);
void oled_fill(uint8_t x1,uint8_t y1,uint8_t x2,uint8_t y2,uint8_t dot);
void oled_fill_rectangle(uint8_t x0,uint8_t y0,uint8_t width,uint8_t height,uint8_t color);
void oled_drawline(uint8_t x1, uint8_t y1, uint8_t x2, uint8_t y2,uint8_t color);
void oled_drawRectangle(uint8_t x1, uint8_t y1, uint8_t x2, uint8_t y2,uint8_t color);
void oled_fill_circle(uint8_t x0,uint8_t y0,uint8_t r,uint8_t color);
void oled_draw_bigpoint(uint8_t x0,uint8_t y0,uint8_t color);
void oled_draw_vline(uint8_t x0,uint8_t y0,uint8_t len,uint8_t color);
void oled_draw_hline(uint8_t x0,uint8_t y0,uint8_t len,uint8_t color);
void oled_fill_circle(uint8_t x0,uint8_t y0,uint8_t r,uint8_t color);
void oled_draw_ellipse(uint8_t x0, uint8_t y0, uint8_t rx, uint8_t ry,uint8_t color) ;
void oled_showchar(uint8_t x,uint8_t y,uint8_t chr,uint8_t size,uint8_t mode);
void oled_shownum(uint8_t x,uint8_t y,uint32_t num,uint8_t len,uint8_t size);
void oled_showstring(uint8_t x,uint8_t y,const uint8_t *p,uint8_t size); 
void oled_showfontHZ(uint8_t x,uint8_t y,uint8_t pos,uint8_t size,uint8_t mode);
void oled_drawBMP(uint8_t x0, uint8_t y0,uint8_t x1, uint8_t y1,uint8_t BMP[]);

#endif
