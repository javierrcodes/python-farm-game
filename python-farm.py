import random 

# Initialize game variables
game_vars = {
    'day': 1,
    'energy': 10,
    'money': 20,
    'bag': {},
}
farmer_row = 2
farmer_col = 2
seed_list = ['LET', 'POT', 'CAU']

# Define seed properties
seeds = {
    'LET': {'name': 'Lettuce', 'price': 2, 'growth_time': 2, 'crop_price': 3},
    'POT': {'name': 'Potato', 'price': 3, 'growth_time': 3, 'crop_price': 6},
    'CAU': {'name': 'Cauliflower', 'price': 5, 'growth_time': 6, 'crop_price': 14},
}
base_prices = {
    'LET': 3,  # Lettuce base price
    'POT': 6,  # Potato base price
    'CAU': 14  # Cauliflower base price
}
# Initialize farm grid
farm = [[None, None, None, None, None],
        [None, None, None, None, None],
        [None, None, 'House', None, None],
        [None, None, None, None, None],
        [None, None, None, None, None]]


# Display the main menu and return the player's choice.
def display_main_menu():
    print("--------------------------------------------------------")
    print("Welcome to Sundrop Farm!")
    print()
    print("You took out a loan to buy a small farm in Albatross Town.")
    print("You have 20 days to pay off your debt of $100.")
    print("You might even be able to make a little profit.")
    print("How successful will you be?")
    print("--------------------------------------------------------")
    print("1) Start a new game")
    print("2) Load your saved game")
    print()
    print("0) Exit Game")
    choice = input("Your choice? ")
    print()
    return choice


#Display the player's current stats including day, energy, money, and seeds.
def show_stats(game_vars):
    print("+----------------------------------------------------+")
    if game_vars['energy'] <0:
        game_vars['energy'] = 0
    print(f"| Day {game_vars['day']:<7} Energy: {game_vars['energy']:<6} Money: ${game_vars['money']:<16}|")
    if not game_vars['bag'] or all(count == 0 for count in game_vars['bag'].values()):
        print(f"|{' ':2}{"You Have No Seeds.":50}|")
    else:
        print(f"|{' ':2}{"Your Seeds":50}|")
        for seed, count in game_vars['bag'].items():
            if count > 0:  # Only print if count is greater than 0
                print(f"|{' ':5}{seeds[seed]['name'] + ":":15}{count:<32}|")
    print("+----------------------------------------------------+")
    

# Handle the in-town menu options and actions. #This function will be called when the player is in town.
def in_town(game_vars):
    while True:
        show_stats(game_vars)
        print("You are in Albatross Town")
        print("-------------------------")
        print("1) Visit Shop")
        print("2) Visit Farm")
        print("3) End Day")
        print()
        print("9) Save Game")
        print("0) Exit Game")
        print("-------------------------")
        choice = input("Your choice? ")
        print()
        try:
            if choice == '1':
                in_shop(game_vars)
            elif choice == '2':
                in_farm(game_vars, farm)
            elif choice == '3':
                if not end_day(game_vars, farm):  # Check if game ends after ending the day
                    break  # Exit if the game has ended
            elif choice == '9':
                save_game(game_vars, farm)
            elif choice == '0':
                print("Exiting game...")
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid Input")


