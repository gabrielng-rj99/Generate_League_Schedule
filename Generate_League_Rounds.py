''' To Generate a Random League Schedule     # Rules                

1 - All teams face each other only twice (or any other number, its a input)
home (and away if its the case), in rounds analogous to the first half.
 
2 - A team must not play twice in the same round.

3 - A team must not play 3 times in a row at home or away either.

4 - To create a code that works for any number of teams >2, but due to the
    physical constraints, it is impossible to have an infinite number of teams,
    an athlete has a limited number of games with intensity per season.

5 - The schedule should be "random", (like a Draw) meaning that for each
    execution, a new, different, etc. schedule should be generated (random).]

6 - To Use this u will need a input that by now is a txt_file that in each line
    will have the name of each team that will be broken if a line is empty.
    so:         
    The Teams characters must be letters, nums (accent is allowed) or hifen (-)
    
    Correct:                    Wrong:

    Arsenal                     Arsenal
    Liverpool                   
    Manchester City             Liver_pool
    Newcastle-UTD
    Totteham                    MC
    Atlético98
    76ers                       NC_UTD
    
    '''

turns = 2

def SHIFTS(turns):
    if turns >= 2:
        return 2
    else:
        return 1
SHIFTS = SHIFTS(turns)

possible_chars = {
    '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', ' ', 'ç', 'Ç', 
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
    'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
    'Á', 'Â', 'Ã', 'À', 'Ä', 'á', 'â', 'ã', 'à', 'ä',
    'É', 'Ê', 'Ẽ', 'È', 'Ë', 'é', 'ê', 'ẽ', 'è', 'ë',
    'Í', 'Î', 'Ĩ', 'Ì', 'Ï', 'í', 'î', 'ĩ', 'ì', 'ï',
    'Ó', 'Ô', 'Õ', 'Ò', 'Ö', 'ó', 'ô', 'õ', 'ò', 'ö',
    'Ú', 'Û', 'Ũ', 'Ù', 'Ü', 'ú', 'û', 'ũ', 'ù', 'ü',
}

# __________________________________________________________________________
# Teams List
from tkinter import Tk, filedialog

def Teams():
    Teams = []

    root = Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(filetypes=[('Text Files', '*.txt')])
    
    if file_path:
        Teams_txt = open(file_path, mode='r+', encoding='UTF-8')
    
    for team in Teams_txt:    
        if team == '\n':
            break

            
        Teams += [team[:-1]]

    Teams_txt.close()

    for team in Teams:
        for char in team:
            if char not in possible_chars:
                raise ValueError("Teams must be alphanumeric or hifen (-)")

    if len(Teams)<=2:
        raise IndexError("The number of teams must be greater than 2")

    if len(Teams)%2 != 0:
        Teams += ["__Null__"]

    return Teams

# __________________________________________________________________________
## Creating all possible games for future check
def all_games(TEAMS, away=False):
    all_games_possibilities = []

    for i in range(len(TEAMS)):
        for j in range(i+1, len(TEAMS)):
            game_home = (TEAMS[i], TEAMS[j])
            all_games_possibilities += [game_home]
            if away:
                game_away = (TEAMS[j], TEAMS[i])
                all_games_possibilities += [game_away]

    return all_games_possibilities

# __________________________________________________________________________
# To Generate Table and First Round
def teams_rd(round):                    # Team list that played in the round
    teams_list = []
    
    for game in round:
        teams_list += [game[0], game[1]]

    teams_list = teams_list[2:]

    return teams_list

