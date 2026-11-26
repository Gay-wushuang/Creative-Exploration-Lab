# 生成简报模板（内部使用，不向用户展示工具参数）

```yaml
kind: music-cover
ratio: "4:3"
reference_roles:
  main:
    source: "用户上传图1"
    fixed_identity: ["发型", "脸型", "眼睛", "标志配饰", "服装结构"]
text_verbatim:
  title: "[原样写入]"
  credit: "cover [原样写入]"
composition:
  focal_point: "人物眼睛"
  subject_size: "70%"
  subject_position: "中心偏右"
  title_layers: "标题与前景发丝部分交织"
visual_concept: "[一句话视觉隐喻]"
art_medium: "[人物媒介] × [背景媒介] × [排版媒介]"
colors: ["主色1", "主色2", "强调色"]
locked: ["文字内容", "人物形象", "确认的空间结构"]
forbidden: ["无关装饰", "未经授权的人设改变", "多余文案"]
qa: ["文字逐字校对", "角色对照", "比例与手部检查", "缩略图可读"]
```

生成前填入用户实际数据，不可把方括号占位符直接渲染到图中。
