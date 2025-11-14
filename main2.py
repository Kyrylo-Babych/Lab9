import json
import os

DATA_FILE = 'teams.json'
RESULT_FILE = 'task_result.json'

def create_initial_file():
    if not os.path.exists(DATA_FILE):
        initial_data = {
            "teams": [
                {"name": "Шахтар", "score": 25},
                {"name": "Динамо", "score": 23},
                {"name": "Кривбас", "score": 20},
                {"name": "Дніпро-1", "score": 18},
                {"name": "Полісся", "score": 17},
                {"name": "Рух", "score": 15},
                {"name": "Ворскла", "score": 12},
                {"name": "Чорноморець", "score": 10},
                {"name": "ЛНЗ", "score": 8}
            ]
        }
        save_data(DATA_FILE, initial_data)
        print(f"Створено початковий файл '{DATA_FILE}' з даними.")

def load_data(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        print(f"Файл '{filename}' не знайдено.")
        if filename == DATA_FILE:
            create_initial_file()
            return load_data(filename)
        return {} 
    except json.JSONDecodeError:
        print(f"Помилка читання JSON у файлі '{filename}'. Можливо, він порожній.")
        return {"teams": []} if filename == DATA_FILE else {}

def save_data(filename, data):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"Помилка запису у файл '{filename}': {e}")

def display_data():
    data = load_data(DATA_FILE)
    teams = data.get('teams', [])
    
    if not teams:
        print("Файл даних порожній або не містить списку 'teams'.")
        return

    print(f"\n--- Поточний рейтинг команд ({DATA_FILE}) ---")
    for i, team in enumerate(teams, 1):
        print(f"{i}. {team['name']}: {team['score']} очок")
    print("----------------------------------------")

def add_record():
    name = input("Введіть назву нової команди: ")
    try:
        score = int(input("Введіть кількість очок: "))
    except ValueError:
        print("Помилка: кількість очок має бути цілим числом.")
        return

    data = load_data(DATA_FILE)
    teams_list = data.get('teams', [])
    
    if any(team['name'].lower() == name.lower() for team in teams_list):
        print(f"Помилка: Команда з назвою '{name}' вже існує.")
        return

    teams_list.append({"name": name, "score": score})
    
    teams_list.sort(key=lambda x: x['score'], reverse=True)
    
    data['teams'] = teams_list
    save_data(DATA_FILE, data)
    print(f"Команду '{name}' успішно додано.")
    display_data() 

def delete_record():
    name_to_delete = input("Введіть назву команди для видалення: ")
    
    data = load_data(DATA_FILE)
    teams_list = data.get('teams', [])
    
    new_teams_list = [
        team for team in teams_list 
        if team['name'].lower() != name_to_delete.lower()
    ]
    
    if len(new_teams_list) == len(teams_list):
        print(f"Помилка: Команду з назвою '{name_to_delete}' не знайдено.")
    else:
        data['teams'] = new_teams_list
        save_data(DATA_FILE, data)
        print(f"Команду '{name_to_delete}' успішно видалено.")
        display_data() 

def search_record():
    name_to_search = input("Введіть назву команди для пошуку: ")
    
    data = load_data(DATA_FILE)
    teams_list = data.get('teams', [])
    
    found_team = None
    place = -1
    
    for i, team in enumerate(teams_list, 1):
        if team['name'].lower() == name_to_search.lower():
            found_team = team
            place = i
            break
            
    if found_team:
        print("\n--- Результат пошуку ---")
        print(f"Місце: {place}")
        print(f"Назва: {found_team['name']}")
        print(f"Очки: {found_team['score']}")
        print("------------------------")
    else:
        print(f"Команду з назвою '{name_to_search}' не знайдено.")

def solve_variant_task():
    print("\n--- Виконання завдання варіанту ---")
    data = load_data(DATA_FILE)
    teams_list = data.get('teams', [])
    
    if not teams_list:
        print("Помилка: Базовий файл даних порожній. Завдання не може бути виконано.")
        return
        
    max_score = teams_list[0]['score']
    min_score = teams_list[-1]['score']
    
    new_team_name = input("Введіть назву 10-ї ('забутої') команди: ")
    
    try:
        new_team_score = int(input(f"Введіть кількість очок для '{new_team_name}': "))
    except ValueError:
        print("Помилка: кількість очок має бути цілим числом.")
        return

    if new_team_score >= max_score:
        print(f"Помилка: Нова команда не може бути чемпіоном (очки <= {max_score-1}).")
        return
    if new_team_score <= min_score:
        print(f"Помилка: Нова команда не може зайняти останнє місце (очки >= {min_score+1}).")
        return
    if any(team['score'] == new_team_score for team in teams_list):
         print(f"Помилка: Нова команда не може мати однакову кількість очок ні з ким.")
         return

    place = 1
    for team in teams_list:
        if team['score'] > new_team_score:
            place += 1
            
    teams_below = [
        team['name'] for team in teams_list 
        if team['score'] < new_team_score
    ]
    
    result_data = {
        "new_team_analysis": {
            "team_name": new_team_name,
            "team_score": new_team_score,
            "determined_place": place,
            "teams_with_fewer_points": teams_below
        }
    }
    
    save_data(RESULT_FILE, result_data)
    
    print("\n--- Результат виконання завдання ---")
    print(f"а) Команда '{new_team_name}' ({new_team_score} очок) посіла {place}-е місце.")
    print(f"б) Команди, які набрали менше очок: {', '.join(teams_below)}")
    print(f"\nДетальний результат збережено у файл '{RESULT_FILE}'.")

def main_menu():
    create_initial_file() 
    
    while True:
        print("\n--- Головне меню ---")
        print("1. Вивести рейтинг команд")
        print("2. Додати нову команду")
        print("3. Видалити команду")
        print("4. Пошук команди за назвою")
        print("5. додати 10-ту команду")
        print("0. Вихід")
        
        choice = input("Оберіть опцію: ")
        
        if choice == '1':
            display_data()
        elif choice == '2':
            add_record()
        elif choice == '3':
            delete_record()
        elif choice == '4':
            search_record()
        elif choice == '5':
            solve_variant_task()
        elif choice == '0':
            print("Завершення роботи.")
            break
        else:
            print("Невірний вибір. Спробуйте ще раз.")

if __name__ == "__main__":
    main_menu()