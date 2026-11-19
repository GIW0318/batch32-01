# GSB Bugfix Task
## 题面
地形区块一多，LOD 就开始抖：镜头往前推一格，远处区块整片跳档；相邻区块差了两级，接缝直接裂开；预算只按距离砍，结果把近处高模砍掉、远处低模留着；上一帧刚选过的区块这一帧又被换掉。terrain_quadtree.py 的 TerrainQuadtree 要实现 add_patch 和 select。要按区块尺寸和镜头距离分档、邻居 LOD 差不能超过一级并沿接缝传播、预算内优先保留近处、支持上一帧结果做滞回、非法区块和邻居要报错。

## 运行方式
```bash
python -m pytest tests -q
```

## 平台字段

所属领域：安全
子方向：图形渲染
任务类型：Bugfix
语言 / 框架：Python 3, pytest
环境可复现等级：有外部依赖，未容器化
