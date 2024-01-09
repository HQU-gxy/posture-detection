def to_hex(bs: bytes) -> list[str]:
  l = list(map(hex, bs))
  return l
