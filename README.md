# CY_door_Flask



Flask配合socket控制有人云USR-G781网关，发送指令

* 已经添加对于socket长连接超时无响应的处理
* 已经添加鉴权处理
* 已经添加后台心跳包，十分钟检测一次，掉线自动重连
