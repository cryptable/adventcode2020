use crate::memory::Page;
use crate::periferals;

pub fn u32_to_array_u8(x: u32) -> [u8;4] {
    let b1 : u8 = ((x >> 24) & 0xFF) as u8;
    let b2 : u8 = ((x >> 16) & 0xFF) as u8;
    let b3 : u8 = ((x >> 8) & 0xFF) as u8;
    let b4 : u8 = (x & 0xFF) as u8;

    [b1, b2, b3, b4]
}

pub fn array_u8_to_u32(x: &[u8; 4]) -> u32 {
    let mut b1 : u32 = ((x[0] as u32) << 24) & 0xFF000000;
    b1 |= ((x[1] as u32) << 16) & 0x00FF0000;
    b1 |= ((x[2] as u32) << 8) & 0x0000FF00;
    b1 |= (x[3] as u32) & 0x000000FF;

    b1
}


pub(crate) struct Comm {
    uart: periferals::uart1::Uart1,
    msg: Page,
    cmd: u8,
}


impl Comm {
    pub fn new() -> Comm {
        return Comm {
            uart: periferals::uart1::Uart1::new(),
            msg: Page::new(),
            cmd: 0x0
        }
    }

    fn encode_msg(&mut self, cmd: u8, data: &[u8]) {
        let lg: [u8; 4] = u32_to_array_u8(data.len() as u32 );
        self.msg.push(cmd).unwrap();
        self.msg.store(&lg).unwrap();
        self.msg.store(data).unwrap();
    }

    pub fn print_msg(&mut self, msg: &str) {
        self.send_msg(0x01, msg.as_ref());
    }

    pub fn send_msg(&mut self, cmd: u8, msg: &[u8]) {
        self.encode_msg(cmd, msg.as_ref());
        self.uart.putb(self.msg.getbuf());
        self.msg.free();
    }

    pub fn receive_msg(&mut self) {
        self.cmd = self.uart.getc();
        let mut lg_bytes : [u8; 4] = [0x0; 4];
        lg_bytes[0] = self.uart.getc();
        lg_bytes[1] = self.uart.getc();
        lg_bytes[2] = self.uart.getc();
        lg_bytes[3] = self.uart.getc();

        let lg = array_u8_to_u32(&lg_bytes);
        for _ in 0..lg {
            self.msg.push(self.uart.getc());
        }
    }

    pub fn get_cmd(&self) -> u8 {
        return self.cmd;
    }

    pub fn get_buf(&self) -> &[u8] {
        return self.msg.getbuf();
    }

}
