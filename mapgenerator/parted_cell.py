from cell import Cell
from directions import Side, Partition


class Parted_Cell(Cell):
    """
    A Parted (partitioned) Cell is divided into four partitions.
    Each of those can contain something, like an activator, or a 
    higher level.
    """

    def __init__(self, top_rt=None, bot_rt=None, 
            bot_lt=None, top_rt=None):

        self.partitions = {Partition.TOP_R: top_rt,
                          Partition.BOT_R: bot_rt,
                          Partition.BOT_L: bot_lt,
                          Partition.TOP_L: top_lt}

        self.asd = 1

    def set_item(self, item, partition):
        self.partitions[partition] = item

    def get_items(self):
        return self.partitions.values()



