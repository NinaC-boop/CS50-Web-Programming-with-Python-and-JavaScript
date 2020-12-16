s = set()


s.add(1)
s.add(2)
s.add(1)
s.add(10)
s.add(3)

s.remove(2)
# each element only appears once and is unique

print(s)

print(f"The set has {len(s)} elements.")