#Handle the in-shop menu options and actions. #This function will be called when the player is in the shop.
def in_shop(game_vars):
    while True:
        print("Welcome to Pierce's Seed Shop!")
        show_stats(game_vars)
        print("What do you wish to buy?")
        print(f"{'Seed':16} {'Price':7} {'Days to Grow':14} {'Crop Price'}")
        print("--------------------------------------------------") 
        for i in range(len(seed_list)):
            seed = seed_list[i]
            print(f"{i+1}) {seeds[seed]['name']:13} {seeds[seed]['price']:^6} {seeds[seed]['growth_time']:^14} {seeds[seed]['crop_price']:^12}")
        print()
        print("0) Leave")
        print("--------------------------------------------------") 

        choice = input("Your choice? ")
        print()
        if choice == '0':
            break
        elif choice in [str(i+1) for i in range(len(seed_list))]:
            seed = seed_list[int(choice)-1]
            price = seeds[seed]['price']
            max_quantity = game_vars['money'] // price
            
            if max_quantity > 0:
                try:
                    quantity = int(input(f"How many {seeds[seed]['name']} seeds would you like to buy? (Max {max_quantity}): "))
                    print()
                    if quantity < 1 or quantity > max_quantity:
                        print(f"Invalid quantity. You can only buy between 1 and {max_quantity} seeds.")
                        print()
                        continue
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    print()
                    continue

                current_total_seeds = sum(game_vars['bag'].values())
                if current_total_seeds + quantity > 10:
                    print("You cannot carry more than 10 seeds in total.")
                    print()
                    continue

                total_cost = price * quantity
                game_vars['money'] -= total_cost
                if seed in game_vars['bag']:
                    game_vars['bag'][seed] += quantity
                else:
                    game_vars['bag'][seed] = quantity
                print(f"You bought {quantity} {seeds[seed]['name']} seeds for ${total_cost}.")
                print()
            else:
                print("You don't have enough money.")
                print()
        else:
            print("Invalid choice. Please try again.")
            print()


#Draw the farm grid and display the farmer's position, seeds, and growth time.
def draw_farm(farm, farmer_row, farmer_col):
    for col in range(len(farm[0])):
        # Print top border
        for row in range(len(farm)):
            print("+-----", end="")
        print("+")

        # Print seed initials or house (if any) or space
        for row in range(len(farm)):
            if farm[row][col] == "House":
                print("| HSE ", end="")
            elif farm[row][col] is None:
                print("|     ", end="")
            elif isinstance(farm[row][col], dict):
                print(f"| {farm[row][col]['seed']} ", end="")
        print("|")

        # Print farmer position or space
        for row in range(len(farm)):
            if col == farmer_col and row == farmer_row:
                print("|  X  ", end="")
            else:
                print("|     ", end="")
        print("|")

        # Print bottom row for growth time or empty space
        for row in range(len(farm)):
            if farm[row][col] is None:
                print("|     ", end="")
            elif isinstance(farm[row][col], dict):
                print(f"|  {farm[row][col]['time']:<2} ", end="")
            elif farm[row][col] == "House":
                print("|     ", end="")
        print("|")

    # Print bottom border
    for row in range(len(farm)):
        print("+-----", end="")
    print("+")


 #Handle the in-farm menu options and actions. #This function will be called when the player is on the farm.
