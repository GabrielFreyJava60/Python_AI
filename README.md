# HW #27 Definition

## Write all methods with TODO comments of the class LfuDictCache

### Notes:
- LFU stands for Least Frequent Used with meaning of deleting Least Frequent Used association
- In the case of equaled frequency the least recent used key-value association should be deleted
- consider using DictCache class (see main.py file)
- consider using SortedDict class from sortedcontainers package

### Make sure that all tests from test_lfu_dict_cache passed

## Implementation Details

### LFU Cache Algorithm
- **Frequency tracking**: Each key has an access frequency counter
- **Frequency lists**: Keys grouped by frequency for efficient eviction
- **LRU tie-breaking**: When frequencies are equal, least recently used key is evicted
- **O(1) operations**: get, put, and eviction operations

### Key Features
- ✅ **LFU eviction** - removes least frequently used items
- ✅ **LRU tie-breaking** - handles equal frequency cases
- ✅ **O(1) complexity** for get and put operations
- ✅ **Capacity management** - maintains fixed size cache
- ✅ **Comprehensive testing** - 10 test cases covering all scenarios

### Algorithm
1. **get(key)**: Returns value and updates frequency - O(1)
2. **put(key, value)**: Stores value and updates frequency - O(1)
3. **Eviction**: Removes least frequent (or least recent if tied) item - O(1)

## Files
- `main.py` - implementation of LfuDictCache and DictCache classes
- `test_lfu_dict_cache.py` - comprehensive test suite (10 tests)
- `demo_lfu.py` - demonstration script showing LFU behavior