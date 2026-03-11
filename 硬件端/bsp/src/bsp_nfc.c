/**
 ****************************************************************************************************
 * @file        bsp_nfc.c
 * @author      普中科技
 * @version     V1.0
 * @date        2024-06-05
 * @brief       NFC实验
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

#include "bsp_nfc.h"
#include "hi_errno.h"
#include "hi_i2c.h"
#include "NT3H.h"
#include <stdlib.h>
#include <string.h>


/**
 * @brief  从Page页中组成NDEF协议的包裹
 * @note
 * @param  *dataBuff: 最终的内容
 * @param  dataBuff_MaxSize: 存储缓冲区的长度
 * @retval
 */
uint32_t get_NDEFDataPackage(uint8_t *dataBuff, const uint16_t dataBuff_MaxSize)
{
    if (dataBuff == NULL || dataBuff_MaxSize <= 0) 
    {
        printf("dataBuff==NULL or dataBuff_MaxSize<=0\r\n");
        return HI_ERR_FAILURE;
    }

    uint8_t userMemoryPageNum = 0; // 用户的数据操作页数

    // 算出要取多少页
    if (dataBuff_MaxSize <= NFC_PAGE_SIZE) 
    {
        userMemoryPageNum = 1; // 1页
    } 
    else 
    {
        // 需要访问多少页
        userMemoryPageNum = (dataBuff_MaxSize / NFC_PAGE_SIZE) + \
                            ((dataBuff_MaxSize % NFC_PAGE_SIZE) >= 0 ? 1 : 0);
    }

    // 内存拷贝
    uint8_t *p_buff = (uint8_t *)malloc(userMemoryPageNum * NFC_PAGE_SIZE);
    if (p_buff == NULL) 
    {
        printf("p_buff == NULL.\r\n");
        return HI_ERR_FAILURE;
    }

    // 读取数据
    for (int i = 0; i < userMemoryPageNum; i++) 
    {
        if (NT3HReadUserData(i) == true) 
        {
            memcpy_s(p_buff + i * NFC_PAGE_SIZE, userMemoryPageNum * NFC_PAGE_SIZE,
                     nfcPageBuffer, NFC_PAGE_SIZE);
        }
    }

    memcpy_s(dataBuff, dataBuff_MaxSize, p_buff, dataBuff_MaxSize);

    free(p_buff);
    p_buff = NULL;

    return HI_ERR_SUCCESS;
}

//NFC初始化
uint32_t nfc_init(void)
{
    uint32_t result;

    // gpio_9 复用为 I2C_SCL
    hi_io_set_pull(HI_IO_NAME_GPIO_9, HI_IO_PULL_UP);
    hi_io_set_func(HI_IO_NAME_GPIO_9, HI_IO_FUNC_GPIO_9_I2C0_SCL);
    // gpio_10 复用为 I2C_SDA
    hi_io_set_pull(HI_IO_NAME_GPIO_10, HI_IO_PULL_UP);
    hi_io_set_func(HI_IO_NAME_GPIO_10, HI_IO_FUNC_GPIO_10_I2C0_SDA);

    result = hi_i2c_init(HI_I2C_IDX_0, I2C_RATE_DEFAULT);
    if (result != HI_ERR_SUCCESS) 
    {
        printf("I2C nfc Init status is 0x%x!!!\r\n", result);
        return result;
    }
    printf("I2C nfc Init is succeeded!!!\r\n");

    return true;
}
