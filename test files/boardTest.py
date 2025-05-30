import unittest
from gameBoard import evaluate_board, GameTree

class A2BTestCase(unittest.TestCase):
    """These are the test cases for functions and classes of a2"""
    
    def test_eval_max_and_min(self):
        boards = [[
                    # a few non-winning boards
                    [ 0 , 2,  -1, 0, 0,  0],
                    [ 2,  0 , 0,  0,  0,  0],
                    [ 1,  0,  0,  0,  0, 0],
                    [ 0,  0,  0,  0,  2, 0],
                    [ 0,  0,  0,  2,  0, -1]
                     ],
                    [
                    [ 1 , 0,  2,  0, 0,  0],
                    [ 0,  2 , 0,  0,  0,  0],
                    [ 2,  0,  3,  0,  0, 0],
                    [ 0,  0,  0,  -3,  0, 0],
                    [ 0,  0,  0,  0, -2, -1]
                    ],
                    #p1 winning board
                    [
                    [ 0 , 1,  2,  0, 0,  0],
                    [ 1,  2 , 0,  0,  0,  0],
                    [ 2,  0,  0,  3,  0, 0],
                    [ 0,  0,  3,  0,  0, 0],
                    [ 0,  0,  0,  0,  0, 0]
                    ],
                    # p2 winning board
                    [
                    [ 0 , -1,  -2,  0, 0,  0],
                    [ -1,  -2 , 0,  0,  0,  0],
                    [ -2,  0,  -3,  0,  0, 0],
                    [ 0,  0,  0,  0,  0, 0],
                    [ 0,  0,  0,  0,  0, 0]
                    ]
        ]
        p1_scores= []
        p2_scores= []
        for board in boards:
            p1_scores.append(evaluate_board(board, 1))
            p2_scores.append(evaluate_board(board, -1))

        # a winning board for p1 should have higher score than for any other board 
        self.assertGreater(p1_scores[2], p1_scores[0])
        self.assertGreater(p1_scores[2], p1_scores[1])
        self.assertGreater(p1_scores[2], p1_scores[3])

        # a winning board for p2 (thus losing for p1) should have lower score than any other board
        self.assertLess(p1_scores[3], p1_scores[0])
        self.assertLess(p1_scores[3], p1_scores[1])
        self.assertLess(p1_scores[3], p1_scores[2])

        # a winning board for p1 (thus losing for p2) should have lower score than any other for p2 
        self.assertLess(p2_scores[2], p2_scores[0])
        self.assertLess(p2_scores[2], p2_scores[1])
        self.assertLess(p2_scores[2], p2_scores[3])

        # a winning board for p2 should have higher score for p2 than any other board
        self.assertGreater(p2_scores[3], p2_scores[0])
        self.assertGreater(p2_scores[3], p2_scores[1])
        self.assertGreater(p2_scores[3], p2_scores[2])

        # wins and losses should have same score for both player
        self.assertEqual(p1_scores[2],p2_scores[3])
        self.assertEqual(p1_scores[3],p2_scores[2])
        
    def test_gametree(self):
        
        boards = [[
                    # a board that is one move away from winning for p1
                    [ 0 , 2,  -2, 0, 0,  0],
                    [ 0,  0 , -3,  -1,  0,  0],
                    [ 0,  0,  0,  0,  0, 0],
                    [ 0,  0,  0,  0,  2, 0],
                    [ 0,  0,  0,  2,  0, 0]
                     ],
                    # a board that is one move away from winning for p2
                    [
                    [ 0 , -2, 2, 0, 0,  0],
                    [ 0,  0,  3,  1,  0,  0],
                    [ 0,  0, -1,  0,  0, 0],
                    [ 0,  0,  0,  0, -2, 0],
                    [ 0,  0,  0,  -2,  0, 0]
                    ],
                    # a board where p1 places piece in any corner will guarantee a win for p2 (p1 must avoid corners)
                    [
                    [ 0 , 0,  0,  0,  0,  0],
                    [ -1, 0,  0,  0,  0,  -1],
                    [ -2, 3,  3,  3,  3, -2],
                    [ -1, 0,  0,  0,  0, -1],
                    [ 0,  0,  -2,  -1,  0,  0]
                    ],
                    # a board where p2 places piece in any corner will guarantee a win for p1 (p2 must avoid corners)
                    [
                    [ 0 , 0,  0,  0,  0,  0],
                    [ 1, 0,  0,  0,  0,  1],
                    [ 2, -3,  -3,  -3,  -3, 2],
                    [ 1, 0,  0,  0,  0, 1],
                    [ 0,  0,  2,  1,  0,  0]
                    ]

        ]

    # ensure bots will always take an obvious winning move
        tree = GameTree(boards[0], 1)
        (row,col) = tree.get_move()
        self.assertEqual((row,col),(0,1))

        tree = GameTree(boards[1], -1)
        (row,col) = tree.get_move()
        self.assertEqual((row,col),(0,1))

        tree = GameTree(boards[2], 1)
        (row,col) = tree.get_move()
        self.assertNotEqual((row,col), (0,0))
        self.assertNotEqual((row,col), (0,5))
        self.assertNotEqual((row,col), (4,0))
        self.assertNotEqual((row,col), (4,5))

        tree = GameTree(boards[3], -1)
        (row,col) = tree.get_move()
        self.assertNotEqual((row,col), (0,0))
        self.assertNotEqual((row,col), (0,5))
        self.assertNotEqual((row,col), (4,0))
        self.assertNotEqual((row,col), (4,5))


if __name__ == '__main__':
    unittest.main()
