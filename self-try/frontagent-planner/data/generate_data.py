"""
从 FrontAgent Planner 提示词生成合成训练数据

使用 Claude API 为前端任务场景生成结构化执行计划，
输出 Alpaca 格式的训练数据。

使用方式:
  export ANTHROPIC_API_KEY=sk-ant-...
  python generate_data.py --count 100 --output train.json
  python generate_data.py --count 20 --output eval.json
"""

import json
import argparse
import os
import time
from pathlib import Path

import anthropic

# ─── Planner 系统提示词（精简版，用于生成训练数据） ───────────────────────

PLANNER_SYSTEM = """你是一位经验丰富的高级软件工程师，拥有跨多种编程语言和框架的专家级知识。你擅长分析复杂任务并制定清晰、可执行的计划。

# 你的工作方式

## 计划结构
你的计划应该按阶段组织，每个阶段有明确的目标：
- **阶段1-分析**: 了解项目现状（list_directory, read_file）
- **阶段2-创建**: 创建或修改文件（create_file, apply_patch）
- **阶段3-安装**: 安装依赖（run_command: npm/pnpm install）
- **阶段4-验证**: 类型检查、构建验证（run_command: tsc --noEmit, npm run build）
- **阶段5-启动**: 启动开发服务器（run_command: npm run dev）
- **阶段6-浏览器验证**: 验证应用运行（browser_navigate, browser_screenshot）
- **阶段7-仓库管理**: 在验收通过后执行仓库自动化（run_command: git/gh）

根据任务类型选择需要的阶段：
- 分析类任务：只需阶段1
- 修改类任务：阶段1 → 阶段2 → 阶段4
- 创建类任务：完整的阶段1-6，若有代码变更且验收通过则追加阶段7

# 可用工具
- read_file: 读取文件内容
- list_directory: 列出目录结构
- create_file: 创建新文件（需设置 needsCodeGeneration: true）
- apply_patch: 修改现有文件（需设置 needsCodeGeneration: true）
- run_command: 执行终端命令
- search_code: 搜索代码
- browser_navigate: 浏览器访问URL
- browser_screenshot: 页面截图

# 输出格式
输出一个 JSON 对象，包含：
- summary: 任务概要描述
- stepOutlines: 步骤列表，每个步骤包含 description、action、phase
- risks: 潜在风险列表
- alternatives: 备选方案列表

每个步骤必须有明确的 phase 字段（如"阶段1-分析"、"阶段2-创建"等）。"""

# ─── 前端任务场景库 ─────────────────────────────────────────────────────

TASK_TEMPLATES = [
    # === 创建类任务 ===
    "创建一个{framework}项目，使用{css}作为样式方案，包含基本的项目结构",
    "创建一个{component}组件，包含{feature1}和{feature2}功能",
    "创建一个{page}页面，使用{layout}布局，包含{elements}",
    "创建一个响应式的{component}组件，在移动端显示为{mobile}，桌面端显示为{desktop}",
    "创建一个带有{animation}动画效果的{component}组件",
    "创建一个{form}表单页面，包含{fields}字段和{validation}验证",
    "创建一个{chart}图表组件，使用{library}库，展示{data}数据",
    "创建一个带有{feature}功能的{component}，支持{props}等属性配置",
    "创建一个{auth}认证页面，包含{pages}等流程页面",
    "创建一个{dashboard}管理面板，包含{widgets}等模块",

    # === 修改类任务 ===
    "将{component}组件从{old}迁移到{new}",
    "为{component}添加{feature}功能，确保不影响现有功能",
    "重构{file}文件，将{old_pattern}改为{new_pattern}",
    "修复{component}中的{bug}问题",
    "优化{component}的{aspect}，提升{metric}",
    "为{page}页面添加{responsive}响应式支持",
    "更新{component}的{style}样式，使其符合{design}设计规范",
    "为{api}接口添加{handling}错误处理",
    "将{component}拆分为{subcomponents}子组件",
    "添加{test}测试到{component}组件",

    # === 分析类任务 ===
    "分析项目的{aspect}，找出{issue}问题",
    "检查{component}组件的{quality}质量",
    "审查{file}文件中的{concern}",
    "列出项目中所有{pattern}的使用情况",
    "分析{dependency}依赖的使用情况和版本兼容性",
]

# 场景变量
FRAMEWORKS = ["React + TypeScript", "Vue 3 + TypeScript", "Next.js", "Nuxt.js", "Vite + React"]
CSS_OPTIONS = ["Tailwind CSS", "CSS Modules", "Styled Components", "Ant Design", "Material UI"]
COMPONENTS = ["导航栏", "侧边栏", "数据表格", "文件上传", "图片轮播", "下拉选择", "日期选择器",
              "模态对话框", "通知提示", "面包屑", "分页器", "搜索框", "标签页", "步骤条", "树形控件"]
PAGES = ["用户登录", "用户注册", "个人设置", "商品详情", "购物车", "订单列表", "数据看板",
         "消息中心", "文件管理", "权限管理", "系统配置", "操作日志"]
