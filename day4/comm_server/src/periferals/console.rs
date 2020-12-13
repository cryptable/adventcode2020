/*
 * Chapter 11: UART
 */
use core::ptr;
use crate::periferals::memmap::MMIO_BASE;

const UART0_IO: *mut u32         = (MMIO_BASE + 0x00201000) as *mut u32;

pub fn console_puts(value: &str) {
  for c in value.chars() {
    unsafe {
      ptr::write_volatile(UART0_IO as *mut u8, c as u8);
    }
  }
}