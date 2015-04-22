import sublime, sublime_plugin

RE_IMPORT = "import .*;\n"
RE_CLASS = "public class";

class OptimizeImportsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        ##Wraps the other two in one command...
        RemoveUnusedImportsCommand.run(self, edit)
        SortImportsCommand.run(self, edit)
        
#Sort all imports, retaining dividing sections
class SortImportsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        print("sorting imports...")
        sections = self.view.find_all(RE_IMPORT_SECTION, 0)
        section_imports = [self.view.substr(section) for section in sections]
        for i in range(len(sections)):
            imports = section_imports[i][:-1].split("\n")
            imports.sort()
            imports = "\n".join(imports) + "\n"

            self.view.replace(edit, sections[i], imports)

#Removes unused imports by scanning the class for textual references
class RemoveUnusedImportsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        print("organizing imports...")
        imports = self.view.find_all(RE_IMPORT, 0)
        lines_to_remove = []
        class_section = self.view.find(RE_CLASS, 0)

        for import_line in imports:
            import_statement = self.view.substr(import_line)

            lastDelim = max(import_statement.rfind('.'), import_statement.rfind(" ")) + 1
            end = import_statement.rfind(";")

            if(lastDelim > 0 and end > 0):
                class_name = import_statement[lastDelim : end]
                class_occurance = self.view.find("(?![A-Za-z])+." + class_name, class_section.end())

                if (class_occurance.end() == -1):
                  	print(class_name + ' does not seem to be referenced in class, removing import')
                  	lines_to_remove.append(import_line)

        for line in reversed(lines_to_remove):
            self.view.erase(edit, line)