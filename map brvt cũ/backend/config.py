VARIABLES = [
    "Thành phố Vũng Tàu", 
    "Thành phố Bà Rịa", 
    "Thị xã Phú Mỹ", 
    "Huyện Châu Đức", 
    "Huyện Long Điền", 
    "Huyện Đất Đỏ", 
    "Huyện Xuyên Mộc", 
    "Huyện Côn Đảo"
]

DOMAINS = ["Đỏ", "Xanh lá", "Xanh dương"]

CONSTRAINTS = [
    ("Thành phố Vũng Tàu", "Thành phố Bà Rịa"), 
    ("Thành phố Vũng Tàu", "Huyện Long Điền"),
    ("Thành phố Bà Rịa", "Thị xã Phú Mỹ"), 
    ("Thành phố Bà Rịa", "Huyện Châu Đức"), 
    ("Thành phố Bà Rịa", "Huyện Long Điền"),
    ("Thị xã Phú Mỹ", "Huyện Châu Đức"),
    ("Huyện Châu Đức", "Huyện Long Điền"), 
    ("Huyện Châu Đức", "Huyện Đất Đỏ"), 
    ("Huyện Châu Đức", "Huyện Xuyên Mộc"),
    ("Huyện Long Điền", "Huyện Đất Đỏ"),
    ("Huyện Đất Đỏ", "Huyện Xuyên Mộc")
]

class CSP:
    def __init__(self, variables, domains, constraints):
        self.VARIABLES = variables.copy()
        self.DOMAINS = {v: list(domains) for v in variables}
        self.CONSTRAINTS = constraints.copy()
