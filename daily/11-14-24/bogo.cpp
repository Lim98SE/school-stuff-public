#include <vector>
#include <random>
#include <algorithm>
#include <iostream>
#include <ctime>
#include <string>
#include <chrono>
#include <cstdlib>
#include <locale>
#include <iomanip>
#include <thread> 
#include <future>

struct comma_out : std::numpunct<char>
{
    char do_thousands_sep()   const { return ','; }  // separate with spaces
    std::string do_grouping() const { return "\3"; } // groups of 3 digit
};

std::vector<int> array = {};

int check_sorted(std::vector<int> arr) {
    for (int i = 0; i < arr.size(); i++) {
        if (i == 0) {
            continue;
        }

        if (arr[i] < arr[i - 1]) {
            return i;
        }
    }

    return -1;
}

auto rng = std::default_random_engine {};

int bogosort(std::vector<int> arr) {
    std::shuffle(std::begin(arr), std::end(arr), rng);
    return check_sorted(arr);
}

int run_thread(std::vector<int> arr) {
    auto future = std::async(bogosort, arr);
    return future.get();
}

int max(std::vector<int> arr) {
    int max_found = -100;

    for (auto i: arr) {
        if (i > max_found) {
            max_found = i;
        }
    }

    return max_found;
}

int run_all_threads(std::vector<int> arr) {
    std::vector<int> results;

    for (int i = 0; i < 16; i++) {
        results.push_back(run_thread(arr));
    }

    return max(results);
}

int run_bogosort(std::vector<int> arr) {
    int iterations = 0;
    int sorted = 0;
    rng.seed(time(NULL));
    std::shuffle(std::begin(array), std::end(array), rng);

    int best = 0;

    while (sorted != -1) {
        sorted = bogosort(arr);

        if (sorted > best) {
            std::cout << "New best: " << best << std::endl;
            best = sorted;
        }

        iterations++;
    }

    return iterations;
}

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::cout << "Supply one argument for number of items to sort.\n";
        return -1;
    }

    std::cout.imbue(std::locale(std::cout.getloc(), new comma_out));

    int items = std::atoi(argv[1]);

    std::cout << "Sorting " << items << " items\n";

    for (int i = 0; i < items; i++) {
        array.push_back(i);
    }

    auto start = std::chrono::high_resolution_clock::now();

    int iterations = run_bogosort(array);

    auto finish = std::chrono::high_resolution_clock::now();

    auto mills = std::chrono::duration_cast<std::chrono::microseconds>(finish-start).count() / 1000;

    std::cout << "\a";
    
    std::cout << "Sort finished!\n";

    std::cout << "Time taken to sort (milliseconds): " << mills << std::endl << iterations << " loops taken\n";

    std::cout << "Iterations/ms: " << iterations / mills << std::endl;
}