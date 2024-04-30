
 /* 
 ____  __    __   _  _  ___  _  _  _  _ 
(_  _)(  )  (  ) ( \/ )/ __)( )/ )( \/ )
 _)(_  )(__  )(__ \  / \__ \ )  (  \  / 
(____)(____)(____)(__) (___/(_)\_) (__) 

 Driver header file for TI BQ25792
 v1.0.0
 Copyright (c) 2023 Illysky Ltd
 */  

#ifndef __TI_BQ25792_H
#define __TI_BQ25792_H

#ifdef __cplusplus
extern "C" {
#endif

#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <stdlib.h>
#include <zephyr/device.h>
#include <zephyr/devicetree.h>
#include <zephyr/kernel.h>


#define  BQ25792_MINIMAL_SYSTEM_VOLTAGE_ADDR 0x00
#define  BQ25792_MINIMAL_SYSTEM_VOLTAGE_SIZE 1
typedef union
{
    uint8_t v;
    struct
    {
		unsigned : 2;
		unsigned VSYSMIN: 6;
    }; 
} __attribute__((packed))  bq25792_minimal_system_voltage_t;


#define  BQ25792_CHARGE_VOLTAGE_LIMIT_ADDR 0x00
#define  BQ25792_CHARGE_VOLTAGE_LIMIT_SIZE 2
typedef union
{
    uint16_t v;
    struct
    {
		unsigned : 5;
		unsigned VREG: 11;
    }; 
} __attribute__((packed))  bq25792_charge_voltage_limit_t;


#define  BQ25792_CHARGE_CURRENT_LIMIT_ADDR 0x00
#define  BQ25792_CHARGE_CURRENT_LIMIT_SIZE 2
typedef union
{
    uint16_t v;
    struct
    {
		unsigned : 7;
		unsigned ICHG: 9;
    }; 
} __attribute__((packed))  bq25792_charge_current_limit_t;


#define  BQ25792_INPUT_VOLTAGE_LIMIT_ADDR 0x05
#define  BQ25792_INPUT_VOLTAGE_LIMIT_SIZE 1
typedef union
{
    uint8_t v;
    struct
    {
		unsigned VINDPM: 8;
    }; 
} __attribute__((packed))  bq25792_input_voltage_limit_t;


#define  BQ25792_INPUT_CURRENT_LIMIT_ADDR 0x06
#define  BQ25792_INPUT_CURRENT_LIMIT_SIZE 2
typedef union
{
    uint16_t v;
    struct
    {
		unsigned : 7;
		unsigned IINDPM: 9;
    }; 
} __attribute__((packed))  bq25792_input_current_limit_t;


#define  BQ25792_PRECHARGE_CONTROL_ADDR 0x08
#define  BQ25792_PRECHARGE_CONTROL_SIZE 1
typedef union
{
    uint8_t v;
    struct
    {
		unsigned VBAT_LOWV: 2;
		unsigned IPRECHG: 6;
    }; 
} __attribute__((packed))  bq25792_precharge_control_t;


#define  BQ25792_TERMINATION_CONTROL_ADDR 0x09
#define  BQ25792_TERMINATION_CONTROL_SIZE 1
typedef union
{
    uint8_t v;
    struct
    {
		unsigned : 1;
		unsigned REG_RST: 1;
		unsigned : 1;
		unsigned ITERM: 5;
    }; 
} __attribute__((packed))  bq25792_termination_control_t;


#define  BQ25792_RECHARGE_CONTROL_ADDR 0x0A
#define  BQ25792_RECHARGE_CONTROL_SIZE 1
typedef union
{
    uint8_t v;
    struct
    {
		unsigned CELL: 2;
		unsigned TRECHG: 2;
		unsigned VRECHG: 4;
    }; 
} __attribute__((packed))  bq25792_recharge_control_t;


#define  BQ25792_VOTG_ADDR 0x0B
#define  BQ25792_VOTG_SIZE 2
typedef union
{
    uint16_t v;
    struct
    {
		unsigned : 5;
		unsigned VOTG: 11;
    }; 
} __attribute__((packed))  bq25792_votg_t;


#define  BQ25792_IOTG_REGULATION_ADDR 0x0D
#define  BQ25792_IOTG_REGULATION_SIZE 1
typedef union
{
    uint8_t v;
    struct
    {
		unsigned PRECHG_TMR: 1;
		unsigned IOTG: 7;
    }; 
} __attribute__((packed))  bq25792_iotg_regulation_t;


#define  BQ25792_TIMER_CONTROL_ADDR 0x0E
#define  BQ25792_TIMER_CONTROL_SIZE 1
typedef union
{
    uint8_t v;
    struct
    {
		unsigned TOPOFF_TMR: 2;
		unsigned EN_TRICHG_TMR: 1;
		unsigned EN_PRECHG_TMR: 1;
		unsigned EN_CHG_TMR: 1;
		unsigned CHG_TMR: 2;
		unsigned TMR2X_EN: 1;
    }; 
} __attribute__((packed))  bq25792_timer_control_t;


#define  BQ25792_CHARGER_CONTROL_0_ADDR 0x0F
#define  BQ25792_CHARGER_CONTROL_0_SIZE 1
typedef union
{
    uint8_t v;
    struct
    {
		unsigned EN_AUTO_IBATDIS: 1;
		unsigned FORCE_IBATDIS: 1;
		unsigned EN_CHG: 1;
		unsigned EN_ICO: 1;
		unsigned FORCE_ICO: 1;
		unsigned EN_HIZ: 1;
		unsigned EN_TERM: 1;
		unsigned : 1;
    }; 
} __attribute__((packed))  bq25792_charger_control_0_t;


#define  BQ25792_CHARGER_CONTROL_1_ADDR 0x10
#define  BQ25792_CHARGER_CONTROL_1_SIZE 1
typedef union
{
    uint8_t v;
    struct
    {
		unsigned : 2;
		unsigned VAC_OVP: 2;
		unsigned WD_RST: 1;
		unsigned WATCHDOG: 3;
    }; 
} __attribute__((packed))  bq25792_charger_control_1_t;


#define  BQ25792_CHARGER_CONTROL_2_ADDR 0x11
#define  BQ25792_CHARGER_CONTROL_2_SIZE 1
typedef union
{
    uint8_t v;
    struct
    {
		unsigned FORCE_INDET: 1;
		unsigned AUTO_INDET_EN: 1;
		unsigned EN_12V: 1;
		unsigned EN_9V: 1;
		unsigned HVDCP_EN: 1;
		unsigned SDRV_CTRL: 2;
		unsigned SDRV_DLY: 1;
    }; 
} __attribute__((packed))  bq25792_charger_control_2_t;


#define  BQ25792_CHARGER_CONTROL_3_ADDR 0x12
#define  BQ25792_CHARGER_CONTROL_3_SIZE 1
typedef union
{
    uint8_t v;
    struct
    {
		unsigned DIS_ACDRV: 1;
		unsigned EN_OTG: 1;
		unsigned PFM_OTG_DIS: 1;
		unsigned PFM_FWD_DIS: 1;
		unsigned WKUP_DLY: 1;
		unsigned DIS_LDO: 1;
		unsigned DIS_OTG_OOA: 1;
		unsigned DIS_FWD_OOA: 1;
    }; 
} __attribute__((packed))  bq25792_charger_control_3_t;


#define  BQ25792_CHARGER_CONTROL_4_ADDR 0x13
#define  BQ25792_CHARGER_CONTROL_4_SIZE 1
typedef union
{
    uint8_t v;
    struct
    {
		unsigned EN_ACDRV2: 1;
		unsigned EN_ACDRV1: 1;
		unsigned PWM_FREQ: 1;
		unsigned DIS_STAT: 1;
		unsigned DIS_VSYS_SHORT: 1;
		unsigned DIS_VOTG_UVP: 1;
		unsigned FORCE_VINDPM_DET: 1;
		unsigned EN_IBUS_OCP: 1;
    }; 
} __attribute__((packed))  bq25792_charger_control_4_t;


#define  BQ25792_CHARGER_CONTROL_5_ADDR 0x14
#define  BQ25792_CHARGER_CONTROL_5_SIZE 1
typedef union
{
    uint8_t v;
    struct
    {
		unsigned SFET_PRESENT: 1;
		unsigned : 1;
		unsigned EN_IBAT: 1;
		unsigned IBAT_REG: 2;
		unsigned EN_IINDPM: 1;
		unsigned EN_EXTILIM: 1;
		unsigned EN_BATOC: 1;
    }; 
} __attribute__((packed))  bq25792_charger_control_5_t;


#define  BQ25792_TEMPERATURE_CONTROL_ADDR 0x16
#define  BQ25792_TEMPERATURE_CONTROL_SIZE 1
typedef union
{
    uint8_t v;
    struct
    {
		unsigned TREG: 2;
		unsigned TSHUT: 2;
		unsigned VBUS_PD_EN: 1;
		unsigned VAC1_PD_EN: 1;
		unsigned VAC2_PD_EN: 1;
		unsigned : 1;
    }; 
} __attribute__((packed))  bq25792_temperature_control_t;


#define  BQ25792_NTC_CONTROL_0_ADDR 0x17
#define  BQ25792_NTC_CONTROL_0_SIZE 1
typedef union
{
    uint8_t v;
    struct
    {
		unsigned JEITA_VSET: 3;
		unsigned JEITA_ISETH: 2;
		unsigned JEITA_ISETC: 2;
		unsigned : 1;
    }; 
} __attribute__((packed))  bq25792_ntc_control_0_t;


#define  BQ25792_NTC_CONTROL_0_ADDR 0x18
#define  BQ25792_NTC_CONTROL_0_SIZE 1
typedef union
{
    uint8_t v;
    struct
    {
		unsigned TS_COOL: 2;
		unsigned TS_WARM: 2;
		unsigned BHOT: 2;
		unsigned BCOLD: 1;
		unsigned TS_IGNORE: 1;
    }; 
} __attribute__((packed))  bq25792_ntc_control_0_t;


#define  BQ25792_ICO_CURRENT_LIMIT_ADDR 0x19
#define  BQ25792_ICO_CURRENT_LIMIT_SIZE 2
typedef union
{
    uint16_t v;
    struct
    {
		unsigned : 7;
		unsigned ICO_ILIM: 9;
    }; 
} __attribute__((packed))  bq25792_ico_current_limit_t;


#define  BQ25792_CHARDER_STATUS_0_ADDR 0x1B
#define  BQ25792_CHARDER_STATUS_0_SIZE 1
typedef union
{
    uint8_t v;
    struct
    {
		unsigned IINDPM_STAT: 1;
		unsigned VINDPM_STAT: 1;
		unsigned WD_STAT: 1;
		unsigned POORSRC_STAT: 1;
		unsigned PG_STAT: 1;
		unsigned AC2_PRESENT_STAT: 1;
		unsigned AC1_PRESENT_STAT: 1;
		unsigned VBUS_PRESENT_STAT: 1;
    }; 
} __attribute__((packed))  bq25792_charder_status_0_t;


#define  BQ25792_CHARGER_STATUS_1_ADDR 0x1C
#define  BQ25792_CHARGER_STATUS_1_SIZE 1
typedef union
{
    uint8_t v;
    struct
    {
		unsigned CHG_STAT: 3;
		unsigned VBUS_STAT: 4;
		unsigned BC12_DONE_STAT: 1;
    }; 
} __attribute__((packed))  bq25792_charger_status_1_t;


#define  BQ25792_CHARGER_STATUS_2_ADDR 0x1D
#define  BQ25792_CHARGER_STATUS_2_SIZE 1
typedef union
{
    uint8_t v;
    struct
    {
		unsigned ICO_STAT: 2;
		unsigned : 3;
		unsigned TREG_STAT: 1;
		unsigned DPDM_STAT: 1;
		unsigned VBAT_PRESENT_STAT: 1;
    }; 
} __attribute__((packed))  bq25792_charger_status_2_t;


#define  BQ25792_CHARGER_STATUS_3_ADDR 0x1E
#define  BQ25792_CHARGER_STATUS_3_SIZE 1
typedef union
{
    uint8_t v;
    struct
    {
		unsigned ACRB2_STAT: 1;
		unsigned ACRB1_STAT: 1;
		unsigned ADC_DONE_STAT: 1;
		unsigned VSYS_STAT: 1;
		unsigned CHG_TMR_STAT: 1;
		unsigned TRICHG_TMR_STAT: 1;
		unsigned PRECHG_TMR_STAT: 1;
		unsigned : 1;
    }; 
} __attribute__((packed))  bq25792_charger_status_3_t;


#define  BQ25792_CHARGER_STATUS_4_ADDR 0x1F
#define  BQ25792_CHARGER_STATUS_4_SIZE 1
typedef union
{
    uint8_t v;
    struct
    {
		unsigned : 3;
		unsigned VBATOTG_LOW_STAT: 1;
		unsigned TS_COLD_STAT: 1;
		unsigned TS_COOL_STAT: 1;
		unsigned TS_WARM_STAT: 1;
		unsigned TS_HOT_STAT: 1;
    }; 
} __attribute__((packed))  bq25792_charger_status_4_t;


#define  BQ25792_FAULT_STATUS_0_ADDR 0x20
#define  BQ25792_FAULT_STATUS_0_SIZE 1
typedef union
{
    uint8_t v;
    struct
    {
		unsigned IBAT_REG_STAT: 1;
		unsigned VBUS_OVP_STAT: 1;
		unsigned VBAT_OVP_STAT: 1;
		unsigned IBUS_OCP_STAT: 1;
		unsigned IBAT_OCP_STAT: 1;
		unsigned CONV_OCP_STAT: 1;
		unsigned VAC2_OVP_STAT: 1;
		unsigned VAC1_OVP_STAT: 1;
    }; 
} __attribute__((packed))  bq25792_fault_status_0_t;


#define  BQ25792_FAULT_STATUS_1_ADDR 0x21
#define  BQ25792_FAULT_STATUS_1_SIZE 1
typedef union
{
    uint8_t v;
    struct
    {
		unsigned VSYS_SHORT_STAT: 1;
		unsigned VSYS_OVP_STAT: 1;
		unsigned OTG_OVP_STAT: 1;
		unsigned OTG_UVP_STAT: 1;
		unsigned : 1;
		unsigned TSHUT_STAT: 1;
		unsigned : 2;
    }; 
} __attribute__((packed))  bq25792_fault_status_1_t;


#define  BQ25792_CHARGER_FLAG_0_ADDR 0x21
#define  BQ25792_CHARGER_FLAG_0_SIZE 1
typedef union
{
    uint8_t v;
    struct
    {
		unsigned IINDPM_FLAG: 1;
		unsigned VINDPM_FLAG: 1;
		unsigned WD_FLAG: 1;
		unsigned POORSRC_FLAG: 1;
		unsigned PG_FLAG: 1;
		unsigned AC2_PRESENT_FLAG: 1;
		unsigned AC1_PRESENT_FLAG: 1;
		unsigned VBUS_PRESENT_FLAG: 1;
    }; 
} __attribute__((packed))  bq25792_charger_flag_0_t;


#define  BQ25792_CHARGER_FLAG_1_ADDR 0x23
#define  BQ25792_CHARGER_FLAG_1_SIZE 1
typedef union
{
    uint8_t v;
    struct
    {
		unsigned CHG_FLAG: 1;
		unsigned ICO_FLAG: 1;
		unsigned : 1;
		unsigned VBUS_FLAG: 1;
		unsigned : 1;
		unsigned TREG_FLAG: 1;
		unsigned VBAT_PRESENT_FLAG: 1;
		unsigned BC12_DONE_FLAG: 1;
    }; 
} __attribute__((packed))  bq25792_charger_flag_1_t;


#define  BQ25792_CHARGER_FLAG_2_ADDR 0x24
#define  BQ25792_CHARGER_FLAG_2_SIZE 1
typedef union
{
    uint8_t v;
    struct
    {
		unsigned : 1;
		unsigned DPDM_DONE_FLAG: 1;
		unsigned ADC_DONE_FLAG: 1;
		unsigned VSYS_FLAG: 1;
		unsigned CHG_TMR_FLAG: 1;
		unsigned TRICHG_TMR_FLAG: 1;
		unsigned PRECHG_TMR_FLAG: 1;
		unsigned TOPOFF_TMR_FLAG: 1;
    }; 
} __attribute__((packed))  bq25792_charger_flag_2_t;


#define  BQ25792_CHARGER_FLAG_2_ADDR 0x24
#define  BQ25792_CHARGER_FLAG_2_SIZE 1
typedef union
{
    uint8_t v;
    struct
    {
		unsigned : 1;
		unsigned DPDM_DONE_FLAG: 1;
		unsigned ADC_DONE_FLAG: 1;
		unsigned VSYS_FLAG: 1;
		unsigned CHG_TMR_FLAG: 1;
		unsigned TRICHG_TMR_FLAG: 1;
		unsigned PRECHG_TMR_FLAG: 1;
		unsigned TOPOFF_TMR_FLAG: 1;
    }; 
} __attribute__((packed))  bq25792_charger_flag_2_t;


#define  BQ25792_CHARGER_FLAG_3_ADDR 0x25
#define  BQ25792_CHARGER_FLAG_3_SIZE 1
typedef union
{
    uint8_t v;
    struct
    {
		unsigned : 3;
		unsigned VBATOTG_LOW_FLAG: 1;
		unsigned TS_COLD_FLAG: 1;
		unsigned TS_COOL_FLAG: 1;
		unsigned TS_WARM_FLAG: 1;
		unsigned TS_HOT_FLAG: 1;
    }; 
} __attribute__((packed))  bq25792_charger_flag_3_t;


#define  BQ25792_FAULT_FLAG_0_ADDR 0x26
#define  BQ25792_FAULT_FLAG_0_SIZE 1
typedef union
{
    uint8_t v;
    struct
    {
		unsigned IBAT_REG_FLAG: 1;
		unsigned VBUS_OVP_FLAG: 1;
		unsigned VBAT_OVP_FLAG: 1;
		unsigned IBUS_OCP_FLAG: 1;
		unsigned IBAT_OCP_FLAG: 1;
		unsigned CONV_OCP_FLAG: 1;
		unsigned VAC2_OVP_FLAG: 1;
		unsigned VAC1_OVP_FLAG: 1;
    }; 
} __attribute__((packed))  bq25792_fault_flag_0_t;


#define  BQ25792_FAULT_FLAG_1_ADDR 0x27
#define  BQ25792_FAULT_FLAG_1_SIZE 1
typedef union
{
    uint8_t v;
    struct
    {
		unsigned VSYS_SHORT_FLAG: 1;
		unsigned VSYS_OVP_FLAG: 1;
		unsigned OTG_OVP_FLAG: 1;
		unsigned OTG_UVP_FLAG: 1;
		unsigned : 1;
		unsigned TSHUT_FLAG: 1;
		unsigned : 2;
    }; 
} __attribute__((packed))  bq25792_fault_flag_1_t;


#define  BQ25792_CHARGER_MASK_0_ADDR 0x28
#define  BQ25792_CHARGER_MASK_0_SIZE 1
typedef union
{
    uint8_t v;
    struct
    {
		unsigned IINDPM_MASK: 1;
		unsigned VINDPM_MASK: 1;
		unsigned WD_MASK: 1;
		unsigned POORSRC_MASK: 1;
		unsigned PG_MASK: 1;
		unsigned AC2_PRESENT_MASK: 1;
		unsigned AC1_PRESENT_MASK: 1;
		unsigned VBUS_PRESENT_MASK: 1;
    }; 
} __attribute__((packed))  bq25792_charger_mask_0_t;


#define  BQ25792_CHARGER_MASK_1_ADDR 0x29
#define  BQ25792_CHARGER_MASK_1_SIZE 1
typedef union
{
    uint8_t v;
    struct
    {
		unsigned CHG_MASK: 1;
		unsigned ICO_MASK: 1;
		unsigned : 1;
		unsigned VBUS_MASK: 1;
		unsigned : 1;
		unsigned TREG_MASK: 1;
		unsigned VBAT_PRESENT_MASK: 1;
		unsigned BC1_2_DONE_MASK: 1;
    }; 
} __attribute__((packed))  bq25792_charger_mask_1_t;


#define  BQ25792_CHARGER_MASK_2_ADDR 0x2A
#define  BQ25792_CHARGER_MASK_2_SIZE 1
typedef union
{
    uint8_t v;
    struct
    {
		unsigned : 1;
		unsigned DPDM_DONE_MASK: 1;
		unsigned ADC_DONE_MASK: 1;
		unsigned VSYS_MASK: 1;
		unsigned CHG_TMR_MASK: 1;
		unsigned TRICHG_TMR_MASK: 1;
		unsigned PRECHG_TMR_MASK: 1;
		unsigned TOPOFF_TMR_MASK: 1;
    }; 
} __attribute__((packed))  bq25792_charger_mask_2_t;


#define  BQ25792_CHARGER_MASK_3_ADDR 0x2B
#define  BQ25792_CHARGER_MASK_3_SIZE 1
typedef union
{
    uint8_t v;
    struct
    {
		unsigned : 3;
		unsigned VBATOTG_LOW_MASK: 1;
		unsigned TS_COLD_MASK: 1;
		unsigned TS_COOL_MASK: 1;
		unsigned TS_WARM_MASK: 1;
		unsigned TS_HOT_MASK: 1;
    }; 
} __attribute__((packed))  bq25792_charger_mask_3_t;


#define  BQ25792_FAULT_MASK_0_ADDR 0x2C
#define  BQ25792_FAULT_MASK_0_SIZE 1
typedef union
{
    uint8_t v;
    struct
    {
		unsigned IBAT_REG_MASK: 1;
		unsigned VBUS_OVP_MASK: 1;
		unsigned VBAT_OVP_MASK: 1;
		unsigned IBUS_OCP_MASK: 1;
		unsigned IBAT_OCP_MASK: 1;
		unsigned CONV_OCP_MASK: 1;
		unsigned VAC2_OVP_MASK: 1;
		unsigned VAC1_OVP_MASK: 1;
    }; 
} __attribute__((packed))  bq25792_fault_mask_0_t;


#define  BQ25792_FAULT_MASK_1_ADDR 0x2D
#define  BQ25792_FAULT_MASK_1_SIZE 1
typedef union
{
    uint8_t v;
    struct
    {
		unsigned VSYS_SHORT_MASK: 1;
		unsigned VSYS_OVP_MASK: 1;
		unsigned OTG_OVP_MASK: 1;
		unsigned OTG_UVP_MASK: 1;
		unsigned : 1;
		unsigned TSHUT_MASK: 1;
		unsigned : 2;
    }; 
} __attribute__((packed))  bq25792_fault_mask_1_t;


#define  BQ25792_ADC_CONTROL_ADDR 0x2E
#define  BQ25792_ADC_CONTROL_SIZE 1
typedef union
{
    uint8_t v;
    struct
    {
		unsigned ADC_EN: 1;
		unsigned ADC_RATE: 1;
		unsigned ADC_SAMPLE: 2;
		unsigned ADC_AVG: 1;
		unsigned ADC_AVG_INIT: 1;
		unsigned : 2;
    }; 
} __attribute__((packed))  bq25792_adc_control_t;


#define  BQ25792_ADC_FUNCTION_DISABLE_0_ADDR 0x2F
#define  BQ25792_ADC_FUNCTION_DISABLE_0_SIZE 1
typedef union
{
    uint8_t v;
    struct
    {
		unsigned IBUS_ADC_DIS: 1;
		unsigned IBAT_ADC_DIS: 1;
		unsigned VBUS_ADC_DIS: 1;
		unsigned VBAT_ADC_DIS: 1;
		unsigned VSYS_ADC_DIS: 1;
		unsigned TS_ADC_DIS: 1;
		unsigned TDIE_ADC_DIS: 1;
		unsigned : 1;
    }; 
} __attribute__((packed))  bq25792_adc_function_disable_0_t;


#define  BQ25792_ADC_FUNCTION_DISABLE_1_ADDR 0x30
#define  BQ25792_ADC_FUNCTION_DISABLE_1_SIZE 1
typedef union
{
    uint8_t v;
    struct
    {
		unsigned DP_ADC_DIS: 1;
		unsigned DM_ADC_DIS: 1;
		unsigned VAC2_ADC_DIS: 1;
		unsigned VAC1_ADC_DIS: 1;
		unsigned : 4;
    }; 
} __attribute__((packed))  bq25792_adc_function_disable_1_t;


#define  BQ25792_BUS_ADC_ADDR 0x31
#define  BQ25792_BUS_ADC_SIZE 2
typedef union
{
    uint16_t v;
    struct
    {
		unsigned IBUS_ADC: 16;
    }; 
} __attribute__((packed))  bq25792_bus_adc_t;


#define  BQ25792_IBAT_ADC_ADDR 0x33
#define  BQ25792_IBAT_ADC_SIZE 2
typedef union
{
    uint16_t v;
    struct
    {
		unsigned IBAT_ADC: 16;
    }; 
} __attribute__((packed))  bq25792_ibat_adc_t;


#define  BQ25792_VBUS_ADC_ADDR 0x35
#define  BQ25792_VBUS_ADC_SIZE 2
typedef union
{
    uint16_t v;
    struct
    {
		unsigned VBUS_ADC: 16;
    }; 
} __attribute__((packed))  bq25792_vbus_adc_t;


#define  BQ25792_VAC1_ADC_ADDR 0x37
#define  BQ25792_VAC1_ADC_SIZE 2
typedef union
{
    uint16_t v;
    struct
    {
		unsigned VAC1_ADC: 16;
    }; 
} __attribute__((packed))  bq25792_vac1_adc_t;


#define  BQ25792_VAC2_ADC_ADDR 0x39
#define  BQ25792_VAC2_ADC_SIZE 2
typedef union
{
    uint16_t v;
    struct
    {
		unsigned VAC1_ADC: 16;
    }; 
} __attribute__((packed))  bq25792_vac2_adc_t;


#define  BQ25792_VBAT_ADC_ADDR 0x3B
#define  BQ25792_VBAT_ADC_SIZE 2
typedef union
{
    uint16_t v;
    struct
    {
		unsigned VBAT_ADC: 16;
    }; 
} __attribute__((packed))  bq25792_vbat_adc_t;


#define  BQ25792_VSYS_ADC_ADDR 0x3D
#define  BQ25792_VSYS_ADC_SIZE 2
typedef union
{
    uint16_t v;
    struct
    {
		unsigned VSYS_ADC: 16;
    }; 
} __attribute__((packed))  bq25792_vsys_adc_t;


#define  BQ25792_TS_ADC_ADDR 0x3F
#define  BQ25792_TS_ADC_SIZE 2
typedef union
{
    uint16_t v;
    struct
    {
		unsigned TS_ADC: 16;
    }; 
} __attribute__((packed))  bq25792_ts_adc_t;


#define  BQ25792_TDIE_ADC_ADDR 0x41
#define  BQ25792_TDIE_ADC_SIZE 2
typedef union
{
    uint16_t v;
    struct
    {
		unsigned TDIE_ADC: 16;
    }; 
} __attribute__((packed))  bq25792_tdie_adc_t;


#define  BQ25792_DP_ADC_ADDR 0x43
#define  BQ25792_DP_ADC_SIZE 2
typedef union
{
    uint16_t v;
    struct
    {
		unsigned DP_ADC: 16;
    }; 
} __attribute__((packed))  bq25792_dp_adc_t;


#define  BQ25792_DN_ADC_ADDR 0x45
#define  BQ25792_DN_ADC_SIZE 2
typedef union
{
    uint16_t v;
    struct
    {
		unsigned DN_ADC: 16;
    }; 
} __attribute__((packed))  bq25792_dn_adc_t;


#define  BQ25792_DPDM_DRIVER_ADDR 0x47
#define  BQ25792_DPDM_DRIVER_SIZE 1
typedef union
{
    uint8_t v;
    struct
    {
		unsigned DPLUS_DAC: 3;
		unsigned DMINUS_DAC: 3;
		unsigned : 2;
    }; 
} __attribute__((packed))  bq25792_dpdm_driver_t;


#define  BQ25792_PART_INFORMATION_ADDR 0x48
#define  BQ25792_PART_INFORMATION_SIZE 1
typedef union
{
    uint8_t v;
    struct
    {
		unsigned : 2;
		unsigned PN: 3;
		unsigned DEV_REV: 3;
    }; 
} __attribute__((packed))  bq25792_part_information_t;



#ifdef __cplusplus
}
#endif
#endif // TI_BQ25792_H
