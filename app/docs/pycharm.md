如何设置让pycharm 自动提示忽略大小写
在 PyCharm 里设置“自动提示忽略大小写”，可以这样操作：

### 设置步骤

1. 打开设置：
   - Windows / Linux：`File` → `Settings`
   - macOS：`PyCharm` → `Settings/Preferences`
   - 快捷键通常是 **Ctrl + Alt + S**

2. 进入路径：
   ```text
   Editor → General → Code Completion
   ```

3. 找到 **Match case** 或 **Case sensitive completion** 选项。

4. 把它改成不区分大小写：
   - 如果有 **Match case**：取消勾选，或选择 **None / First letter only**
   - 如果有 **Case sensitive completion**：选择 **None**
   - 如果看到中文界面：把“区分大小写”改为 **无** 或 **仅首字母**

5. 点击 **Apply** → **OK**。

### 推荐选择

| 选项 | 效果 |
|---|---|
| **None / 无** | 完全忽略大小写，提示最宽松 |
| **First letter only / 仅首字母** | 首字母要匹配，后面忽略大小写 |
| **All letters / 所有字母** | 严格区分大小写 |

一般日常写代码，选 **None** 或 **First letter only** 比较舒服。

如果改完后仍然没有自动提示，可以再确认一下没有开启 **Power Save Mode**，并且项目 Python 解释器配置正确。

---
你用的是哪个版本的 PyCharm？不同版本的界面位置可能略有差异，我可以帮你更准确地定位。