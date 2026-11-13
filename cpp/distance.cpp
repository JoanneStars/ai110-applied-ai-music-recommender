#include <cmath>
#include <cstddef>
#include <limits>

// Stable C ABI allows Python's ctypes to call C++ without third-party bindings.
#if defined(_WIN32)
#define VM_EXPORT extern "C" __declspec(dllexport)
#else
#define VM_EXPORT extern "C" __attribute__((visibility("default")))
#endif

VM_EXPORT double vm_euclidean_distance(const double* left,
                                       const double* right,
                                       std::size_t count) {
    if (!left || !right || count == 0) {
        return std::numeric_limits<double>::quiet_NaN();
    }
    double sum = 0.0;
    for (std::size_t index = 0; index < count; ++index) {
        if (!std::isfinite(left[index]) || !std::isfinite(right[index])) {
            return std::numeric_limits<double>::quiet_NaN();
        }
        const double difference = left[index] - right[index];
        sum += difference * difference;
    }
    return std::sqrt(sum);
}
