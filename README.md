# HW #28 Definition

## Write class RandomNumbersStream with the following methods and use cases

### Methods

- `__init__(self, min: int = -10 ** 20, max: int = 10 ** 20)` - initialization for generation of endless random numbers in closed interval [min, max]
- `setFilter(self, predicate: Callable[[int], bool])` - sets predicate for filtering generated random numbers
- `setLimit(self, limit: int)` - sets limit of generated random numbers
- `setDistinct(self)` - defines the generation of unique random numbers (by default numbers may repeat)
- `resetDistinct(self)` - cancels the generation of unique random numbers (sets default)
- `__iter__(self) -> Iterator[int]` - iterates generated random numbers

### Use Cases

#### Endless Random Numbers Streaming:

```python
numbers = RandomNumbersStream(min=10, max=100)
for num in numbers:
    print(num)  # endless loop printing random numbers in the interval [10, 100]
```

#### Endless Even Random Numbers Streaming:

```python
numbers = RandomNumbersStream(min=10, max=100)
numbers.setFilter(lambda n: n % 2 == 0)
for num in numbers:
    print(num)  # endless loop printing even random numbers in the interval [10, 100]
```

#### Limited Even Random Numbers Streaming:

```python
numbers = RandomNumbersStream(min=10, max=100)
numbers.setFilter(lambda n: n % 2 == 0)
numbers.setLimit(10)
for num in numbers:
    print(num)  # printing 10 even random numbers in the interval [10, 100]
```

#### Sport Lotto:

```python
numbers = RandomNumbersStream(min=1, max=49)
numbers.setDistinct()
numbers.setLimit(10)
for num in numbers:
    print(num)  # printing 10 unique random numbers in the interval [1, 49]
```

## Files

- `main.py` - implementation of RandomNumbersStream class
- `demo_random_stream.py` - demonstration script showing RandomNumbersStream behavior
