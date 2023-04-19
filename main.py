from nomic.gpt4all import GPT4All
import sys

m = GPT4All(model="gpt4all-lora-quantized")
m.open()
print("Open")

sys.stdout.write(m.prompt("2+2", True))
sys.stdout.write(m.prompt("hi", True))



