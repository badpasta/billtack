
from typing import Optional, TypeVar
from datetime import datetime


# 通过泛型，限制group_by函数的参数stats_object的类型是可迭代的
T = TypeVar('T', bound=iter)


def group_by(stats_object: T, key: str, cycle: Optional[str] = None, out_key: list[str] = ['cnt']) -> dict:
    
    stat = {
        'total': {
            'cnt': 0,
            'sum': 0,
        }
    }
    
    for task in stats_object:
        assert key in task, \
            f"{key} is not in task. keys: {task.keys()}"
        group_name = task.get(key)
        if group_name not in stat:
            stat[group_name] = {
                'cnt': 0,
                'sum': 0
            }
            
            
        stat[group_name]['cnt'] += 1
        stat[group_name]['sum'] += task.get('worktime_avg')
        stat['total']['cnt'] += 1
        stat['total']['sum'] += task.get('worktime_avg')
    
    if cycle == 'monthly':
        # 获取tasks中所有的created_at
        data_list = [datetime.strptime(task.get('created_at'), \
                        '%Y-%m-%d %H:%M:%S') for task in stats_object]
        
        # 获取最早和最晚的时间并求跨过的月份
        min_date = min(data_list)
        max_date = max(data_list)
        month_count = (max_date.year - min_date.year) * 12 + \
            (max_date.month - min_date.month) + 1
        
        # 将每个月份的任务数除以月份，得到每个月份的平均任务数
        for key, value in stat.items():
            value['cnt'] = value['cnt'] / month_count
            value['sum'] = value['sum'] / month_count
        
    return stat


def order_by(): ...