def in_farm(game_vars, farm):
    # Implement farm functionality here
    farmer_row, farmer_col = 2, 2
    while True:
        current_position = farm[farmer_row][farmer_col]
        can_harvest = current_position and 'time' in current_position and current_position['time'] == 0
        can_plant = not farm[farmer_row][farmer_col] and any(count > 0 for count in game_vars['bag'].values())

        # Draw Farm and show available options
        draw_farm(farm, farmer_row, farmer_col)
        print(f"Energy: {game_vars['energy']}")
        print("[WASD] Move ")
        if can_plant:
            print("P)lant Seed")
        if can_harvest:
            print("H)arvest")
        print("R)eturn to Town")
        
        # Check if the player is too tired to continue
        if game_vars['energy'] <= 0:
            print("You're too tired. You should get back to town.")
            action = input("Your choice? ").upper()
            if action == 'R':
                break
            else:
                print("You can't do that. You have to return to town.")
                continue

        action = input("Your choice? ").upper()

        # Handle movement of the farmer on the farm grid.
        if action in ['W', 'A', 'S', 'D']:
            if action == 'W' and farmer_col > 0:	
                farmer_col -= 1
            elif action == 'A' and farmer_row > 0:
                farmer_row -= 1
            elif action == 'S' and farmer_col < len(farm[0]) - 1:
                farmer_col += 1
            elif action == 'D' and farmer_row < len(farm) - 1:
                farmer_row += 1
            else:
                print("You can't move off the grid!")
                
            game_vars['energy'] -= 1

        #Handle the planting of seeds on the farm.
        elif action == 'P' and can_plant:
            if not any(count > 0 for count in game_vars['bag'].values()):
                print("You do not have any seeds to plant!")
            elif farm[farmer_row][farmer_col] is not None:
                print("The current square is already occupied!")
            else:
                available_seeds = [(seed, seeds[seed]) for seed in seed_list if game_vars['bag'].get(seed, 0) > 0]
                
                if not available_seeds:
                    print("You do not have any seeds to plant!")
                else:
                    print("What do you wish to plant?")
                    print("-----------------------------------------------------")
                    print(f"{'Seed':^9}{'Days to Grow':^19} {'Crop Price':^12} {'Available':^12}")
                    print("-----------------------------------------------------")
                    
                    for index, (seed, seed_info) in enumerate(available_seeds, start=1):
                        count = game_vars['bag'][seed]
                        print(f"{index}) {seed_info['name']:<15} {seed_info['growth_time']:<15} {seed_info['crop_price']:<15} {count}")
                    
                    print()
                    print("0) Leave")
                    print("-----------------------------------------------------")

                    # Plant the selected seed
                    try:
                        seed_choice = int(input("Your choice? "))
                        if seed_choice != 0 and 1 <= seed_choice <= len(available_seeds):
                            seed_key = available_seeds[seed_choice - 1][0]
                            if game_vars['bag'][seed_key] > 0:
                                game_vars['bag'][seed_key] -= 1
                                if game_vars['bag'][seed_key] == 0:  # Check if the bag is empty after planting
                                    print("You have used the last of your seeds.")
                                farm[farmer_row][farmer_col] = {'seed': seed_key, 'time': seeds[seed_key]['growth_time']}
                                game_vars['energy'] -= 1
                                if game_vars['energy'] <= 0:
                                    print("You're too tired. You should get back to town.")
                        else:
                            print("Invalid choice. Please try again.")
                    except ValueError:
                        print("Invalid input. Please enter a number.")

        # Handle the harvesting of crops from the farm.
        elif action == 'H' and can_harvest:
            if current_position and 'time' in current_position:
                if current_position['time'] == 0:
                    crop_type = current_position['seed']
                    game_vars['money'] += seeds[crop_type]['crop_price']
                    farm[farmer_row][farmer_col] = None
                    game_vars['energy'] -= 1
                    print(f"You harvest the {seeds[crop_type]['name']} and sold it for ${seeds[crop_type]['crop_price']}!")
                    print(f"You now have ${game_vars['money']}!")

        elif action == 'R':
            break
        
        else:
            print("Invalid action.")


#Handle the end of the day, updating crop prices, and checking for game end conditions.
def end_day(game_vars, farm):
    if game_vars["day"] >= 20:
        if game_vars["money"] >= 100:
            print(f"You paid off your debt of $100 and made a profit of ${game_vars['money'] - 100}.")
            print("You win!")
            print()
        else:
            print("You didn't make enough money to pay off your debt!")
            print("You lose!")
            print()
        return False  # End the game

    # Proceed with day transition
    game_vars['day'] += 1
    game_vars['energy'] = 10  # Reset energy for the new day
    print(f"Ending day {game_vars['day'] - 1}. Moving to day {game_vars['day']}...")

    # The crop price for each seed on a particular day is randomly determined from +2 to -2 of the base price.
    # Update crop prices 
    daily_prices = {}
    for seed in seed_list:
        base_price = base_prices[seed]  # Get the constant base price
        adjustment = random.randint(-2, 2)
        new_price = base_price + adjustment
        
        # Apply specific constraints based on the seed type
        if seed == 'LET':  # Lettuce
            new_price = max(1, min(new_price, 5))  # Price between 1 and 5
        elif seed == 'POT':  # Potato
            new_price = max(4, min(new_price, 8))  # Price between 4 and 8
        elif seed == 'CAU':  # Cauliflower
            new_price = max(12, min(new_price, 16))  # Price between 12 and 16
        
        daily_prices[seed] = new_price
        seeds[seed]['crop_price'] = new_price  # Update daily crop price in seeds

    # Update crops on the farm
    for row in range(len(farm)):
        for col in range(len(farm[0])):
            if farm[row][col] and 'time' in farm[row][col]:
                farm[row][col]['time'] -= 1
                if farm[row][col]['time'] < 0:
                    farm[row][col]['time'] = 0
                if farm[row][col]['time'] == 0:
                    print(f"The crop at ({row}, {col}) is ready to harvest!")

    return True  # Continue the game


