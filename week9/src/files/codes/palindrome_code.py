def is_palindrome(s):
  s = ''.join(c for c in s if c.isalnum()).lower()
  return s == s[::-1]

print(is_palindrome('madam'))  # True
print(is_palindrome('hello'))  # False