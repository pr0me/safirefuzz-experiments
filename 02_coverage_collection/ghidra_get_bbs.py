from ghidra.program.model.block import SimpleBlockModel
from ghidra.util.task import TaskMonitor

bbm = SimpleBlockModel(currentProgram)
blocks = bbm.getCodeBlocks(TaskMonitor.DUMMY)
block = blocks.next()
name = '{}_bbs.txt'.format(currentProgram.getName())

with open(name, 'w') as f:

    while block:
        f.write("{}\n".format(block.minAddress))
        block = blocks.next()
