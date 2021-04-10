# print-and-do

Based on [runbook.py](https://github.com/UnquietCode/runbook.py) by UnquietCode.

Main changes: 
* Methods are not invoked before getting to the specific step
* * Enables each step to perform operations at the correct time 

Inspired by [this blog post](https://blog.danslimmon.com/2019/07/15/do-nothing-scripting-the-key-to-gradual-automation)
by Dan Slimmon.

Define your own run-book in a class extending from `Runbook`. Every method that
doesn't begin with an underscore is read in as a step to be completed, in order.
The step name will be built from the method name, and the description is taken
either from the method's own docstring or from any data returned from invoking
the method.

# Installation

In print-and-do directory
```
pip install .
```


# Example 
In example/my-first-pad.py you will find a simple example.

Run it with 

```
python3 example/my-first-pad.py
```

```python
from unquietcode.tools.runbook import Runbook


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

    def third_step(self):
        """
        Send an email to mike.
        """
        print(f"The value from step 2 is: {self.value}")
        print(f"The name you entered in step 2 is: {self.name}")

    def fourth_step(self, skippable=False, critical=True):
        value = "string"
        return f"a custom {value}"

    def last_step(self, name='the end'):
        pass

if __name__ == '__main__':
    ExamplePrintAndDo.main()
```

<!-- Every `Runbook` object comes with a default main method that you can use to execute the script. -->

<!-- The run-book object can also be instantiated and run directly. -->

<!-- ```python
book = CustomRunbook(file_path="path/to/file")
book.run()
``` -->

**You should avoid using the step names `run` and `main`**, which are already defined, unless you need to override these methods to define custom behavior.

As steps are completed, the results are written out to a log file (equal to the name of the class). You can set a custom log file path by passing
an argument to main, as in:

```
python3 my_runbook.py output.log
```

When reusing the same log file, already completed steps will be skipped. Any new steps found in the `Runbook`
and not already in the log will be processed as normal, with results appended to the end of the file.


## Standalone version

A super-simple do nothing script is included in example/standalone.
This script has no dependencies to the project, so it can be copied over and run without any installation.

Using the standalone version is preferred to get a feel for what a do nothing script can accomplish, or when you don't want to install a whole package or download the entire repository to do something.

Test the script with:
```
python example/standalone/standalone-pad.py
```
Steps are run in the order the methods are declared in the file.

### License

print-and-do (LemurP): Licensed under the MIT License

runbook.py (UnquietCode): Licensed under the Apache Software License 2.0 (ASL 2.0).