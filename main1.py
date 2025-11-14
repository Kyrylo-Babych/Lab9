import csv
import sys


INPUT_FILENAME = "API_NY.GDP.PCAP.CD_DS2_en_csv_v2_134819.csv"
OUTPUT_FILENAME = "gdp_2019_selected_countries.csv"
TARGET_YEAR = "2019"
SKIP_HEADER_ROWS = 4 


def read_and_display_data(filename: str) -> dict:
    gdp_data = {}
    
    try:
        with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            
            for _ in range(SKIP_HEADER_ROWS):
                next(reader)

            headers = next(reader)
            country_name_index = headers.index("Country Name")
            
            try:
                year_header = next(h for h in headers if h.startswith(TARGET_YEAR))
                year_index = headers.index(year_header)
            except (ValueError, StopIteration):
                raise ValueError(f"Не знайдено стовпець даних для року '{TARGET_YEAR}'")

            print(f"## Вміст файлу: {filename} (Тільки дані по {TARGET_YEAR})")
            print("-" * 50)
            
            display_count = 0
            MAX_DISPLAY_ROWS = 10

            for row in reader:
                try:
                    country = row[country_name_index]
                    gdp_value = row[year_index]
                    
                    if country and gdp_value.strip() and gdp_value.strip() != '..':
                        gdp_data[country] = gdp_value.strip()

                        if display_count < MAX_DISPLAY_ROWS:
                            print(f"{country}: {gdp_value.strip()}")
                            display_count += 1
                        elif display_count == MAX_DISPLAY_ROWS:
                            if display_count == 10:
                                print("...")
                                display_count += 1 

                except IndexError:
                    continue
            
            print("-" * 50)
            print(f"Зчитано даних про GDP за {TARGET_YEAR} для {len(gdp_data)} країн/регіонів.")

    except FileNotFoundError:
        print(f"Помилка: Файл '{filename}' не знайдено. Переконайтесь, що він знаходиться у коректній директорії.", file=sys.stderr)
    except Exception as e:
        print(f"Виникла непередбачена помилка під час обробки файлу: {e}", file=sys.stderr)

    return gdp_data

def search_and_write_data(gdp_data: dict, output_filename: str, user_input: str):
    if not gdp_data:
        print("Неможливо виконати пошук, оскільки не було зчитано жодних даних.")
        return

    countries_to_search = [c.strip() for c in user_input.split(',')]
    search_results = []

    search_results.append(["Country Name", f"GDP per capita (current US$) {TARGET_YEAR}"])
    
    found_count = 0
    print("\n## Результати пошуку даних")
    for country in countries_to_search:
        gdp_value = gdp_data.get(country) 
        
        if gdp_value:
            search_results.append([country, gdp_value])
            print(f"Знайдено: {country}: {gdp_value}")
            found_count += 1
        else:
            search_results.append([country, "N/A"])
            print(f"Не знайдено даних для країни: {country}")

    try:
        with open(output_filename, 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            writer.writerows(search_results)
            
        print("-" * 50)
        print(f"Результати пошуку ({found_count} з {len(countries_to_search)} країн) успішно збережено у файл: '{output_filename}'")
    except Exception as e:
        print(f"Помилка при записі у вихідний файл: {e}", file=sys.stderr)


if __name__ == "__main__":
    
    all_gdp_data = read_and_display_data(INPUT_FILENAME)
    
    if all_gdp_data:
        print("\n## Пошук даних за назвами країн")
        print("Введіть назви країн для пошуку, розділені комами (наприклад: Ukraine, Poland, Germany):")
        user_countries = input("> ")
        search_and_write_data(all_gdp_data, OUTPUT_FILENAME, user_countries)
    else:
        print("\nПрограма завершена, оскільки не вдалося зчитати вхідні дані.")