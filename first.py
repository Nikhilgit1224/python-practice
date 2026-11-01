print("hello")

from pydantic import BaseModel


class Person(BaseModel):
	name: str
	age: int

with open("person.txt", "w") as file:
    file.write("this is a test file")