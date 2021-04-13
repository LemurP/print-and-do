#!/usr/bin/env python
import inspect


class ExamplePrintAndDoStandalone():
    def _preamble(self):
        return "This pad is a standalone example that showcases a basic do nothing script."

    def first_step(self):
        print("Do ABC now.")

    def second_step(self):
        print("Find the name of the largest planet in our solar system. Paste it below")

        self.name = input("Enter a name:")
        self.value = 10

    def third_step(self):
        print("Send an email to mike.")
        print(f"The value from step 2 is: {self.value}")
        print(f"The name you entered in step 2 is: {self.name}")

    def fourth_step(self):
        print("Add steps by creating a new function in ExamplePrintAndDoStandalone")
        print("Each step is executed according to the order in the class")

    def __get_steps(self):
        # sort methods by declaration order
        def key_filter(name_method_tuple):
            method = name_method_tuple[1]

            if hasattr(method, '__func__'):
                return method.__func__.__code__.co_firstlineno
            else:
                return method.__code__.co_firstlineno

        def is_not_private_main_or_run(name_method_tuple):
            name = name_method_tuple[0]
            return not (name[0] == '_' or name == 'main' or name == 'run')

        all_methods = inspect.getmembers(self, lambda _: (inspect.ismethod(_) or inspect.isfunction(
            _)) and not inspect.isbuiltin(_))
        all_methods = sorted(all_methods, key=key_filter)

        filtered_methods = [_ for _ in filter(is_not_private_main_or_run, all_methods)]
        return filtered_methods

    def run(self):

        # title
        class_name = type(self).__name__.replace('_', ' ')

        print(f"\n\t======={'=' * len(class_name)}=======")
        print(f"\t       {class_name}       ")
        print(f"\t======={'=' * len(class_name)}=======")

        # preamble
        preamble = self._preamble()

        if preamble:
            print()
            print(preamble)

        all_steps = self.__get_steps()
        number_of_steps = len(all_steps)
        for i, step in enumerate(all_steps):
            print(f"\n\t======Step {i + 1}/{number_of_steps}======")
            step_method = step[1]
            step_method()
            input("\n\tDo the thing [enter to continue]")

        print("\nAll steps completed!\n")
        return None


if __name__ == '__main__':
    ExamplePrintAndDoStandalone().run()
