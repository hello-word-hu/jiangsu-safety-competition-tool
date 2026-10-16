# "江苏省大学生安全知识竞赛"脚本

> 一个用于**课程/竞赛答题流程自动化**的学习研究脚本（Python + requests）。
> 本仓库是 [@Scwizard](https://github.com/Scwizard) 的
> [jiangsu-safety-competition](https://github.com/Scwizard/jiangsu-safety-competition) 的**整理版**，
> 遵循原仓库 **Apache License 2.0**，保留原始版权与许可（见 `LICENSE`），并**明确标注本版所做修改**。

---

## 一、这个仓库是什么

- 面向**江苏省大学生安全知识竞赛**（学校使用的 `*.mycourse.cn` 平台）的答题流程自动化脚本
- 仅包含 Python 源码，共 4 个必要文件 + 1 个题库文件，其余全部清理
- 支持 PyInstaller 打包为单文件 exe（Release 由 GitHub Actions 自动构建）

## 二、特性

| 能力 | 说明 |
|---|---|
| 新题库 | `database.db`（SQLite，表 `tiku`：`question`=题号、`answer`=正确选项号），**可直接替换**成你自己的题库 |
| 通过试题获取题库 | 运行"练习 / 模拟考试"任务时，脚本会把服务器下发的正确项（`optionList[].isCorrect`）**自动追加写入 `~/tiku_learned.csv`**，多跑几轮即可攒出题库 |
| 三档取答案 | 正式考试时按 ①试卷下发的正确项 → ②本地题库 → ③试卷第一个选项（保证不留空白卷）依次取答案，三者都没有才跳过（**不会中断整场考试**） |
| 一键重打包 | `repack_db.py` 把采集到的 CSV 变成新题库，并塞回 exe，生成"新题库版"程序 |

## 三、使用说明

```bash
pip install -r requirements.txt
python main.py
```

1. 输入学校名称（支持关键词）→ 选择学校
2. 输入用户名、密码，按提示保存验证码图片并输入验证码
3. 选择任务类型：
   - **练习 / 模拟考试**：跑一轮即可采集题库（结果写入 `~/tiku_learned.csv`）
   - **正式考试**：输入期望分数与每题时长后自动作答
4. 题库缺口补齐后重新打包：
   ```bash
   # CSV -> 新题库 -> 新程序
   python repack_db.py --from-csv ~/tiku_learned.csv new_bank.db main.py out.exe
   ```

打包 exe（本地）：
```bash
pyinstaller -F -n jiangsu-safety-competition main.py
```

## 四、注意事项（请务必阅读）

1. **脚本运行期间不要在其他设备登录同一账号**，否则会挤掉会话、浪费考试机会。
2. 每题时长不要低于 6 秒（平台会把间隔过短的作答判为无效）；脚本已内置每题等待。
3. 期望分数的真实含义是"前 N 题正常作答，其余主动记为错题"；想全部作答请把 N 填成 ≥ 题目总数。
4. 题库来源：内置题库仅为示例；`~/tiku_learned.csv` 由你自己的账号在练习任务中采集。
5. 不要在本仓库提交**账号、密码、token、Cookie、手机号、邮箱**等任何个人/凭据信息。
6. 请不要用于代考、批量刷课等违规用途；使用产生的后果由使用者自行承担。

## 五、本版做了哪些修改（相对原作者仓库）

原作者：[@Scwizard](https://github.com/Scwizard)，原仓库：[jiangsu-safety-competition](https://github.com/Scwizard/jiangsu-safety-competition)（Apache-2.0）。

1. **修复崩溃**：正式考试中若某题不在题库，原逻辑 `request_data(questionId)[0][1]` 会抛 `IndexError: list index out of range` 并整场中断；现改为**三档取答案**且失败仅跳过该题。
2. **新增题库采集**：练习/模拟任务自动把"题号 → 正确选项"写入 `~/tiku_learned.csv`。
3. **新增 `repack_db.py`**：把采集到的 CSV 合成 `database.db` 并重新打包 exe，形成"采集 → 建库 → 出包"闭环。
4. **清理与精简**：删除多余文件，只保留运行必需的 4 个源码文件 + 题库；打赏图替换为整理者提供的收款码（微信码已遮挡真实姓名）。
5. **新增 Release 工作流**：`.github/workflows/release.yml`，打 tag 自动构建 Windows 单文件 exe 并上传到 Release。
6. **新增文档**：本 README 的使用说明、注意事项、免责声明与致谢。

## 六、免责声明

- 本项目仅供**学习、研究与个人技术交流**，用于了解 Web 端答题流程自动化与数据解析方法。
- 使用者应遵守所在学校、竞赛主办方与平台的服务条款；**禁止**用于代考、冒名作答、批量刷课、售卖题库等违规或违法用途。
- 项目按 **Apache License 2.0** 提供，**不附带任何担保**；因使用本项目造成的账号封禁、成绩作废、机会损失等后果，由使用者自行承担。
- 本仓库不收集、不存储任何个人信息；采集出的 `tiku_learned.csv` 仅保存在使用者本机。
- 如原作者或平台方认为本整理版不妥，请提 Issue，会立即下架。

## 七、致谢

- 感谢原作者 **[@Scwizard](https://github.com/Scwizard)** 的开源实现与题库整理，本版本的所有自动化能力都建立在原作者 的代码之上。
- 感谢每一位提交 Issue / PR 的同学。

## 八、打赏（自愿，感谢支持）

<p align="center">
  <img src="donation_alipay.png" width="300" alt="支付宝">
  <img src="donation_wechat.png" width="300" alt="微信">
</p>

---

License: Apache-2.0 · 原始版权归原作者所有
