from dataclasses import dataclass


# schema được dùng để định nghĩa cấu trúc của tài liệu được truy vấn từ hệ thống
@dataclass
class RetrieverDocument:
    id: str
    score: float # độ confident
    text: str
    metadata: dict[str, any]
