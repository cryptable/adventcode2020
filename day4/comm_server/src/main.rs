#![no_std]
#![no_main]
#![feature(global_asm)]
#![feature(asm)]

global_asm!(include_str!("start.s"));

mod panic;
mod periferals;

#[no_mangle]
pub extern "C" fn rmain() {

  let uart = periferals::uart1::Uart1::new();

  uart.puts("Hello, world!\n");

  loop {
    uart.putc(uart.getc());
  }

}