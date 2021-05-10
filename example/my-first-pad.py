#!/usr/bin/env python
from pado.runbook import Runbook


class ExamplePrintAndDo(Runbook):
    """
    This pad is a basic example that exercises
    the various options available.
    """

    def first_step(self):
        """
        Do ABC now.
        """

    def second_step(self):
        """
        Find the name of the largest planet in our solar system. Paste it here
        """
        self.name = input("Enter a name:")
        self.value = 10

    def third_step(self, skippable=False, critical=True):
        """
        Send an email to mike.
        """
        print(f"The value from step 2 is: {self.value}")
        print(f"The name you entered in step 2 is: {self.name}")

    def last_step(self, name='the end'):
        pass


if __name__ == "__main__":
    ExamplePrintAndDo.main()
