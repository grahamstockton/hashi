import random
from collections import deque

class Island:
    def __init__(self, Xpos, Ypos, bridges = 0):
        self.x = Xpos
        self.y = Ypos
        self.bridge_number = bridges

class HashiGenerator:
    def __init__(self, width = 6, isl_density = .5, wander_distrib = None):
        self.width = width
        self.max_island_number = int(.3 * width * width)
        self.__island_dict = {}
        self.num_islands = 0

        # if no wander_distrib, come up with one
        if wander_distrib:
            self.wander_distrib = wander_distrib
        else:
            # simple distribution of edge distances. Will be sampled randomly when determining walk distance
            self.wander_distrib = [*[i for i in range(width//3)], *[i for i in range(width//2)], *[i for i in range(width)]]

    def gen_max_wander_dist(self):
        return random.choice(self.wander_distrib)

    def is_valid_position(self, row, col):
        return (0 <= row < self.width) and (0 <= col < self.width)

    def generate_islands(self):
        # Clear Islands in case of reuse
        self.__island_dict.clear()

        # Create first island
        first_island = Island(random.randint(0, self.width - 1), random.randint(0, self.width - 1))
        self.__island_dict[str([first_island.x, first_island.y])] = first_island

        # We want to do this in a breadth-first fashion, so that we don't get single branches
        crawl_queue = deque([ [[first_island.x, first_island.y], (0, 0)] ]) # (0, 0) is initial origin direction

        while crawl_queue:
            # Stop if we have enough islands
            if self.num_islands >= self.max_island_number:
                break

            # Pop the start position
            start_pos, origin_direction = crawl_queue.popleft()

            # We want a subroutine for each direction
            for direction in ((-1, 0), (1, 0), (0, 1), (0, -1)):
                # check if this is the direction you came from
                if origin_direction == direction:
                    continue
                # get a position for the crawler
                crawler_pos = start_pos[:]
                # create max crawl distance
                dist = self.gen_max_wander_dist()

                for k in range(dist):
                    # move in direction
                    crawler_pos[0] += direction[0]
                    crawler_pos[1] += direction[1]

                    # Check if valid
                    if not self.is_valid_position(*crawler_pos):
                        break

                    # Check if you landed on an island
                    encountered_island = self.__island_dict.get(str(crawler_pos), False)
                    if encountered_island:
                        # create an edge weight
                        edge_wt = random.randint(1,2)
                        # update both old and new island for the edge weight
                        encountered_island.bridge_number += edge_wt
                        self.__island_dict[str(start_pos)].bridge_number += edge_wt
                        break

                    # If at end of walk, create a connected island and add its position to the queue
                    if k == dist - 1:
                        # Make new island and put it in dict, queue
                        new_island = Island(*crawler_pos, 1)
                        self.__island_dict[str(crawler_pos)] = new_island
                        crawl_queue.append([[new_island.x, new_island.y], (-1*direction[0], -1*direction[1])]) # -1 because relative to new island, it will be opposite direction

                        # increment num_islands, edge count of old island
                        self.num_islands += 1
                        self.__island_dict[str(start_pos)].bridge_number += 1

    def get_islands(self):
        return list(self.__island_dict.values())

    def __str__(self):
        island_array = [[0 for i in range(self.width)] for j in range(self.width)]
        for isl in self.__island_dict.values():
            island_array[isl.x][isl.y] = isl.bridge_number
        return "\n".join(" ".join(str(item) for item in arr) for arr in island_array)


def main():
    # Tests go here
    pass

if __name__ == '__main__':
    main()