FEATURES = ["排序筛选", "分页加载", "拖拽排序", "批量操作", "实时搜索", "数据导出",
            "主题切换", "国际化", "键盘快捷键", "无限滚动", "虚拟列表"]
FORMS = ["用户信息编辑", "商品发布", "订单创建", "审批流程", "问卷调查", "评论提交"]
FIELDS = ["用户名、邮箱、手机号", "标题、内容、分类、标签", "收货地址、支付方式",
          "开始日期、结束日期、优先级", "评分、文字评论、图片上传"]
VALIDATIONS = ["实时校验", "提交时校验", "自定义规则校验", "异步校验（如检查用户名重复）"]
BUGS = ["样式错位", "状态不同步", "内存泄漏", "渲染性能问题", "事件处理异常", "路由跳转错误"]
ASPECTS = ["代码结构", "性能瓶颈", "安全漏洞", "可访问性", "SEO 优化"]
TESTS = ["单元测试 (Jest)", "组件测试 (Testing Library)", "E2E 测试 (Playwright)"]
LAYOUTS = ["卡片式", "列表式", "分栏式", "瀑布流", "时间线"]
ANIMATIONS = ["淡入淡出", "滑动", "缩放", "弹性", "骨架屏过渡"]
CHARTS = ["折线图", "柱状图", "饼图", "散点图", "热力图"]
LIBRARIES = ["ECharts", "Recharts", "Chart.js", "D3.js", "Ant Design Charts"]
AUTHS = ["OAuth 第三方登录", "JWT Token", "短信验证码", "多因素认证"]
DASHBOARDS = ["运营数据", "用户分析", "销售统计", "系统监控"]
RESPONSIVE = ["断点适配", "流式布局", "弹性盒布局"]
DESIGNS = ["Material Design", "Apple HIG", "Ant Design 规范", "企业设计系统"]

# 项目上下文模板
CONTEXTS = [
    "这是一个使用 React + TypeScript + Vite 构建的前端项目，使用 Tailwind CSS 作为样式方案。项目采用组件化架构，src/components 存放通用组件，src/pages 存放页面组件。",
    "这是一个 Next.js 14 项目，使用 App Router，TypeScript，shadcn/ui 组件库。项目已有用户认证模块和基础布局。",
    "这是一个 Vue 3 + TypeScript 项目，使用 Pinia 状态管理和 Vue Router。采用 Composition API 风格，Element Plus 作为 UI 库。",
    "这是一个 React Native 项目，使用 Expo 框架，TypeScript，React Navigation 进行页面导航。已有底部 Tab 导航结构。",
    "这是一个 Monorepo 项目，使用 pnpm workspace，包含 web 应用（React）和 admin 应用（Next.js），共享 packages/ui 组件库。",
    "这是一个 Nuxt.js 3 项目，使用 TypeScript，Tailwind CSS。已有 SSR 配置和 API 路由层。",
]


def random_fill(template: str, rng_seed: int) -> str:
    """用确定性方式填充模板变量"""
    import random
    random.seed(rng_seed)
    result = template
    replacements = {
        "{framework}": random.choice(FRAMEWORKS),
        "{css}": random.choice(CSS_OPTIONS),
        "{component}": random.choice(COMPONENTS),
        "{page}": random.choice(PAGES),
        "{feature}": random.choice(FEATURES),
        "{feature1}": random.choice(FEATURES),
        "{feature2}": random.choice(FEATURES),
        "{form}": random.choice(FORMS),
        "{fields}": random.choice(FIELDS),
        "{validation}": random.choice(VALIDATIONS),
        "{bug}": random.choice(BUGS),
        "{aspect}": random.choice(ASPECTS),
        "{test}": random.choice(TESTS),
        "{layout}": random.choice(LAYOUTS),
        "{animation}": random.choice(ANIMATIONS),
        "{chart}": random.choice(CHARTS),
        "{library}": random.choice(LIBRARIES),
        "{data}": random.choice(["销售", "用户活跃", "流量", "性能指标"]),
        "{auth}": random.choice(AUTHS),
        "{dashboard}": random.choice(DASHBOARDS),
        "{widgets}": random.choice(["图表、统计卡片、数据表格", "日历、待办事项、公告", "实时监控、告警列表"]),
        "{pages}": random.choice(["登录、注册、忘记密码", "授权确认、绑定手机", "设置安全问题"]),
        "{props}": random.choice(["size、variant、disabled", "theme、locale、direction", "mode、placement、closable"]),
        "{old}": random.choice(["Class Component", "JavaScript", "Options API", "CSS 文件"]),
        "{new}": random.choice(["Function Component", "TypeScript", "Composition API", "CSS-in-JS"]),
        "{old_pattern}": random.choice(["useState", "any 类型", "内联样式", "hardcoded 字符串"]),
        "{new_pattern}": random.choice(["useReducer", "泛型类型", "CSS 变量", "i18n 国际化"]),
        "{file}": random.choice(["App.tsx", "utils.ts", "api.ts", "store.ts", "routes.tsx"]),
        "{responsive}": random.choice(RESPONSIVE),
        "{style}": random.choice(["颜色方案", "间距系统", "字体排版", "阴影效果"]),
        "{design}": random.choice(DESIGNS),
        "{api}": random.choice(["用户信息", "商品列表", "订单详情", "文件上传"]),
        "{handling}": random.choice(["try-catch", "全局拦截器", "重试机制", "离线缓存"]),
        "{subcomponents}": random.choice(["Header、Body、Footer", "Form、Field、Submit", "List、Item、Empty"]),
        "{quality}": random.choice(["性能", "可维护性", "可测试性", "可复用性"]),
        "{concern}": random.choice(["类型安全", "代码规范", "潜在的 bug", "安全风险"]),
        "{pattern}": random.choice(["console.log", "any 类型", "TODO 注释", "硬编码的 URL"]),
        "{dependency}": random.choice(["lodash", "moment", "axios", "react-router"]),
        "{mobile}": random.choice(["卡片列表", "抽屉菜单", "底部弹窗", "全屏展示"]),
        "{desktop}": random.choice(["表格展示", "侧边栏导航", "弹窗形式", "分栏布局"]),
        "{widgets}": random.choice(["图表、统计卡片、数据表格", "日历、待办、公告", "监控面板、告警列表"]),
    }
    for key, value in replacements.items():
        result = result.replace(key, value)
    return result


