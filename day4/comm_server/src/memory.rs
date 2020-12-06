use core::slice::index::slice_end_index_len_fail;

const PAGE_SIZE: usize = 4096;
const PAGE_COUNT: usize = 32;

struct Page {
    free: usize,
    buffer: [u8; PAGE_SIZE],
    next: isize
}

struct PageList {
    pages: [Page; PAGE_COUNT]
}

const MEMORY: PageList = PageList {
    pages: [ Page {
        free:PAGE_SIZE,
        buffer:[0x00; PAGE_SIZE],
        next: -1,
    } ; PAGE_COUNT]
};

fn free_page() -> isize {
    for i in range(MEMORY.len()) {
        if MEMORY[i].free == PAGE_SIZE {
            return i;
        }
    }
    return -1;
}

impl Page {
    pub fn new() -> Result<Page, &'static str> {
        for page in MEMORY {
            if page.free == PAGE_SIZE {
                return Ok(page);
            }
        }
        return Err("Out of MEMORY");
    }

    pub fn get(&self, pos: u32) -> Result<u8, &'static str> {
        let page_idx = pos / PAGE_SIZE;

        if page >= 32 {
            return Err("Out of Range");
        }

        let mut page = self;
        for idx in range(page_idx) {
            if page.next < 0 {
                return Err("Out of Range");
            }
            page = MEMORY[page.next];
        }
        if pos > (PAGE_SIZE - page.free) as u32 {
            return Err("Out of Range");
        }

        return page.buffer[pos]
    }

    fn free_mem_size(&self) -> usize {
        let mut free: usize = self.free;

        for page in MEMORY {
            if page.free == PAGE_SIZE {
                free += page.free;
            }
        }

        return free;
    }

    fn put(&mut self, kar: u8) {
        let mut page = self;
        while page.free == 0 {
            if page.next == -1 {
                page.next = free_page();
                page = MEMORY[page.next];
                break;
            }
            page = MEMORY[page.next];
        }
        page.buffer[PAGE_SIZE-page.free] = u8;
    }

    pub fn store(&self, data: &[u8]) -> Result<usize, &'static str> {
        let mut page = self;

        if self.free_mem_size() < data.len() {
            Err("Out of Memory")
        }

        for d in data {
            put(d)
        }

        return Ok(data.len())
    }

}