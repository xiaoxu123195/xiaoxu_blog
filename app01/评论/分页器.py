from urllib.parse import urlencode
import math


class Pagination:
    def __init__(self, current_page, all_count, base_url, query_params, per_page=20, pager_page_count=11):
        """
        :param current_page: 当前页码
        :param all_count: 数据库中的总条数
        :param base_url: 原始url
        :param query_params: 保留原搜索条件
        :param per_page: 一页展示多少条
        :param pager_page_count: 最多显示多少个页码
        """
        self.all_count = all_count
        self.per_page = per_page
        # 计算一共有多少个页码
        # 1.取余
        # div, p = divmod(all_count, per_page)
        # if p != 0:
        #     div += 1
        # self.current_count = div
        # 2.进位
        self.current_count = math.ceil(all_count / per_page)

        # 1.只能满足的数字条件
        try:
            self.current_page = int(current_page)
            if not 0 < self.current_page <= self.current_count:
                self.current_page = 1
        except Exception:
            self.current_page = 1

        self.base_url = base_url
        self.query_params = query_params
        self.pager_page_count = pager_page_count
        # 分页器的中值
        self.half_pager_count = int(self.pager_page_count / 2)
        if self.current_count < self.pager_page_count:
            # 如果可分页的页码小于最大显示页码，就让最大显示页码变为可显示页码
            self.pager_page_count = self.current_count

    def pager_html(self):
        # 计算页码的起始和结束
        start = self.current_page - self.half_pager_count
        end = self.current_page + self.half_pager_count
        if self.current_page <= self.half_pager_count:
            # 在最左侧
            start = 1
            # 右边就是最大值
            end = self.pager_page_count
        if self.current_page + self.half_pager_count >= self.current_count:
            # 在最右侧
            start = self.current_count - self.pager_page_count
            end = self.current_count
        # 生成分页
        page_list = []

        # 上一页
        if self.current_page != 1:
            self.query_params['page'] = self.current_page - 1
            page_list.append(f'<li><a href="{self.base_url}?{self.query_encode}">上一页</a></li>')

        for i in range(start, end+1):
            self.query_params['page'] = i
            if self.current_page == i:
                li = f'<li class="active">< href="{self.base_url}?{self.query_encode}">{i}</a></li>'
            else:
                li = f'<li><a href="{self.base_url}?{self.query_encode}">{i}</a></li>'
            page_list.append(li)

        # 下一页
        if self.current_page != self.current_count:
            self.query_params['page'] = self.current_page + 1
            page_list.append(f'<li><a href="{self.base_url}?{self.query_encode}">下一页</a></li>')

        return ''.join(page_list)

    @property
    def query_encode(self):
        return urlencode(self.query_params)

    @property
    def start(self):
        return (self.current_page - 1) * self.per_page

    @property
    def end(self):
        return self.current_page * self.per_page


if __name__ == '__main__':
    pager = Pagination(
        current_page='a',
        all_count=100,
        base_url='/article',
        query_params={'tag': 'python'},
        per_page=4,
        pager_page_count=7
    )
    # print(pager.start, pager.end)
    print(pager.pager_html())
