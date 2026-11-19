# GSB Bugfix Task
## 题面
技能栏经常出现充能显示和实际能不能放对不上：两层充能的技能第一次放完就整条变灰，急速属性只影响面板不影响真实回复，多个技能共用同一个计时器，时间回拨后充能直接算错，状态接口返回的内部字典还能被外部改坏。ability_cooldown.py 的 CooldownTracker 要处理 cast、advance、ready 和 state，需要按技能独立充能、支持多层充能和急速缩短冷却、记录部分回复进度、拒绝时间回拨和非法配置，状态返回副本。

## 运行方式
```bash
python -m pytest tests -q
```

## 平台字段

所属领域：安全
子方向：游戏开发
任务类型：Bugfix
语言 / 框架：Python 3, pytest
环境可复现等级：有外部依赖，未容器化
