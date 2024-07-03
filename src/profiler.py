import platform
from time import perf_counter
from typing import Any, Callable, Dict, List

if platform.system() == "Linux":
    try:
        from hwcounter import count, count_end
    except ImportError:
        print(
            "hwcounter package not found. Please install it to use the profiler on Linux."
        )
        exit(1)


# Class Decorator
class profiler:
    def __enter__(self):
        self.start_time = perf_counter()
        if platform.system() == "Linux":
            self.start_cycles = count()
        return self

    def __exit__(self, type, value, traceback):
        self.total_time = perf_counter() - self.start_time
        if platform.system() == "Linux":
            self.total_cycles = count_end() - self.start_cycles


def profile_functions(
    functions: Dict[str, Callable], test_elements: List[Any], n_times: int = 500000
):
    print(f"Running {n_times} times for performance comparison...")
    for name, func in functions.items():
        print(f"\n{name}:")
        if platform.system() == "Linux":
            mean_cycles = 0
        mean_time = 0
        for _ in range(n_times):
            with profiler() as p:
                for element in test_elements:
                    func(element)
            mean_time += p.total_time
            if platform.system() == "Linux":
                mean_cycles += p.total_cycles
        mean_time /= n_times
        print(f"\tMean time: {mean_time}")
        if platform.system() == "Linux":
            mean_cycles /= n_times
            print(f"\tMean cycles: {mean_cycles}")
