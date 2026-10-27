# ONERGY 欧洲储能运维初稿

交付：20页16:9中文演讲PPTX，路径onergy_europe_om_draft.pptx。原生文字、线条、表格构成与图形可编辑；照片为源图。含20页中文讲稿备注。

## 事实来源与边界
仅成功读取《历橙新能源企业宣传10.14.pdf》（33页）。原始两份PPTX超过工具32MiB上限，另一《历橙演讲.pptx》未读取。公司/项目事实均标注PDF页码。未引用未经核实的2026年行业统计或海外法规。公司披露数字不等于第三方审计。小程序、AI和合作范围均注明“建议方案”，不假设已上线。

## 需要补充的数据
1. 匈牙利主案例：项目业主/匿名口径、MW功率、服务日期、合同边界、验收记录、遗留项关闭、恢复时间/调试周期的原始证据。
2. 三个补充案例：荷兰项目容量，全部项目服务日期、验收与修复前后数据；“20+场站维护”与波兰115MWh单项目的统计关系。
3. 运维指标：技术可用率分母及排除项、首次响应/到场/恢复的时间戳、重复故障观察窗口、样本量与统计期。
4. 欧洲覆盖：服务时效起止与例外、资格文件、现场准入、可用人员/库存；维修300+的统计期间及质量指标。
5. 国内“1000+项目实证”的去重定义；小程序当前状态、真实界面与AI试点评估；演讲者姓名、职务及公开联系方式。

## 字体和预览
本机及输出使用Noto Sans CJK SC。PPTX未嵌入字体；接收方安装同字体可减少版式变化。PDF包含字体子集，适合直接审阅。preview/index.html及01—20.png为实际成品渲染，非仅SVG预览。

## 复现
使用 /workspace/shared/ppt-master-minimal/bin/python。
先后运行 output/build_onergy.py --stage check、--stage split、--stage finalize、--stage export --replace（每条命令单独执行）。源SVG逐页手工编写，保存在projects/onergy_europe_om_ppt169_20261027/svg_output/，不是python-pptx默认模板。
构建脚本调用已安装PPT Master的质量检查、讲稿拆分、后处理和原生DrawingML导出；仅在生成文件上明确中西文字体，并按实际Noto字体测量文本框，避免上游估宽导致换行。没有修改技能转换器源码。
render_onergy_preview.py调用技能官方浏览器渲染器，使用系统Chromium，不安装浏览器。需先用最小环境启动技能svg_editor/server.py，对上述项目加--live --no-browser --port 15051。
成品PDF由LibreOffice打开PPTX生成；validate_onergy.py检查PPTX编辑回存、20页讲稿、字体、文字完整、意外换行和页面边界。

## 检查结果
20/20 SVG质量检查通过。原生导出20成功0失败，最终PPTX重新打开、编辑回存通过；LibreOffice打开并导出20页PDF；所有SVG文字均在对应PDF页出现，意外换行与出界均为0。字体仅Noto Sans CJK SC常规/粗体。Microsoft PowerPoint桌面端未直接启动验证，终端字体和版本可能造成差异。
未调用收费API，未生成AI图片，未提交或推送Git。
