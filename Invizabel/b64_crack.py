import base64
import sys

#tool
def b64_crack():
    value = input("Enter value:\n").encode()

    if value == b"":
        print("Please enter something. Shutting down.")
        sys.exit()

    if value != b"":
        for i in range(1000000):
                try:
                        value = base64.b64decode(value)

                except:
                        clean = str(value).replace("b'", "")
                        clean = clean.replace("'", "")
                        print(clean)
                        print("attempts: " + str(i))
                        break
