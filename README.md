# print-and-do

Based on [runbook.py](https://github.com/UnquietCode/runbook.py) by UnquietCode.

Main changes: 
* Methods are not invoked before getting to the specific step
  * Enables each step to perform operations at the correct time
* Command-line interface for running PADos from start
* Standalone version without any requirements
* Central storage of which pados have been registered, to enable listing all known pados
* List all PADos in a directory (beta)

Inspired by [this blog post](https://blog.danslimmon.com/2019/07/15/do-nothing-scripting-the-key-to-gradual-automation)
by Dan Slimmon.

Define your own run-book in a class extending from `Runbook`. Every method that
doesn't begin with an underscore is read in as a step to be completed, in order.
The step name will be built from the method name, and the description is taken from the method's own docstring.

# Similar projects
[Runbook by Braintree](https://github.com/braintree/runbook) - Create automated runbooks for tasks. Powerful tool, written in Ruby.

>Though Runbook can solve a myriad of problems, it is best used for removing the need for repeated, rote developer operations. Runbook allows developers to execute processes at a higher level than that of individual command-line commands. Additionally, Runbook provides features to simply and safely execute operations in mission-critical environments.

Print-And-Do exists as a simpler version of a Runbook, but somewhat more powerful than a do-nothing script. For users more familiar with Python this can be a simpler place to start.

# Use cases
You have a process that requires manual steps, but you know some or all of the steps can be automated. Automating everything at once is a daunting task.

By structuring the manual process as a Print-And-Do script you can perform the process as a step-by-step process where each step can be automated separately.

Pasting an existing process description into a PADo is often a good first iteration. Then you run the script to see the description. Each time you performs the process, you should refine the PADo and hopefully be able to automate some part. When the entire PADo is automated, it can be turned into a fully automated script by removing the reference to Runbook and being run in a pipeline or as a cron-job.

# Installation

In print-and-do directory
```
pip install .
```


# Example 
In example/my-first-pad.py you will find a simple example.

Run it with 

```
pado run example/my-first-pad.py
```

```python
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