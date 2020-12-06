
struct Comm {
    cmd: u8,
    lg: u32,
    buffer: [u8; 256],
}