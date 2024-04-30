import random

class CacheLine:
    def __init__(self, tag):
        self.tag = tag
        self.state = 'I'  # Initial state: Invalid

class CacheSet:
    def __init__(self, associativity):
        self.lines = [CacheLine(None) for _ in range(associativity)]
        self.associativity = associativity

class Cache:
    def __init__(self, num_sets, associativity):
        self.num_sets = num_sets
        self.sets = [CacheSet(associativity) for _ in range(num_sets)]

class Memory:
    def __init__(self, size):
        self.size = size
        self.data = [0] * size

class Processor:
    def __init__(self, pid, cache):
        self.pid = pid
        self.cache = cache

class CacheModel:
    def __init__(self, num_processors, memory_size, cache_size, num_sets, associativity):
        self.num_processors = num_processors
        self.memory = Memory(memory_size)
        self.processors = [Processor(pid, Cache(num_sets, associativity)) for pid in range(num_processors)]
        self.cache_size = cache_size
        self.event_log = []
        self.bus_access_cycles = 0
        self.bus_requests = 0
        self.bus_responses = 0

    def reset(self):
        for processor in self.processors:
            for cache_set in processor.cache.sets:
                for line in cache_set.lines:
                    line.state = 'I'
                    line.tag = None
        self.memory.data = [0] * self.memory.size
        self.event_log.clear()
        self.bus_access_cycles = 0
        self.bus_requests = 0
        self.bus_responses = 0

    def get_cache_state(self):
        return {
            'processors': [
                {
                    'pid': processor.pid,
                    'cache': {
                        'sets': [
                            {
                                'lines': [
                                    {'tag': line.tag, 'state': line.state}
                                    for line in cache_set.lines
                                ]
                            }
                            for cache_set in processor.cache.sets
                        ]
                    }
                }
                for processor in self.processors
            ],
            'memory': {
                'data': self.memory.data
            }
        }

    def read(self, processor_id, address):
        self.event_log.clear()
        processor = self.processors[processor_id]
        cache = processor.cache
        set_index = address % cache.num_sets
        tag = address // cache.num_sets
        cache_set = cache.sets[set_index]

        self.bus_access_cycles += 1
        self.bus_requests += 1

        for line in cache_set.lines:
            if line.tag == tag:
                if line.state in ['M', 'O', 'E', 'S']:
                    self.event_log.append(f"CPU{processor_id}: Read hit for address {address}")
                    self.bus_responses += 1
                    return True, self.event_log
                elif line.state == 'I':
                    line.state = 'S'
                    self.event_log.append(f"CPU{processor_id}: Read miss for address {address}, fetching from memory")
                    self.event_log.append(f"CPU{processor_id}: Setting cache line state to S")
                    self.bus_responses += 1
                    return False, self.event_log

        self.event_log.append(f"CPU{processor_id}: Read miss for address {address}, fetching from memory")
        replaced_line_index = random.randint(0, cache_set.associativity - 1)
        replaced_line = cache_set.lines[replaced_line_index]
        replaced_line.tag = tag
        replaced_line.state = 'S'
        self.event_log.append(f"CPU{processor_id}: Replacing cache line {replaced_line_index} with tag {tag}, setting state to S")
        self.bus_responses += 1
        return False, self.event_log












    def write(self, processor_id, address):
    self.event_log.clear()
    processor = self.processors[processor_id]
    cache = processor.cache
    set_index = address % cache.num_sets
    tag = address // cache.num_sets
    cache_set = cache.sets[set_index]

    self.bus_access_cycles += 1
    self.bus_requests += 1

    for line in cache_set.lines:
        if line.tag == tag:
            if line.state == 'E':  # Check if the line is in the Exclusive state
                self.event_log.append(f"CPU{processor_id}: Write hit for address {address}")
                line.state = 'M'  # Upgrade state to Modified
                self.event_log.append(f"CPU{processor_id}: Setting cache line state to M")
                self.bus_responses += 1
                return True, self.event_log
            elif line.state in ['M', 'O', 'E']:  # Also include 'E' state in the check
                self.event_log.append(f"CPU{processor_id}: Write hit for address {address}")
                line.state = 'M'
                self.event_log.append(f"CPU{processor_id}: Setting cache line state to M")
                self.bus_responses += 1
                return True, self.event_log
            elif line.state in ['I', 'S']:
                line.state = 'M'
                self.event_log.append(f"CPU{processor_id}: Write miss for address {address}, invalidating other copies")
                self.invalidate_other_copies(processor_id, address)
                self.event_log.append(f"CPU{processor_id}: Setting cache line state to M")
                self.bus_responses += 1
                return False, self.event_log

    self.event_log.append(f"CPU{processor_id}: Write miss for address {address}, fetching from memory")
    replaced_line_index = random.randint(0, cache_set.associativity - 1)
    replaced_line = cache_set.lines[replaced_line_index]
    replaced_line.tag = tag
    replaced_line.state = 'M'
    self.event_log.append(f"CPU{processor_id}: Replacing cache line {replaced_line_index} with tag {tag}, setting state to M")
    self.bus_responses += 1
    self.invalidate_other_copies(processor_id, address)
    return False, self.event_log

    












        
def invalidate_other_copies(self, processor_id, address):
    tag = address // len(self.processors[0].cache.sets)  # Calculate the tag from the address
    for other_processor in self.processors:
        if other_processor.pid != processor_id:  # Exclude the current processor
            cache = other_processor.cache
            set_index = address % cache.num_sets  # Calculate the set index from the address
            cache_set = cache.sets[set_index]
            for line in cache_set.lines:
                if line.tag == tag:  # Check if the tag matches
                    line.state = 'I'  # Set the state to 'I' (Invalid)
                    self.event_log.append(f"CPU{other_processor.pid}: Invalidating cache line with tag {tag}")
        

    def display_memory_contents(self):
        return self. memory.data
