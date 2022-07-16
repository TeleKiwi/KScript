import core

while True:
    text = input('kscript > ')
    result, error = core.run(text)
    if error: print(error.as_string())
    else: print(result)