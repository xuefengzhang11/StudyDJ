from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'order'

urlpatterns = [
    # 判断用户是否购买这门课程
    url(r'isBuy/(?P<courid>\d+)/(?P<usertel>\d+)', views.isBuy, name='isBuy'),
    # 加入购物车
    url(r'joinCart/(?P<courid>\d+)/(?P<usertel>\d+)', views.joincart, name='joincart'),
    # 查询购物车
    url(r'getCourCarts/(?P<usertel>\d+)', views.getCourCarts, name='getCourCarts'),
    # 得到订单信息
    url(r'getStatusOrder/(?P<usertel>\d+)/(?P<status>\d+)', views.getStatusOrder, name='getStatusOrder'),
    # 删除订单
    url(r'deleteOrder/(?P<orderid>\d+)/', views.deleteOrder, name='deleteOrder'),
    # 通过id删除购物车数据
    url(r'delCartById/(?P<cartid>\d+)', views.delCartById, name='delCartById'),
    # 全选或者全不选 choiceAllOrNot
    url(r'choiceAllOrNot/(?P<flag>\w+)/(?P<usertel>\d+)', views.choiceAllOrNot, name='choiceAllOrNot'),
    # 单个选择或取消 ChangeCartById
    url(r'ChangeCartById/(?P<cartid>\d+)/(?P<usertel>\d+)', views.ChangeCartById, name='ChangeCartById'),
    # 购买
    url(r'goBuy/(?P<usertel>\d+)', views.goBuy, name='goBuy'),
    # 取消购买
    url(r'noBuy/(?P<usertel>\d+)', views.noBuy, name='noBuy'),

]
