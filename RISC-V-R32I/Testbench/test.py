def to_unsigned_32bit(value):
    """
    Convert a signed 32-bit integer to its unsigned equivalent.

    Parameters:
    - value (int): The signed 32-bit integer.

    Returns:
    - int: The unsigned 32-bit integer.
    """
    bit_width = 32
    # Mask the value to fit within 32 bits
    mask = (1 << bit_width) - 1
    return value & mask

# Example usage:
signed_values = [0, -3, 0xFFFFFFF4, -2147483648]  # Example signed 32-bit values
unsigned_values = [to_unsigned_32bit(value) for value in signed_values]

for signed, unsigned in zip(signed_values, unsigned_values):
    print(f"Signed: {signed} -> Unsigned: {unsigned}")

# Output will be the unsigned values of the provided 32-bit signed integers
