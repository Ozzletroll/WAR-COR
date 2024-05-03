import json



class Paginator:
    """ Paginator class to format all results for template """

    def __init__(self, data, page, per_page):
        self.data = data
        self.per_page = per_page
        self.pages = self.initialise_pages()
        self.current_page = page
        self.page = self.get_current_page(page)
        self.total_pages = len(self.pages)
        self.page_numbers = self.get_page_numbers()

    def initialise_pages(self):

        pages = []
        page_number = 1

        for index in range(0, len(self.data), self.per_page):
            new_page = Page(page_number=page_number,
                            items=self.data[index:index + self.per_page])
            pages.append(new_page)
            page_number += 1

        return pages

    def get_current_page(self, page):

        if page > len(self.pages) or page < 1:
            return None
        else:
            return self.pages[page - 1]

    def get_page_numbers(self,
                         left_edge = 2,
                         left_current = 2,
                         right_current = 4,
                         right_edge = 2):
        
        def remove_consecutive_nones(list):

            if not list:
                return[1]

            new_list = [list[0]]
            for index in range(1, len(list)):
                if list[index] is None and list[index - 1] is None:
                    continue
                new_list.append(list[index])

            return new_list
        
        page_numbers = []

        for index, page in enumerate(self.pages):
            if (index + 1 <= left_edge or 
                page.page_number > (self.total_pages - right_edge) or 
                page.page_number == self.current_page or 
                self.current_page <= page.page_number < self.current_page + right_current or 
                self.current_page - left_current <= page.page_number < self.current_page):
                page_numbers.append(page.page_number)
            else:
                page_numbers.append(None)

        return remove_consecutive_nones(page_numbers)
    
    def serialise(self, target_url, new_page_url):

        object_dict = self.__dict__
        object_dict["pages"] = [page.serialise() for page in object_dict["pages"]]
        object_dict["page"] = object_dict["page"].serialise()
        object_dict["target_url"] = target_url
        object_dict["new_page_url"] = new_page_url
        return json.dumps(object_dict)


class Page:

    def __init__(self, page_number, items):
        self.page_number = page_number
        self.items = items

    def serialise(self):
        return self.__dict__
