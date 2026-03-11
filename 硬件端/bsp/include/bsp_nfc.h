/**
 ****************************************************************************************************
 * @file        bsp_nfc.h
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

#ifndef BSP_NFC_H
#define BSP_NFC_H

#include "cmsis_os2.h"
#include "hi_io.h"
#include "hi_gpio.h"



#define NDEF_HEADER_SIZE 0x2 // NDEF协议的头部大小

#define NDEF_PROTOCOL_HEADER_OFFSET 0           // NDEF协议头(固定)
#define NDEF_PROTOCOL_LENGTH_OFFSET 1           // NDEF协议数据的总长度位
#define NDEF_PROTOCOL_MEG_CONFIG_OFFSET 2       // 标签的控制字节位
#define NDEF_PROTOCOL_DATA_TYPE_LENGTH_OFFSET 3 // 标签数据类型的长度位
#define NDEF_PROTOCOL_DATA_LENGTH_OFFSET 4      // 标签的数据长度位
#define NDEF_PROTOCOL_DATA_TYPE_OFFSET 6        // 标签的数据类型位
#define NDEF_PROTOCOL_VALID_DATA_OFFSET 20      // 有效数据位


//函数声明
uint32_t get_NDEFDataPackage(uint8_t *dataBuff, const uint16_t dataBuff_MaxSize);
uint32_t nfc_init(void);

#endif
