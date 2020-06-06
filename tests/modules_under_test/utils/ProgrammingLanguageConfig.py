from utils import ProgrammingLanguageConstants

PROGRAMMING_LANGUAGE = ''


class LanguageOptionError(RuntimeError):
    ''' user-defined exception used if getter is not applicable to certain languages'''
    def __init__(self, arg):
        self.args = arg

    def __str__(self):
        error_string = ''
        for chr in self.args:
            error_string += chr

        return "LanguageOptionError: {}".format(error_string)


def get_file_extensions_im():
    if PROGRAMMING_LANGUAGE == 'c++':
        return ProgrammingLanguageConstants.CPP_ALLOWED_FILE_EXTENSIONS_IM
    else:
        raise LanguageOptionError("Programming language '{}' is currently not supported!".format(PROGRAMMING_LANGUAGE))


def get_file_extensions_am():
    if PROGRAMMING_LANGUAGE == 'c++':
        return ProgrammingLanguageConstants.CPP_ALLOWED_FILE_EXTENSIONS_AM
    else:
        raise LanguageOptionError("Programming language '{}' is currently not supported!".format(PROGRAMMING_LANGUAGE))


def get_class_identifier():
    if PROGRAMMING_LANGUAGE == 'c++':
        return ProgrammingLanguageConstants.CPP_CLASS_IDENTIFIER
    else:
        raise LanguageOptionError("Programming language '{}' is currently not supported!".format(PROGRAMMING_LANGUAGE))


def get_interface_identifier():
    if PROGRAMMING_LANGUAGE == 'c++':
        raise LanguageOptionError('C++ does not have an interface identifier')
    else:
        raise LanguageOptionError("Programming language '{}' is currently not supported!".format(PROGRAMMING_LANGUAGE))


def get_abstract_method_identifier():
    if PROGRAMMING_LANGUAGE == 'c++':
        return ProgrammingLanguageConstants.CPP_ABSTRACT_METHOD_IDENTIFIER
    else:
        raise LanguageOptionError("Programming language '{}' is currently not supported!".format(PROGRAMMING_LANGUAGE))


def get_namespace_identifier():
    if PROGRAMMING_LANGUAGE == 'c++':
        return ProgrammingLanguageConstants.CPP_NAMESPACE_IDENTIFIER
    else:
        raise LanguageOptionError("Programming language '{}' is currently not supported!".format(PROGRAMMING_LANGUAGE))


def get_prefix_user_include_identifier():
    if PROGRAMMING_LANGUAGE == 'c++':
        return ProgrammingLanguageConstants.CPP_PREFIX_USER_INCLUDE
    else:
        raise LanguageOptionError("Programming language '{}' is currently not supported!".format(PROGRAMMING_LANGUAGE))


def get_prefix_standard_include_identifier():
    if PROGRAMMING_LANGUAGE == 'c++':
        return ProgrammingLanguageConstants.CPP_PREFIX_STD_INCLUDE
    else:
        raise LanguageOptionError("Programming language '{}' is currently not supported!".format(PROGRAMMING_LANGUAGE))
