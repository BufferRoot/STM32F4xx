# GY Local Patch Changelog
> Branch/patch applied on top of grblHAL/STM32F4xx master (8300aa0, 2026-09-09)

---

## 2026-09-09

### Sync
- Synced tree + submodules to [grblHAL/STM32F4xx](https://github.com/grblHAL/STM32F4xx) `8300aa0` ("Updated submodules").
- Keypad now tracks upstream `Plugin_I2C_keypad` `c349330` (proper `KEYPAD_ENABLE=2` UART/MPG path). Prior Interactive_Jog local name fix no longer required.
- `flexi_script.py`: quote `$BUILD_DIR` paths so UF2 post-build works when the workspace path contains spaces.

### Reapplied GY overlays (unchanged intent from 2026-04-11)
- `FLEXI_STM32F446RETX_BL_FLASH_EMU.ld`, `boards/flexi_hal_map.h` (EEPROM emul, dual UART ports, PROBE2)
- `platformio.ini` `[env:f446re_flexi_3axis_basic]` + `[env:flexi]`

---

## 2026-04-11

### New Files

#### `FLEXI_STM32F446RETX_BL_FLASH_EMU.ld`
- New linker script for Flexi-HAL with flash-emulated EEPROM layout:
  - `BOOT_FLASH`: `0x08000000`, 48K (tinyuf2 bootloader)
  - `EEPROM_EMUL`: `0x0800C000`, 16K (flash sector 3)
  - `FLASH` (app): `0x08010000`, 448K
- Exports `_EEPROM_Emul_Start`, `_EEPROM_Emul_Sector`, `_FLASH_VectorTable`
- Required by all Flexi-HAL environments when `EEPROM_ENABLE` is not set (flash emulation path in `flash.c`)

---

### Modified Files

#### `boards/flexi_hal_map.h`
1. **EEPROM emulation override** — added `#undef EEPROM_ENABLE` after the `I2C_ENABLE` block. This removes the forced `i2c_eeprom_init` dependency and routes NVS storage through the flash emulation driver instead.
2. **Serial port reassignment** — updated default serial port mapping:
   - `SERIAL_PORT = 6` (GPIOC TX=6, RX=7) — primary/USB-replacement stream
   - `SERIAL1_PORT = 33` (GPIOC TX=10, RX=5) — secondary stream
   - `SERIAL2_PORT = 1` (GPIOA TX=9, RX=10) — tertiary stream
   - Previous single-port config commented out for reference
3. **PROBE2 on AUXINPUT3** — replaced `SAFETY_DOOR` assignment on `AUXINPUT3` with `PROBE2`:
   - `PROBE2_PORT` / `PROBE2_PIN` → `AUXINPUT3_PORT` / `AUXINPUT3_PIN`
   - Original `SAFETY_DOOR` block commented out

#### `platformio.ini`
1. **`[env:f446re_flexi_3axis_basic]`** — switched `board_build.ldscript` from `FLEXI_STM32F446RETX_BL_FLASH.ld` to `FLEXI_STM32F446RETX_BL_FLASH_EMU.ld` (required after EEPROM emulation change in board map).
2. **`[env:flexi]`** — new full-featured Flexi-HAL environment added:
   - 4-axis (N_AXIS=4, Y_GANGED, Y_AUTO_SQUARE)
   - Dual spindle: Huanyang VFD (SPINDLE0=11) + second VFD (SPINDLE1=6) via MODBUS
   - WIZnet W5500 Ethernet with LwIP (TELNET, FTP, WebSocket, HTTP, WebUI)
   - SD card (SDCARD_ENABLE=2), MPG (MPG_ENABLE=2), PROBE2, TOOLSETTER
   - KEYPAD_ENABLE=2 (UART keypad, no I2C strobe required)
   - NVS_SIZE=16384, DEFAULT_PLANNER_BUFFER_BLOCKS=128
   - Flash-emulated EEPROM linker script
   - Machine defaults pre-configured (steps/mm, travel, rates, homing, jerk)
   - `lib_deps` pulls `${wiznet_networking.lib_deps}`; `lib_extra_dirs` includes `lwip`, `networking`, `FatFs`
   - Post-build: `flexi_script.py` → `firmware.uf2` (family `0x57755a57`, base `0x08010000`)

---

### Submodule Updates

#### `spindle/` — switched upstream
- **From**: `https://github.com/Expatria-Technologies/Plugins_spindle` (branch `vfd_support`, commit `66540c0`)
- **To**: `https://github.com/grblHAL/Plugins_spindle` (branch `master`, commit `9b32c53`)
- Reason: Expatria fork had stale `modbus_settings_t` typedef and old `stream_enumerate_streams` signature (missing `void *data` argument) incompatible with updated grblHAL core.

#### `keypad/` — (superseded 2026-09-09)
- Earlier Interactive_Jog local `#else` name fix replaced by sync to upstream keypad `c349330`.

---

### Build Results

| Environment | Result | UF2 Size | Notes |
|---|---|---|---|
| `f446re_flexi_3axis_basic` | ✅ SUCCESS (2026-04-11) | 421,376 bytes | 3-axis, USB CDC, no plugins |
| `flexi` | ✅ SUCCESS (2026-09-09) | 751,616 bytes | 4-axis, ETH, WebUI, VFD, SD — post-sync |
