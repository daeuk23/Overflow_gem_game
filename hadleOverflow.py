from dataInput import Queue

def get_overflow_list(grid):  # returning spots which is overflows
    rows = len(grid)          # total number of rows
    cols = len(grid[0])       # total number of cols
    overflowing_cells = []    # empty initially

    def spot_in_corner(r, c): # this is case of spot in corner within grid, having 2 neighbors
        return (r == 0 or r == rows - 1) and (c == 0 or c == cols - 1)

    def spot_in_edge(r, c):   # this is case of edge in corner within grid, having 3 neighbors
        return (r == 0 or r == rows - 1 or c == 0 or c == cols - 1) and not spot_in_corner(r, c)

    for r in range(rows):
        for c in range(cols):
            value = abs(grid[r][c]) 
            if spot_in_corner(r, c):
                if value >= 2:
                    overflowing_cells.append((r, c))
            elif spot_in_edge(r, c):
                if value >= 3:
                    overflowing_cells.append((r, c))
            else:
                if value >= 4:
                    overflowing_cells.append((r, c))

    if not overflowing_cells:  # case no overflowing_cells, empty overflow cells than should return none 
        return None

    return overflowing_cells


def overflow(grid, a_queue):
    overflow_cells = get_overflow_list(grid)
    sign_flag = is_same_sign(grid)
    if overflow_cells is not None and not sign_flag:  # this is only meaning that grid is overflow
        for r, c in overflow_cells:
            # set sign of cell
            original_sign = 1 if grid[r][c] > 0 else -1
            
            # set cell value to 0
            grid[r][c] = 0

        for r, c in overflow_cells:
            # updating neighbors
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
                    grid[nr][nc] = abs(grid[nr][nc]) + 1  # neighbor update logic absolute calculation
                    grid[nr][nc] *= original_sign

        #a_queue.enqueue(grid) # my initial version with swallow copy (problem)
        a_queue.enqueue([row.copy() for row in grid]) # deep copying grid to queue
        #return overflow(grid, a_queue) # my initial version is just calling overflow recursively
        return 1 + overflow(grid, a_queue) # count how many times recursive function has called

    else:
        #return len(a_queue) # my original version return length at last step bur fixed
        return 0



def is_same_sign(grid): # function for checking second statement of overflow (if all sign is same then grid is not overflow)
    initial_sign = None  # initially none

    for row in grid:
        for value in row:
            if value != 0:  # value is not 0
                if initial_sign is None:  # no setted initial sign (first loop)
                    if value > 0:
                        initial_sign = 1
                    else:
                        initial_sign = -1
                else:  # initial sign setted
                    if (value > 0 and initial_sign == -1) or (value < 0 and initial_sign == 1):
                        return False  # different sign found, return False

    return True  # all same signs
