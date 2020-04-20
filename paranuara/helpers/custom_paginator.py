from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


class AppPaginator(object):

    def __init__(self, objects, page_size=None, page_number=None):

        self.objects = objects
        self.page_size = page_size
        self.page_number = page_number

    def paginate_objects(self):

        if self.page_size:
            if not self.page_number:
                self.page_number = 1

            paginator = Paginator(self.objects, self.page_size)

            try:
                return paginator.page(self.page_number).object_list, paginator.count

            except PageNotAnInteger:
                return paginator.page(1).object_list, paginator.count

            except EmptyPage:
                return paginator.page(paginator.num_pages).object_list, paginator.count

        return self.objects, len(self.objects)