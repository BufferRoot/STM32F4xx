# GrblHAL STM32F4xx Driver (Flexi-HAL Optimized)

A high-performance **grblHAL driver for STM32F4 series processors**, specifically tuned for the **Flexi-HAL board (STM32F446RET6 @ 180 MHz)**.

> ⚡ **Key Highlights**
>
> * Optimized for **maximum motion performance and deterministic timing**
> * Enables **Dual UART mode on Flexi-HAL hardware**
> * Designed for **high-speed, multi-interface CNC control systems**

---

## 🚀 Quickstart

The Flexi-HAL implementation is designed for the **tinyuf2 bootloader**.
It is strongly recommended to build using **PlatformIO** to ensure all linker scripts and performance patches are applied correctly.

### 🔧 Build with PlatformIO

Clone the repository (with submodules):

```bash id="5n0d8y"
git clone --recurse-submodules https://github.com/grblHAL/STM32F4xx.git
```

Compile for your target:

* **Basic 3-Axis**

```bash id="qz3d7c"
pio run -e f446re_flexi_3axis_basic
```

* **Full Featured (ETH / WebUI / VFD)**

```bash id="v2ybq9"
pio run -e flexi
```

### 📦 Deployment

Copy the generated `firmware.uf2` file to the **FLEXI USB drive**.

---

## 🧠 GY Local Patch Changelog

**Latest: 2026-04-11**

This patch integrates **performance tuning**, **hardware remapping**, and **enhanced communication capabilities** for the Flexi-HAL platform.

---

### 1. 🧩 Memory & Storage Architecture

* Flash EEPROM moved to internal flash (`0x0800C000`)
* Custom linker: `FLEXI_STM32F446RETX_BL_FLASH_EMU.ld`
* Memory layout:

  * 48K bootloader
  * 448K application
* Vector table offset: `0x08010000`

---

### 2. 🔌 Peripheral & Pin Remapping

* **Dual UART Mode (Flexi-HAL Enhancement)**

  * Multiple hardware serial streams enabled simultaneously
  * Designed for concurrent:

    * Host communication
    * Peripheral control (VFD, MPG, etc.)

* **Enhanced Serial Mapping**

  * Stream 1 (Serial 6): GPIOC TX6 / RX7 *(Primary interface)*
  * Stream 2 (Serial 33): GPIOC TX10 / RX5 *(Secondary interface)*
  * Stream 3 (Serial 1): GPIOA TX9 / RX10 *(Tertiary/debug)*

* Probe2 → AUXINPUT3

* 4-axis with Y-ganging + auto-squaring

---

### 3. 🌐 Integrated Features (flexi)

* W5500 Ethernet (LwIP: Telnet, FTP, WebUI)
* Dual VFD (Huanyang + Modbus)
* SD support:

```c id="m6yq9g"
SDCARD_ENABLE = 2
```

---

### 4. 🛠 Bug Fixes

* Plugins_spindle alignment fix
* Keypad UART build fix
* SysTick priority fix (eliminates stepper jitter under load)

---

## ⚡ Performance Tuning Details

| Category     | Setting        | Value / Notes                             |
| ------------ | -------------- | ----------------------------------------- |
| CPU          | Clock Speed    | 180 MHz                                   |
| FPU          | Float ABI      | hard (-mfpu=fpv4-sp-d16)                  |
| Optimization | Flags          | -O3 -ffast-math (LTO disabled)            |
| Motion       | Stepper Timer  | 90 MHz (STEPPER_TIMER_DIV = 1)            |
| Motion       | Planner Buffer | 256 (Basic) / 128 (ETH)                   |
| Motion       | Features       | Jerk Control, G187, Backlash Compensation |

---

## 🏗 Build Environment Matrix

| Environment              | Axis | Networking | Features                 |
| ------------------------ | ---- | ---------- | ------------------------ |
| f446re_flexi_3axis_basic | 3    | USB        | Minimal                  |
| flexi                    | 4    | W5500 ETH  | WebUI, SD, Dual VFD, MPG |

---

## 📌 Patch Baseline

```id="7sm3fp"
grblHAL/STM32F4xx (5c93e06, 2026-03-31)
```

---

## 💡 Notes

* Built for **high-throughput motion control**
* Dual UART enables **simultaneous host + device communication**
* Deterministic ISR timing for **smooth step generation**
* PlatformIO required for correct builds

---
