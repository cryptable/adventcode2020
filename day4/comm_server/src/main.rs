#![no_std]
#![cfg_attr(target_arch = "aarch64", no_main)]
#![feature(global_asm)]

#[cfg(target_arch = "aarch64")]
global_asm!(include_str!("start.s"));

mod panic;
mod comm;
mod periferals;
mod memory;

#[cfg(target_arch = "aarch64")]
#[no_mangle]
pub extern "C" fn rmain() {

  let mut comm_out = comm::Comm::new();
  let mut comm_in = comm::Comm::new();

  loop {
    comm_in.receive_msg();
    if comm_in.get_cmd() == 0x02 {
      comm_out.print_msg("Help recevied:");
      comm_out.send_msg(0x03, comm_in.get_buf());
    }
  }

}

#[cfg(target_arch = "x86_64")]
fn main() {

  let mut comm_out = comm::Comm::new();
  let mut comm_in = comm::Comm::new();

  loop {
    comm_in.receive_msg();
    if comm_in.get_cmd() == 0x02 {
      comm_out.print_msg("Help recevied:");
      comm_out.send_msg(0x03, comm_in.get_buf());
    }
  }

}