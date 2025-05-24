# Overflow Gem Game
This project is a simple board game where players use gems on a board following specific rules.  
It includes various features such as player-versus-player matches and the ability to play against an AI opponent.  

## Informations  
### Contributer  

[DaeukKim](https://www.linkedin.com/in/daeuk-kim-68628231b/)  : Leader, develop rest of files except game.py  
contact : Email -> a24738598@gmail.com  
[TaeheunKim](https://www.linkedin.com/in/tae-heun-kay-kim-a21021273/)  : dataInput.py, handleOverflow.py  
[ChanwookKang](https://github.com/senecaChanwook) : gameboard.py, play1,2.py  
game.py : contributed by [Caterine-leung](https://www.linkedin.com/in/catherine-leung-4578aa11/?originalSubdomain=ca)  

### period of this project  
Initiative steps and documents : July 21th 2024  
Initial programmed date : Aug 1th 2024  
testing and error handling : Aug 4th 2024  
Finalized with new features : Aug 11th 2024  

## Features  
-** Gem game : Provide a game UI to play games with points by placing gem on the board according to the set rules  
-** Players and AI : Two players will be able to watch the match on **one device** and will also have options to compete against ai  
-** Basic method : Based on the hash table, the method of putting data on the board (the possibility of data loss x)

### Updated feature (Aug 11th 2024)  
-** Board size changeable : 3*4 to 5*6 freely changeable game rules accordingly  
-** new Interface : Appears a color-selectable interface  
-** Reduced time complexity : It significantly reduced the computational time for game wins and losses  

## Rules  
1. Select a board (3*4 to 5*6)  
2. Two players can take turns putting gem in each cell  
3. However, if each cell has more stones than the adjacent side, the rule of "overflow" changes the stone in that cell and the surrounding "neighbor".
- Corners: Overflow at 2 gems.
- Edges: Overflow at 3 gems.
- Middle cells: Overflow at 4 gems.
4. Overflow Occurrence Rules
The corresponding gem is distributed to the adjacent side. "At this point, the color gem that was previously occupied is added. If overflow occurs again after distribution, the same thing happens again.  
5. If there is only one color left on the board, the player of the gem wins  

## Sequence  
Each cell on the board must undergo continuous validation, as a single overflow can trigger changes in adjacent cells, potentially causing further overflows.  
Therefore, ongoing validation is essential. However, by implementing a preprocessing method to identify potential changes in advance,   
we significantly reduced the overall time complexity.  

### Bot logic  
Although the bot may appear to place gems randomly, this is not the case.  
Once an overflow occurs, the bot analyzes the number of stones at each location and predicts potential overflows,  
strategically placing gems in areas that minimize further changes. In other words, the bot operates at a very high difficulty level.  

### structure 
Queue and deque functionalities effiently handle cells

## Execution  

1. **Clone the Repo**:
   ```bash
   git clone <https://github.com/daeuk23/Overflow_gem_game.git>
   ```  

2. **Make sure current version is activated**
   ```bash
   python --version
   ```   

3. **Install requirements**
   ```bash
   pip install -r game.py
   ```  

4. **Execution**
   ```bash
   python game.py
   ```  
insert in terminal  

All of these sources are copyrighted to contributers.
