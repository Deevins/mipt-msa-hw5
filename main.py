import requests
import functools
import collections
import time
import timeit
import cProfile


# Кэширование ответа от запроса
@functools.lru_cache(maxsize=None)
def get_text(url):
    response = requests.get(url)
    return response.text


# Подсчет всех слов в тексте с использованием Counter
def count_all_words(url):
    text = get_text(url)
    # Разделяем текст по пробельным символам
    words = text.split()
    return collections.Counter(words)


# Получаем частоту нужных слов
def count_word_frequencies(url, words_list):
    counter = count_all_words(url)
    return {word: counter[word] for word in words_list}


# Функция для бенчмарка
def benchmark(url, words_list, number=10):
    # Прогрев кэша
    count_word_frequencies(url, words_list)

    # Бенчмарк с использованием time
    start_time = time.time()
    result = count_word_frequencies(url, words_list)
    duration = time.time() - start_time
    print("Результаты частот:", result)
    print("Время выполнения одного запроса (time): {:.4f} секунд".format(duration))

    # Бенчмарк с использованием timeit
    t = timeit.timeit(lambda: count_word_frequencies(url, words_list), number=number)
    print("Бенчмарк (среднее за {} запусков): {:.4f} секунд на запуск".format(number, t / number))


def main():
    words_file = "words.txt"
    url = "https://eng.mipt.ru/why-mipt/"

    # Чтение списка слов из файла
    with open(words_file, 'r') as file:
        words_list = [line.strip() for line in file if line.strip()]

    # Подсчет частот слов
    frequencies = count_word_frequencies(url, words_list)
    print("Частоты слов:", frequencies)

    print("\nПроведение бенчмарка оптимизированного решения...")
    benchmark(url, words_list, number=10)

    # Профилирование с использованием cProfile через объект Profile
    print("\nПрофилировка решения с использованием cProfile:")
    profiler = cProfile.Profile()
    profiler.enable()
    count_word_frequencies(url, words_list)
    profiler.disable()
    profiler.print_stats(sort='time')


if __name__ == "__main__":
    main()