# Reset the game variables to their initial state.
def reset_game():
    global game_vars, farm
    game_vars = {
        'day': 1,
        'energy': 10,
        'money': 20,
        'bag': {},
    }
    farm = [[None, None, None, None, None],
            [None, None, None, None, None],
            [None, None, 'House', None, None],
            [None, None, None, None, None],
            [None, None, None, None, None]]
    

# Save the game to a file
def save_game(game_vars, farm):
    try:
        with open("savegame.txt", "w") as f:
            # Save day, energy, and money
            f.write(f"{game_vars['day']},{game_vars['energy']},{game_vars['money']}\n")

            # Save seed bag
            for seed, count in game_vars['bag'].items():
                f.write(f"{seed}:{count}\n")
            f.write("\n")  # Separate seed data from farm data

            # Save farm state
            for row in farm:
                row_data = []
                for cell in row:
                    if cell == None:
                        row_data.append("None")
                    elif cell == "House":
                        row_data.append("HSE")
                    elif isinstance(cell, dict) and 'seed' in cell and 'time' in cell:
                        row_data.append(f"{cell['seed']}:{cell['time']}")
                    else:
                        row_data.append("None")
                f.write(",".join(row_data) + "\n")
        print("Game Saved Successfully!")
        print()
    
    except Exception as e:
        print(f"An error occurred while saving the game: {e}")


# Load the game from a saved file
def load_game(game_vars, farm):
    try:
        with open("savegame.txt", "r") as f:
            # Read the first line for day, energy, and money
            first_line = f.readline().strip()
            if not first_line:
                raise ValueError("Save file is empty.")
            day, energy, money = map(int, first_line.split(','))
            game_vars['day'] = day
            game_vars['energy'] = energy
            game_vars['money'] = money

            # Read the seeds in the bag
            game_vars['bag'] = {}
            while True:
                line = f.readline().strip()
                if not line or ',' in line:  # End of seed section or start of farm section
                    break
                try:
                    seed, count = line.split(':')
                    game_vars['bag'][seed] = int(count)
                except ValueError:
                    print(f"Skipping invalid seed data: {line}")
                    continue

            # Read the farm state
            for row in range(len(farm)):
                line = f.readline().strip()
                if not line:
                    raise ValueError("Farm state line is empty or missing.")
                cells = line.split(',')
                if len(cells) != len(farm[0]):
                    raise ValueError(f"Farm row length {len(cells)} does not match expected length {len(farm[0])}.")
                for col in range(len(farm[0])):
                    cell = cells[col]
                    if cell == 'None':
                        farm[row][col] = None
                    elif cell == 'HSE':
                        farm[row][col] = 'House'
                    elif ':' in cell:
                        seed, time = cell.split(':')
                        try:
                            farm[row][col] = {'seed': seed, 'time': int(time)}
                        except ValueError:
                            print(f"Skipping invalid farm data: {cell}")
                            farm[row][col] = None
                    else:
                        print(f"Unexpected farm data: {cell}")
                        farm[row][col] = None

        print("Game loaded successfully!")
        print()
    except FileNotFoundError: # Handle file not found error
        print("Save file not found.")
        print("Starting New Game...")
    except ValueError as e: # Handle invalid data in the save file
        print(f"Error in save file format: {e}")
    except Exception as e: # Handle other exceptions
        print(f"An error occurred while loading the game: {e}")


# Main game loop
# Display the main menu and handle the player's choice.
def main():
    while True:
        choice = display_main_menu()
        try:
            if choice == '1':
                reset_game()
                in_town(game_vars)
            elif choice == '2':
                # Implement loading game functionality here
                print("Loading a saved game...")
                load_game(game_vars,farm)
                in_town(game_vars)
            elif choice == '0':
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid Input.")

main()