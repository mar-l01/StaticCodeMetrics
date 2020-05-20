#################################
# abstractness metric constants #
#################################

#######
# C++ #
#######
CPP_ALLOWED_FILE_EXTENSIONS_AM = ['hpp', 'h']

# [\w()]* handles the __ declspec(dllexport)-part of class definition:
# e.g. class __declspec(dllexport) ModbusTcpClient
CPP_CLASS_IDENTIFIER = '\s*(class|struct)\s*[\w()]*\s*\w+\s*'  # noqa: W605

# abstract methods in C++ are typically denoted by setting a virtual method equal to 0:
# e.g. virtual void anAbstractMethod() = 0;
# it starts with (virtual) and ends with (= 0;)
CPP_ABSTRACT_METHOD_IDENTIFIER = '^(\s*virtual)\s+\w+\s*\w*\((.|\s)*\)\s*\w*\s*(=\s*0\s*;)$'  # noqa: W605

# namespaces are indicated by namespace namespaceX
CPP_NAMESPACE_IDENTIFIER = '^(\s*namespace)\s*\w*\s*'  # noqa: W605


#################################
# instability metric constants  #
#################################

#######
# C++ #
#######
CPP_ALLOWED_FILE_EXTENSIONS_IM = ['cpp', 'hpp', 'c', 'h']

# includes-libraries (user/std) in C++ files
CPP_PREFIX_STD_INCLUDE = '#include <'
CPP_PREFIX_USER_INCLUDE = '#include "'
