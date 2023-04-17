

from typing import Optional
from logging import debug as log_debug, error as log_err
from datetime import datetime

from billtack.utils import ripples


def from_users(users: list[str], start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> ripples.Ripples:
    """
    从用户列表中获取所有的RippleBase对象
    """
    
    _ripples = ripples.Ripples()
    
    
    
    
    for user in users:
        _ripples.extend(ripples.from_user(user, start_date, end_date))
        
    return _ripples


