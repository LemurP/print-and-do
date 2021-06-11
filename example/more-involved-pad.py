#!/usr/bin/env python
import hashlib

from pado.runbook import Runbook


class ExamplePrintAndDo(Runbook):
    """
    This pad is a basic example that exercises
    the various options available.
    """
    nickname = "Uionor"

    def make_a_new_nickname(self):
        """
        Enter your nickname
        """
        nickname = input("Enter nickname [Uionor]:")
        if nickname:
            self.nickname = nickname

    def second_step(self):
        """
        Record the hash for your nickname
        """
        print(f"{hashlib.sha1(bytes(self.nickname.encode('utf-8'))).hexdigest()}")

    def third_step(self, skippable=False, critical=True):
        """
        Make sure to use a __secure__ algorithm to ensure you are happy with the result
        * Make seven references

        # Use markdown to display instructions
        """

    def last_step(self, name='the end'):
        pass


if __name__ == '__main__':
    ExamplePrintAndDo.main()
