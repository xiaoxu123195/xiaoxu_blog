from urllib.parse import urlencode


class Search:
    def __init__(self, key, order, order_list, query_params):
        self.key = key
        self.order_list = order_list
        self.order = order
        self.query_params = {}
        for i in query_params:
            self.query_params[i] = query_params.getlist(i)

    def order_html(self):
        order_list = []
        for li in self.order_list:
            self.query_params[self.key] = li[0]
            if self.order == li[0]:
                li = f'<li class="active"><a href="?{self.query_encode}">{li[1]}</a></li>'
            else:
                li = f'<li><a href="?{self.query_encode}">{li[1]}</a></li>'
            order_list.append(li)

        if not self.order:
            # 没有传递order
            str_li = order_list[0]
            new_str = str_li[0:3] + ' class="active"' + str_li[3:]
            order_list[0] = new_str

        return ''.join(order_list)

    @property
    def query_encode(self):
        # return self.query_params.urlencode()
        return urlencode(self.query_params, doseq=True)


# if __name__ == '__main__':
#     order = Search(
#         order='look_count',
#         order_list=[
#             ('-create_date', '最新发布'),
#             ('look_count', '最多浏览'),
#             ('digg_count', '最多点赞'),
#             ('collects_count', '最多收藏'),
#             ('comment_count', '最多评论')
#         ],
#         query_params={"key": 'python'}
#     )
#     print(order.order_html())
