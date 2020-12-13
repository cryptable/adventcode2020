

class Assembly:

    def __init__(self, cmd, arg):
        self.cmd = cmd
        self.arg = int(arg)
        self.passed = 0


class Cpu:

    def __init__(self):
        self.pc = 0
        self.acc = 0

    def run(self, code_mem):
        while True:
            if self.pc == len(code_mem):
                print("OK")
                return True
            if self.pc > len(code_mem):
                return True
            if code_mem[self.pc].passed > 0:
                return False
            if code_mem[self.pc].cmd == "nop":
                code_mem[self.pc].passed += 1
                self.pc += 1
            elif code_mem[self.pc].cmd == "jmp":
                code_mem[self.pc].passed += 1
                self.pc += code_mem[self.pc].arg
            elif code_mem[self.pc].cmd == "acc":
                code_mem[self.pc].passed += 1
                self.acc += code_mem[self.pc].arg
                self.pc += 1
            else:
                raise Exception('Unknown command')

    def reset(self):
        self.pc = 0
        self.acc = 0


def printMem(mem):
    print("Assemby")
    for cmd in mem:
        print("{} {}".format(cmd.cmd, cmd.arg))


def copyMem(mem):
    copy = []
    for cmd in mem:
        copy.append(Assembly(cmd.cmd, cmd.arg))
    return copy


if __name__ == '__main__':
    with open("./input.txt", "r") as infile:
        code_mem = []
        for line in infile:
            cmd = line.split(' ')
            code_mem.append(Assembly(cmd[0], cmd[1]))
        infile.close()

    cpu = Cpu()
    for idx in range(0, len(code_mem)):
        modified_mem = copyMem(code_mem)
        if modified_mem[idx].cmd == "nop":
            modified_mem[idx].cmd = "jmp"
        elif modified_mem[idx].cmd == "jmp":
            modified_mem[idx].cmd = "nop"
        if cpu.run(modified_mem):
            print(cpu.acc)
        cpu.reset()