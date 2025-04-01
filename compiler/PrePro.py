import re
class PrePro:

    regex_comentarios = r"//.*?$"

    def filter(source):
        return re.sub(PrePro.regex_comentarios, "", source, flags=re.MULTILINE)