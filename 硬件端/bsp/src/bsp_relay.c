/**
 ****************************************************************************************************
 * @file        bsp_relay.c
 * @author      普中科技
 * @version     V1.0
 * @date        2024-06-05
 * @brief       继电器实验
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

#include "bsp_relay.h"


//继电器初始化
void relay_init(void)
{
    hi_gpio_init();                                            // GPIO初始化
    hi_io_set_pull(RELAY_PIN, HI_IO_PULL_DOWN);                   // 设置GPIO下拉
    hi_io_set_func(RELAY_PIN, RELAY_GPIO_FUN);                   // 设置IO为GPIO功能
    hi_gpio_set_dir(RELAY_PIN, HI_GPIO_DIR_OUT);                // 设置GPIO为输出模式
}

