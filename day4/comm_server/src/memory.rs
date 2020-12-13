
const PAGE_SIZE: usize = 32768;
const PAGE_COUNT: usize = 32;

pub struct Page {
    free: usize,
    buffer: [u8; PAGE_SIZE],
    next: isize
}

impl Page {
    pub fn new() -> Page {
        return Page {
            free: PAGE_SIZE,
            buffer: [0x0; PAGE_SIZE],
            next: -1,
        }
    }

    pub fn get(&self, pos: u32) -> Result<u8, &'static str> {
        if pos >= PAGE_SIZE as u32 {
            return Err("Out of Range");
        }
        Ok(self.buffer[pos as usize])
    }

    fn free_mem_size(&self) -> usize {
        let free: usize = self.free;

        return free;
    }

    pub fn len(&self) -> usize {
        PAGE_SIZE - self.free
    }

    pub fn getbuf(&self) -> &[u8] {
        return &self.buffer[0..self.len()]
    }

    pub fn push(&mut self, kar: u8) -> Result<usize, &'static str> {
        if self.free <= 0 {
            return Err("Out of Memory");
        }
        self.buffer[PAGE_SIZE - self.free] = kar;
        self.free -= 1;

        Ok((PAGE_SIZE - self.free -1) as usize)
    }

    pub fn store(&mut self, data: &[u8]) -> Result<usize, &'static str> {
        if self.free_mem_size() < data.len() {
            return Err("Out of Memory");
        }

        for d in data {
            self.push(*d).unwrap();
        }

        Ok(data.len())
    }

    pub fn free(&mut self) {
        self.free = PAGE_SIZE;
        self.next = -1;
    }
}

#[cfg(test)]
mod tests {

}