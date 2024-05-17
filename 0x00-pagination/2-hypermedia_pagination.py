#!/usr/bin/env python3
"""
Pagination with hypermedia
"""
import csv
from typing import List, Tuple, Dict, Any
import math


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    Return a tuple containing the start index and
    end index for the range of items
    in a list that corresponds to the given
    pagination parameters.

    Parameters:
    page (int): The page number (1-indexed).
    page_size (int): The number of items per page.

    Returns:
    tuple: A tuple of two integers representing
    the start index and end index.
    """
    start_index = (page - 1) * page_size
    end_index = page * page_size

    return start_index, end_index


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]  # Skip the header

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        Get a page from the dataset.

        Parameters:
        page (int): The page number (1-indexed).
        page_size (int): The number of items per page.

        Returns:
        List[List]: The list of rows corresponding
        to the given page and page size.
        """
        assert isinstance(page, int) and page > 0,\
            "Page must be a positive integer."
        assert isinstance(page_size, int) and page_size > 0,\
            "Page size must be a positive integer."

        start_index, end_index = index_range(page, page_size)
        dataset = self.dataset()

        # If start index is out of range of dataset, return an empty list
        if start_index >= len(dataset):
            return []

        return dataset[start_index:end_index]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Get a page from the dataset along with pagination information.

        Parameters:
        page (int): The page number (1-indexed).
        page_size (int): The number of items per page.

        Returns:
        Dict[str, Any]: A dictionary containing pagination information.
        """
        data = self.get_page(page, page_size)
        total_items = len(self.dataset())
        total_pages = math.ceil(total_items / page_size)

        next_page = page + 1 if page < total_pages else None
        prev_page = page - 1 if page > 1 else None

        return {
            "page_size": len(data),
            "page": page,
            "data": data,
            "next_page": next_page,
            "prev_page": prev_page,
            "total_pages": total_pages
        }
