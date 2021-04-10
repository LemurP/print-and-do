import inspect

class ExamplePrintAndDoStandalone():
    def _preamble(self):
        return """This pad is a basic example that exercises
the various options available.
"""

    def first_step(self):
        print("""Do ABC now.""")
    
    
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
        pass

    def __get_steps(self):
        # sort methods by declaration order
        def key_filter(value):
            value = value[1]
            
            if hasattr(value, '__func__'):
                return value.__func__.__code__.co_firstlineno
            else:
                return value.__code__.co_firstlineno
        
        def is_not_private_main_or_run(value):
            if value[0][0]=='_' or value[0]=='main' or value[0]=='run':
                return False
            return True
        
        all_methods = inspect.getmembers(self, lambda _:(inspect.ismethod(_) or inspect.isfunction(_)) and not inspect.isbuiltin(_))
        print([_[0] for _ in all_methods])
        all_methods = sorted(all_methods, key=key_filter)
        filtered_methods = [_ for _ in filter(is_not_private_main_or_run,all_methods)]
        print([_[0] for _ in filtered_methods])
        return filtered_methods
    def run(self):
        
        # title
        pretty_class_name = type(self).__name__
        pretty_class_name = pretty_class_name.replace('_',' ')
        
        print()
        print(f"\t======={'='*len(pretty_class_name)}=======")
        print(f"\t       {pretty_class_name}       ")
        print(f"\t======={'='*len(pretty_class_name)}=======")
        
        # preamble
        preamble = self._preamble()
        
        if preamble:
            print()
            print(preamble)
        all_steps = self.__get_steps()
        number_of_steps = len(all_steps)
        for i,step in enumerate(all_steps):
            print()
            print(f"\t======Step {i+1}/{number_of_steps}======")
            step[1]()
            print()
            input("\tDo the thing [enter to continue]")
            
        print()
        print("\nAll steps completed!\n")
        
        return None

    
if __name__ == '__main__':
    ExamplePrintAndDoStandalone().run()