def Table_0(TEAMS_QTY):                 # Table that all games are "0x0"
    Table_0 = list(range(TEAMS_QTY-1))
    
    for i in range(TEAMS_QTY-1):
        Table_0[i] = [f"Rodada {i+1:02}"]
        Table_0[i] += [[0,0]]*(TEAMS_QTY//2)

    return Table_0

def Round_1(Table, TEAMS):              # Change the First Round
    TEAMS_QTY = len(TEAMS)
    g = 1  # Game Counter
    all_games_P = all_games(TEAMS) # [P]ossibility

    for team in TEAMS:
        round_teams = teams_rd(Table[0])
        if team in round_teams:
            continue
        else:
            for game in all_games_P:
                team1 = game[0]
                team2 = game[1]

                if team in game:
                    if team1 not in round_teams and team2 not in round_teams:
                        Table[0][g] = game
                        round_teams = teams_rd(Table[0])
                        g = (g % (TEAMS_QTY//2) ) + 1
                        continue
                
        continue

# __________________________________________________________________________
# To Generate teams Rotation
def teams_home(Round):
    teams_home = []
    
    for game in Round[1:]:
        teams_home += [game[0]]
    return teams_home

def teams_away(Round):
    teams_away = []
    
    for game in Round[1:]:
        teams_away += [game[1]]
    
    return teams_away
    
def rotation(home_teams, away_teams):

    axys = home_teams[0]

    AT_1st  = away_teams[0]         # First  [A]way [T]eam
    HT_2nd  = home_teams[1]         # Second [H]ome [T]eam
    HT_last = home_teams[-1]        # Last   [H]ome [T]eam

    new_home_teams = [axys] + [AT_1st] + [HT_2nd] + home_teams[2:-1]
    new_away_teams = away_teams[1:] + [HT_last]

    return new_home_teams, new_away_teams

# __________________________________________________________________________
# To Generate Next Rounds
def all_Rounds(Table, TEAMS):

    rd = 1  # Round Counter
    g = 1   # Game Counter
    TEAMS_QTY = len(TEAMS)


    while rd < TEAMS_QTY-1:

        Round = Table[rd][1:]
        
        home_teams = teams_home(Table[rd-1])
        away_teams = teams_away(Table[rd-1])

        new_home_teams = rotation(home_teams, away_teams)[0]
        new_away_teams = rotation(home_teams, away_teams)[1]

        for game in Round:
            game = (new_home_teams[g-1], new_away_teams[g-1])

            Table[rd][g] = game  
            
            g = (g % (TEAMS_QTY//2) ) + 1


        rd += 1

def mirror_Rounds(Table, TEAMS):

    TEAMS_QTY = len(TEAMS)
    newTable = Table_0(TEAMS_QTY)    

    rd = 0  # Round Counter
    g = 1   # Game Counter

    while rd < TEAMS_QTY-1:

        newTable[rd][0] = f"Rodada {rd+TEAMS_QTY}"
        Round = Table[rd][1:]

        for game in Round:                       
            newTable[rd][g] = tuple(reversed(game))            
            g = (g % (TEAMS_QTY//2) ) + 1


        rd += 1

    return newTable

# __________________________________________________________________________      
# Suffle and Fix (Rule 3) Functions
import random

def shuffle_teams(TEAMS):           # Shuffle teams
    random.shuffle(TEAMS)

def shuffle_single_round(Round):    # Shuffle games in single round
    round_games = Round[1:]
    random.shuffle(round_games)
    Round = [Round[0]]+round_games
    return Round

def shuffle_all_rounds(Table):      # Shuffle games around the rounds in TB
    for rd in range(len(Table)):
        Table[rd] = shuffle_single_round(Table[rd])

def fix_rule_3(Table, TEAMS):
    TEAMS_QTY = len(TEAMS)
    checklist = []

    for rd in range(1, TEAMS_QTY-1):
        g = 1
        if rd%2 == 1:
            for game in Table[rd][1:]:
                Table[rd][g] = (game[1], game[0])
                g = (g % (TEAMS_QTY//2) ) + 1

    for rd in range(1,TEAMS_QTY-2):

        previous_home_teams = teams_home(Table[rd-1])
        previous_away_teams = teams_away(Table[rd-1])

        home_teams = teams_home(Table[rd])
        away_teams = teams_away(Table[rd])

        next_home_teams = teams_home(Table[rd+1])
        next_away_teams = teams_away(Table[rd+1])



        for team in home_teams:
            if team in previous_home_teams and team in home_teams and team in next_home_teams:
                checklist += [(team, rd)]
        
        for team in away_teams:
            if team in previous_away_teams and team in away_teams and team in next_away_teams:
                checklist += [(team, rd)]

    #print(checklist)
    if checklist:
        return False
    else:
        return True

def fix_new_rounds_nums(newTable, rd):
    i = 0
    for round in newTable:
        rd += 1
        newTable[i][0] = f'Rodada {rd:02}'
        i += 1

# __________________________________________________________________________
## Checking/Verification Functions
def check_games_possibilities(TEAMS):
    teams_appearences = []
    all_games_P = all_games(TEAMS)  # [P]ossibilities

    for team in TEAMS:
        appears = 0
        for game in all_games_P:
            if team in game:
                appears += 1

        teams_appearences += [(team, appears)]

    # print(len(teams_appearences))

    # for check in teams_appearences:
    #     print(check)

    for i in range(len(teams_appearences)):
        if teams_appearences[i][1] != len(TEAMS)-1:
            return False
        
    return True

def check_game_number_each_team(Table, TEAMS, SHIFTS):   # Show if each team played
    flag = True                             # correct number of games
    TEAMS_QTY = len(TEAMS)
    for team in TEAMS:
        counter = 0

        if team == "R" or team=="o": # For "A", "B", "C",[...],"R",[...] scenario
            counter = (TEAMS_QTY-1)*-SHIFTS

        for Round in Table:
            for game in Round:
                if team in game:
                    counter += 1
        
        #print(team, counter)

        if counter != (TEAMS_QTY-1)*SHIFTS:
            flag = False
            break

    return flag

def check_IAGWP(Table, TEAMS):                  # [I]f [A]ll [G]ames [W]ere [P]layed	
    all_games_P = all_games(TEAMS)
    
    for Round in Table:
        for game in Round:
            game_back = tuple(reversed(game)) 

            if game in all_games_P:
                all_games_P.remove(game)

            elif game_back in all_games_P:
                all_games_P.remove(game_back)

        # print(len(all_games_P))

    if all_games_P:
        return False
    
    if not all_games_P:
        return True

def all_checks(Table, TEAMS, SHIFTS):
    chk_GP    = check_games_possibilities(TEAMS)
    chk_GNET  = check_game_number_each_team(Table, TEAMS, SHIFTS)
    chk_IAGWP = check_IAGWP(Table, TEAMS)

    return all([chk_GP, chk_GNET, chk_IAGWP])

# __________________________________________________________________________
## Print Table
def print_table(Table):                     # Show Games Schedule    
    print()
    for Round in Table:
        print (Round[0])
        for game in Round[1:]:
            if "__Null__" in game:
                continue

            print (f"{game[0]} vs {game[1]}")

        print()

# __________________________________________________________________________
# Main code Execution
import copy
def main():

    TEAMS = Teams()                         # Teams now is a Python List

    shuffle_teams(TEAMS)                    # Shuffle Teams (1st shuffle)

    Table = Table_0(len(TEAMS))             # To Generate Zeros Table

    Round_1(Table, TEAMS)                   # To Generate 1st Round

    all_Rounds(Table, TEAMS)                # To Generate all Rounds

    shuffle_all_rounds(Table)               # Shuffle all game Rounds (2nd shuffle)

    is_fixed = fix_rule_3(Table, TEAMS)     # Fix Home/Away Games (Rule 3)

    if SHIFTS >= 2:
        Table += mirror_Rounds(Table, TEAMS)    # To add the mirror Rounds

    all_checked = all_checks(Table, TEAMS, SHIFTS)

    if turns >= 3:
        rd = 38
        
        for turn in range(2, turns):
            if turn % 2 == 0:
                newTempTable = copy.deepcopy(Table[0:19])
                fix_new_rounds_nums(newTempTable, rd)
                Table += newTempTable

            else:
                newTempTable = copy.deepcopy(Table[19:38])
                fix_new_rounds_nums(newTempTable, rd)
                Table += newTempTable
            
            rd += 19

    if all_checked and is_fixed:
        print_table(Table)                  # Show Games Schedule
    
    else:
        raise ValueError("Something is Wrong with the Table")


main()