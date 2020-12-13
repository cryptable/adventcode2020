use core::panic::PanicInfo;

#[cfg(target_arch = "aarch64")]
#[panic_handler]
fn on_panic(_info: &PanicInfo) -> ! {
    loop {}
}