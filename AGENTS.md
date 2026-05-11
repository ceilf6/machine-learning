# 机器学习课程仓库

## 工程结构

- `./lundechen-machine_learning_2026_spring/`：课程仓库，最高可信源
  - `./lundechen-machine_learning_2026_spring/session-*/`：每次课程的资料目录，例如 `session-1/`
- `./wechat-session/`：课程群聊记录，按 `MM-DD/` 目录组织
- `./tasks/`：作业回答
- `./tasks-list.md`：待完成作业

## 开发规范

1. 不确定的问题一定要向用户提问。
2. 每次开发或解析任务前，先同步课程子模块：
   1. 进入 `./lundechen-machine_learning_2026_spring/`，确认工作区状态；如果存在未提交改动、分支不明确或同步方式不确定，先向用户提问。
   2. 从 `upstream` 上游仓库拉取最新情况，以最新的 `session-*` 资料作为任务来源基础。
3. 维护任务列表：
   1. 任务来源优先级以 `./lundechen-machine_learning_2026_spring/session-*/` 为准。
      `./wechat-session/` 只作为课程子模块 session 任务的辅助信息，用于补充提交要求、时间、说明或群内答疑。
      如果微信群记录与子模块 session 内容冲突，优先采用子模块 session；仍不确定时向用户提问。
   2. 将任务解析到 `./tasks-list.md`。
      如果需要查看任务详情，先查找课程子模块对应 `session-*` 目录，再用 `./wechat-session/` 辅助确认。
      **不需要提交到微信群的任务自动标记为已完成。**
   3. 任务使用全局连续序号；完成任务后只标 `[x]`，不删除。
      ```md
      ## 05-09 课程任务
      - [ ] 1. 需要提交到微信群且未完成的任务
      - [x] 2. 不需要提交到微信群的任务
      - [x] 3. 需要提交到微信群且完成的任务
      ```
