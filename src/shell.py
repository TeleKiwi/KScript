import core

while True:
    text = input('kscript > ')
    if text == "break": break
    result, error = core.run('<stdin>', text)
    if error: print(error.as_string())
    else: print(result)