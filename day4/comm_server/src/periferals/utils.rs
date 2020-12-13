
#[cfg(target_arch = "aarch64")]
global_asm!(include_str!("asmutils.s"));

#[cfg(target_arch = "aarch64")]
extern {
    fn asm_delay(t: isize);
}

#[cfg(target_arch = "aarch64")]
pub fn delay(time: isize) {
  unsafe {
    asm_delay(time);
  }
}

#[cfg(target_arch = "x86_64")]
pub fn delay(time: isize) {
    for _ in 0..time {}
}