
import re


from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker


def register(linter):
    linter.register_checker(OsEnvironChecker(linter))


class OsEnvironChecker(BaseChecker):
    __implements__ = IAstroidChecker

    name = 'prohibit-os-environ'
    priority = -1
    msgs = {
        'R9000': (
            'Usage of os.environ is prohibited. '
            'Import from django settings instead.',
            'os-environ-prohibited',
            'Modules should not use os.environ directly.'
        ),
    }

    def __init__(self, linter=None):
        """
        Создаем два списка, в которых будем хранить упоминания типа:
        """
        super().__init__(linter)

        self.reset_module_names()

        # флаг, который настраивается при входе в каждый модуль
        # и который проверяется во всех хуках
        self.check_this_module = True

        # достаем регулярку, в которой лежат пути для игнора (в dot-нотации)
        if 'OS_ENVIRON_CHECKER' in linter.cfgfile_parser.sections():
            config = linter.cfgfile_parser['OS_ENVIRON_CHECKER']
            self.allow_in_modules = config.get('allow_in_modules')
        else:
            self.allow_in_modules = None

    def reset_module_names(self):
        """
        Создать два пустых списка, в которых будем хранить упоминания типа:

        import os
        import os as ABC

        from os import environ
        from os import environ as XYZ
        """
        self.os_module_names = []
        self.os_environ_module_names = []

    def visit_module(self, node):
        """
        При заходе в каждый файл проверяем, нужно ли его анализировать,
        и если нужно - то сбрасываем списки упоминаний os.environ
        и разрешаем парсить при помощи флага check_this_module.

        Иначе - запрещаем парсить при помощи флага check_this_module
        """
        if (self.allow_in_modules
            and not re.match(self.allow_in_modules, node.name)
        ):
            self.check_this_module = True
            self.reset_module_names()
        else:
            self.check_this_module = False

    def visit_import(self, node):
        """
        Ищем все строки "import os" и "import os as ABC".
        Кладем в список self.os_module_names вхождения "os",
        а также алиасы "ABC"
        """
        if not self.check_this_module:
            return

        for module_name, module_alias in node.names:
            if module_name == 'os':
                self.os_module_names.append(module_alias or module_name)

    def visit_importfrom(self, node):
        """
        Ищем строки "from os import environ" и "from os import environ as XYZ".
        Кладем в список os_environ_module_names все вхождения environ,
        а также алиасов environ (XYZ)
        """
        if not self.check_this_module:
            return
        if node.modname == 'os':
            for module_name, module_alias in node.names:
                if module_name == 'environ':
                    self.os_environ_module_names.append(
                        module_alias or module_name
                    )

    def visit_attribute(self, node):
        """
        Мы попадаем сюда, когда в коде встречается "object.attribute".
        """
        if not self.check_this_module:
            return

        # если атрибут - это environ...
        if node.attrname == 'environ':

            # если при этом этот атрибут принадлежит модулю os или его алиасам..
            if node.expr.name in self.os_module_names:

                # выдаем ошибку
                self.add_message('os-environ-prohibited', node=node,)

    def visit_name(self, node):
        """
        Мы попадаем сюда, когда в коде встречается обращение к переменной
        """
        if not self.check_this_module:
            return
        # если эта переменная - environ или его алиасы...
        if node.name in self.os_environ_module_names:

            # выдаем ошибку
            self.add_message('os-environ-prohibited', node=node,)
