/**
 ****************************************************************************************************
 * @file        bsp_uart.c
 * @author      普中科技
 * @version     V1.0
 * @date        2024-06-05
 * @brief       串口通信实验
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

#include "bsp_uart.h"
#include "hi_uart.h"


//串口初始化
void uart0_init(uint32_t buad)
{
    hi_uart_attribute uart_attr;
    
    hi_gpio_init();                                            // GPIO初始化
    hi_io_set_pull(UART0_TX_PIN, HI_IO_PULL_UP);                // 设置GPIO上拉
    hi_io_set_func(UART0_TX_PIN, UART0_TX_GPIO_FUN);            // 设置IO为串口功能
    hi_gpio_set_dir(UART0_TX_PIN, HI_GPIO_DIR_OUT);             // 设置GPIO为输出模式

    hi_io_set_pull(UART0_RX_PIN, HI_IO_PULL_NONE);                // 设置GPIO浮空
    hi_io_set_func(UART0_RX_PIN, UART0_RX_GPIO_FUN);            // 设置IO为串口功能
    hi_gpio_set_dir(UART0_RX_PIN, HI_GPIO_DIR_IN);             // 设置GPIO为输入模式

    uart_attr.baud_rate=buad;
    uart_attr.data_bits=HI_UART_DATA_BIT_8;
    uart_attr.stop_bits=HI_UART_STOP_BIT_1;
    uart_attr.parity=HI_UART_PARITY_NONE;
    hi_uart_init(HI_UART_IDX_0,&uart_attr,NULL);
}

//串口发送数据
void uart0_send_data(uint8_t *dat,uint8_t len)
{
    hi_uart_write(HI_UART_IDX_0,dat,len);
}

//串口读取数据
uint32_t uart0_read_data(uint8_t *dat,uint8_t len)
{
    return hi_uart_read(HI_UART_IDX_0,dat,len);
}
