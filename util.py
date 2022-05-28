def format_bytes(bytes_obj):
    return ''.join('\\x{:02x}'.format(b) for b in bytes_obj)