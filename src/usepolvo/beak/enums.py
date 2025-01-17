# usepolvo/beak/enums.py

from enum import Enum


class PaginationMethod(Enum):
    OFFSET_LIMIT = "offset_limit"
    PAGE_SIZE = "page_size"
    PAGE = "page"