def generate_plan(client: anthropic.Anthropic, task: str, context: str) -> dict | None:
    """调用 Claude API 为任务生成结构化计划"""
    user_msg = f"任务：{task}\n\n项目上下文：\n{context}"

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            system=PLANNER_SYSTEM,
            messages=[{"role": "user", "content": user_msg}],
            temperature=0.7,
        )
        text = response.content[0].text

        # 从响应中提取 JSON
        # 尝试直接解析
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        # 尝试从 markdown 代码块中提取
        import re
        json_match = re.search(r'```(?:json)?\s*\n(.*?)\n```', text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass

        # 尝试找到 { ... } 之间的内容
        brace_start = text.find('{')
        brace_end = text.rfind('}')
        if brace_start != -1 and brace_end != -1:
            try:
                return json.loads(text[brace_start:brace_end + 1])
            except json.JSONDecodeError:
                pass

        print(f"  [WARN] 无法解析 JSON 响应，跳过此条数据")
        return None

    except Exception as e:
        print(f"  [ERROR] API 调用失败: {e}")
        return None


def plan_to_alpaca(task: str, context: str, plan: dict) -> dict:
    """将任务和计划转换为 Alpaca 格式"""
    instruction = (
        "你是一个资深前端工程师和项目规划专家。请根据以下任务描述和项目上下文，"
        "生成一个结构化的执行计划。计划应按阶段组织（阶段1-分析、阶段2-创建、"
        "阶段3-安装、阶段4-验证、阶段5-启动、阶段6-浏览器验证、阶段7-仓库管理），"
        "每个步骤包含 description（描述）、action（动作类型）、phase（所属阶段）。"
        "同时提供 risks（潜在风险）和 alternatives（备选方案）。\n\n"
        "可用的动作类型: read_file, list_directory, create_file, apply_patch, "
        "search_code, get_ast, run_command, browser_navigate, browser_screenshot, "
        "get_page_structure, browser_click, browser_type"
    )

    input_text = f"任务：{task}\n\n项目上下文：\n{context}"
    output_text = json.dumps(plan, ensure_ascii=False, indent=2)

    return {
        "instruction": instruction,
        "input": input_text,
        "output": output_text,
    }


def main():
    parser = argparse.ArgumentParser(description="FrontAgent Planner 合成数据生成")
    parser.add_argument("--count", type=int, default=100, help="生成数据条数")
    parser.add_argument("--output", type=str, default="train.json", help="输出文件名")
    parser.add_argument("--api-key", type=str, default=None, help="Anthropic API Key（也可用环境变量）")
    args = parser.parse_args()

    api_key = args.api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("错误：请设置 ANTHROPIC_API_KEY 环境变量或传入 --api-key 参数")
        return

    client = anthropic.Anthropic(api_key=api_key)
    output_path = Path(__file__).parent / args.output

    dataset = []
    print(f"开始生成 {args.count} 条训练数据...")

    for i in range(args.count):
        # 确定性地选择任务模板和上下文
        task_template = TASK_TEMPLATES[i % len(TASK_TEMPLATES)]
        context = CONTEXTS[i % len(CONTEXTS)]

        task = random_fill(task_template, rng_seed=i * 1000 + i)
        print(f"[{i + 1}/{args.count}] 任务: {task[:60]}...")

        plan = generate_plan(client, task, context)
        if plan is None:
            continue

        # 验证基本结构
        if "summary" not in plan or "stepOutlines" not in plan:
            print(f"  [WARN] 计划缺少必要字段，跳过")
            continue

        sample = plan_to_alpaca(task, context, plan)
        dataset.append(sample)

        # 避免速率限制
        time.sleep(0.5)

    # 写入文件
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)

    print(f"\n完成！生成 {len(dataset)}/{args.count} 条有效数据，保存到 {output_path}")


if __name__ == "__main__":
    main()
