
# 一、AI 招聘 Agent 项目完整项目文档
# AI Recruitment Agent —— 企业级 AI 招聘智能体

## 1. 项目概述

### 1.1 项目名称

AI Recruitment Agent

### 1.2 项目定位

构建一个基于 **LangGraph + LLM + RAG + Elasticsearch + Milvus + Rerank** 的企业级 AI 招聘智能体。

系统能够理解用户自然语言招聘需求，自动完成：

```text
用户需求
  ↓
Intent 意图识别
  ↓
Planner 任务规划
  ↓
Tool Calling
  ↓
Hybrid RAG
  ├── Elasticsearch
  └── Milvus
  ↓
Fusion
  ↓
Rerank
  ↓
Candidate / Job Score
  ↓
Reflection
  ↓
重新规划 / 最终回答
```

最终实现一个真正具备：

* 自主规划
* 工具调用
* 多阶段检索
* 语义匹配
* 结果重排
* 可解释评分
* 自我反思
* 循环执行
* 状态持久化
* Human-in-the-loop

能力的 AI Recruitment Agent。

---

# 2. 项目目标

## 2.1 用户端目标

用户可以直接通过自然语言与 AI 招聘顾问交流。

例如：

```text
帮我找上海的高级Java开发岗位，
5年以上经验，薪资30K以上，
最好有Spring Cloud、RAG、LangGraph或者AI Agent经验。
```

Agent 自动完成：

```text
理解需求
→ 提取结构化条件
→ 获取用户画像
→ 查询岗位
→ ES检索
→ Milvus语义检索
→ 结果融合
→ Rerank
→ 匹配评分
→ Reflection
→ 返回推荐结果
```

---

# 3. 核心技术架构

## 3.1 总体架构

```text
                         用户
                          │
                          ▼
                    Web / App / 小程序
                          │
                          ▼
                     API Gateway
                          │
             ┌────────────┴────────────┐
             │                         │
             ▼                         ▼
      Java Business Services       AI Agent Service
             │                         │
             │                    FastAPI
             │                         │
             │                    LangGraph
             │                         │
             │             ┌───────────┼───────────┐
             │             │           │           │
             │            Tool        RAG        Memory
             │             │           │           │
             │             │       ┌───┴───┐       │
             │             │       │       │       │
             │             │      ES    Milvus   Redis
             │             │       │       │
             │             │       └───┬───┘
             │             │           │
             │             │         Rerank
             │             │           │
             │             └───────────┤
             │                         │
             │                        LLM
             │                         │
             └─────────────────────────┘
```

---

# 4. 技术栈

## 4.1 Java业务层

```text
Java 8+
Spring Boot
Spring Cloud
Spring Cloud Gateway
MyBatis-Plus
MySQL
Redis
Kafka
```

负责：

```text
用户
简历
岗位
企业
招聘流程
投递记录
面试记录
```

---

## 4.2 AI服务

```text
Python 3.11+
FastAPI
LangGraph
LangChain
Pydantic
```

---

## 4.3 LLM

第一阶段：

```text
Qwen
```

推荐抽象成统一接口：

```text
LLMProvider
```

方便后续切换：

```text
Qwen
DeepSeek
OpenAI
Claude
```

---

## 4.4 Embedding

```text
Qwen embedding
```

统一封装：

```text
EmbeddingService
```

---

## 4.5 Vector Database

```text
Milvus
```

保存：

```text
岗位向量
简历向量
技能向量
公司描述向量
JD Chunk
Resume Chunk
```

---

## 4.6 Search Engine

```text
Elasticsearch
```

负责：

```text
关键词搜索
字段过滤
范围查询
技能匹配
薪资过滤
城市过滤
工作经验过滤
岗位状态过滤
```

---

## 4.7 Rerank

支持：

```text
Qwen Rerank
BGE Reranker
其他可插拔Reranker
```

---

# 5. 核心业务流程

## 5.1 用户请求

用户输入：

```text
帮我找上海5年以上Java开发，
薪资30K以上，最好有AI Agent经验。
```

---

## 5.2 Intent Recognition

LLM 将自然语言转换为：

```json
{
  "intent": "job_search",
  "city": "上海",
  "keywords": [
    "Java",
    "AI Agent"
  ],
  "min_experience": 5,
  "min_salary": 30000,
  "skills": [
    "Java",
    "AI Agent"
  ]
}
```

---

# 6. LangGraph State

核心状态：

```python
class RecruitmentState(TypedDict, total=False):

    user_id: str

    query: str

    intent: dict

    plan: list[str]

    tool_results: dict

    es_results: list[dict]

    milvus_results: list[dict]

    fused_results: list[dict]

    reranked_results: list[dict]

    scored_jobs: list[dict]

    reflection: dict

    final_answer: str

    retry_count: int

    trace: list[str]
```

State 是整个 Agent 的共享上下文。

---

# 7. LangGraph Workflow

## 7.1 Graph

```text
START
  │
  ▼
Intent
  │
  ▼
Planner
  │
  ▼
Tool
  │
  ▼
Retrieval
  │
  ▼
Fusion
  │
  ▼
Rerank
  │
  ▼
Score
  │
  ▼
Reflection
  │
  ├──────────────┐
  │              │
  ▼              ▼
Planner         Final
  │              │
  └── Loop       ▼
                 END
```

---

# 8. Intent Node

职责：

```text
自然语言
→
结构化招聘条件
```

需要识别：

```text
intent
city
salary
experience
education
skills
industry
job_type
company_type
remote
keywords
```

必须使用 Pydantic 对 LLM 输出进行结构化约束。

---

# 9. Planner Node

根据 Intent 生成执行计划。

例如：

```json
{
  "steps": [
    "get_user_profile",
    "get_resume",
    "search_es",
    "search_milvus",
    "fusion",
    "rerank",
    "score",
    "reflection"
  ]
}
```

Planner 不应该产生无意义步骤。

需要根据实际 Intent 动态决定是否需要：

```text
用户画像
简历
岗位搜索
公司搜索
薪资搜索
```

---

# 10. Tool System

## 10.1 Tool列表

```text
get_user_profile
get_resume
get_job_detail
search_jobs
search_company
search_salary
match_candidate_job
score_candidate
generate_interview_questions
```

---

## 10.2 Tool设计原则

所有 Tool 必须：

```text
输入Schema明确
输出Schema明确
异常可控
日志可追踪
超时可控
可单元测试
```

禁止让 LLM 直接访问数据库。

正确架构：

```text
LLM
 ↓
Tool
 ↓
Service
 ↓
Repository
 ↓
Database
```

---

# 11. Hybrid RAG

系统采用：

```text
ES + Milvus
```

而不是单独使用 Vector Search。

---

## 11.1 Elasticsearch

负责：

```text
城市
薪资
经验
学历
岗位名称
技能
公司
行业
```

例如：

```json
{
  "bool": {
    "filter": [
      {
        "term": {
          "city.keyword": "上海"
        }
      },
      {
        "range": {
          "experience_years": {
            "gte": 5
          }
        }
      },
      {
        "range": {
          "salary_min": {
            "gte": 30000
          }
        }
      }
    ]
  }
}
```

---

# 12. Milvus

负责语义检索。

用户：

```text
熟悉AI Agent开发
```

可以召回：

```text
LangGraph
LangChain
RAG
Agent
LLM Application
智能体开发
```

---

# 13. Embedding流程

```text
岗位JD
 ↓
文本清洗
 ↓
Chunk
 ↓
Embedding
 ↓
Milvus
```

简历：

```text
Resume PDF
 ↓
Parser
 ↓
结构化
 ↓
Chunk
 ↓
Embedding
 ↓
Milvus
```

---

# 14. Fusion

ES 与 Milvus 的 Score 不可直接比较。

采用：

```text
RRF
```

公式：

```text
RRF(d) = Σ 1 / (k + rank(d))
```

最终生成：

```text
fused_results
```

---

# 15. Rerank

Fusion：

```text
Top 50
```

进入 Rerank：

```text
Top 50
 ↓
Reranker
 ↓
Top 20
```

Rerank 输入：

```text
Query
+
Candidate Documents
```

输出：

```text
document
rerank_score
```

---

# 16. Job Match Score

最终匹配分不能完全依赖 LLM。

采用确定性评分：

```text
总分 =

技能匹配 × 40%
+
经验匹配 × 20%
+
岗位相关性 × 25%
+
薪资匹配 × 15%
```

例如：

```text
技能匹配：90
经验匹配：100
岗位相关性：92
薪资匹配：80

最终：

90 × 0.4
+
100 × 0.2
+
92 × 0.25
+
80 × 0.15

= 91
```

---

# 17. Reflection

Reflection 判断：

```text
结果是否满足用户需求？
```

例如：

```json
{
  "pass": true,
  "retry": false,
  "reason": "找到多个满足核心条件的岗位"
}
```

如果失败：

```json
{
  "pass": false,
  "retry": true,
  "reason": "满足薪资和经验条件的岗位不足"
}
```

重新：

```text
Reflection
 ↓
Planner
 ↓
Retrieval
 ↓
Rerank
 ↓
Score
```

---

# 18. 防止无限Loop

必须设计：

```text
MAX_RETRY = 2
```

当：

```text
retry_count >= MAX_RETRY
```

必须：

```text
停止Loop
 ↓
返回当前最佳结果
```

禁止 Agent 无限循环。

---

# 19. Final Answer

最终 LLM 输入：

```text
用户需求
+
用户画像
+
Top N岗位
+
匹配分数
+
匹配原因
+
Reflection结果
```

生成：

```text
岗位名称
公司
地点
薪资
匹配度
匹配原因
风险
建议
```

---

# 20. Memory

分为两种。

## 20.1 Short-term Memory

保存当前会话：

```text
query
intent
plan
retrieval
score
```

---

## 20.2 Long-term Memory

保存用户长期偏好：

```text
期望城市
期望薪资
技术栈
工作年限
行业偏好
公司偏好
岗位偏好
拒绝记录
```

存储：

```text
Redis
+
MySQL
```

---

# 21. Resume RAG

用户上传：

```text
PDF / DOCX
```

处理：

```text
文件
 ↓
Parser
 ↓
文本清洗
 ↓
结构化
 ↓
Chunk
 ↓
Embedding
 ↓
Milvus
```

同时保存结构化简历：

```text
MySQL
```

---

# 22. 数据模型

## User

```text
id
name
phone
email
city
created_at
updated_at
```

## Resume

```text
id
user_id
content
education
experience_years
skills
projects
created_at
updated_at
```

## Job

```text
id
company_id
title
description
city
salary_min
salary_max
experience_min
experience_max
education
skills
status
created_at
updated_at
```

## Company

```text
id
name
industry
scale
city
description
```

## Application

```text
id
user_id
job_id
status
created_at
updated_at
```

---

# 23. ES Index

建议：

```text
job_index
resume_index
company_index
```

Job Mapping：

```text
id
title
description
skills
city
salary_min
salary_max
experience_min
experience_max
education
company_id
```

---

# 24. Milvus Collection

建议：

```text
job_vectors
resume_vectors
skill_vectors
```

Job Vector：

```text
job_id
chunk_id
text
embedding
metadata
```

---

# 25. API

## Chat

```http
POST /api/v1/agent/chat
```

Request：

```json
{
  "user_id": "10001",
  "message": "帮我找上海30K以上的Java岗位"
}
```

Response：

```json
{
  "conversation_id": "xxx",
  "answer": "...",
  "jobs": [],
  "trace_id": "xxx"
}
```

---

## Resume Upload

```http
POST /api/v1/resume/upload
```

---

## Job Search

```http
POST /api/v1/jobs/search
```

---

## Job Match

```http
POST /api/v1/jobs/match
```

---

# 26. 项目目录

```text
ai-recruitment-agent/
│
├── app/
│   ├── main.py
│   │
│   ├── agent/
│   │   ├── graph.py
│   │   ├── state.py
│   │   ├── nodes/
│   │   │   ├── intent.py
│   │   │   ├── planner.py
│   │   │   ├── tool.py
│   │   │   ├── retrieval.py
│   │   │   ├── fusion.py
│   │   │   ├── rerank.py
│   │   │   ├── score.py
│   │   │   ├── reflection.py
│   │   │   └── final.py
│   │   └── routing.py
│   │
│   ├── tools/
│   │   ├── user.py
│   │   ├── resume.py
│   │   ├── job.py
│   │   └── company.py
│   │
│   ├── retrieval/
│   │   ├── es/
│   │   ├── milvus/
│   │   ├── embedding/
│   │   ├── rerank/
│   │   └── fusion/
│   │
│   ├── memory/
│   │   ├── short_term.py
│   │   └── long_term.py
│   │
│   ├── llm/
│   │   ├── base.py
│   │   ├── qwen.py
│   │   └── factory.py
│   │
│   ├── schemas/
│   │   ├── intent.py
│   │   ├── job.py
│   │   ├── resume.py
│   │   └── response.py
│   │
│   ├── services/
│   └── config/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── scripts/
│   ├── init_es.py
│   ├── init_milvus.py
│   └── seed_data.py
│
├── docker/
│
├── docs/
│
├── .env.example
├── docker-compose.yml
├── pyproject.toml
└── README.md
```

---

# 27. 测试要求

必须覆盖：

```text
Intent测试
Planner测试
Tool测试
ES测试
Milvus测试
RRF测试
Rerank测试
Score测试
Reflection测试
Graph测试
API测试
E2E测试
```

至少包含：

```text
正常搜索
无结果
部分满足
完全满足
复杂需求
多轮对话
Tool失败
ES失败
Milvus失败
LLM失败
Rerank失败
Reflection Loop
达到最大重试次数
```

---

# 28. 可观测性

所有 Agent 执行必须记录：

```text
trace_id
conversation_id
user_id
node
input
output
duration
token_usage
error
retry_count
```

推荐：

```text
LangSmith
```

进行：

```text
Trace
Debug
Evaluation
Latency
Token
Agent trajectory
```

---

# 29. 生产级要求

代码必须满足：

```text
类型安全
异常处理
日志
配置管理
环境隔离
Docker
测试
API文档
健康检查
超时
重试
限流
熔断
```

禁止：

```text
硬编码API Key
硬编码数据库连接
LLM直接操作数据库
无限Agent Loop
Node之间大量共享全局变量
没有异常处理的Tool
没有测试的核心算法
```

---

# 30. 最终验收标准

项目完成必须能够执行：

```text
用户
 ↓
POST /api/v1/agent/chat
 ↓
LangGraph
 ↓
Intent
 ↓
Planner
 ↓
Tool
 ↓
ES
 ↓
Milvus
 ↓
Fusion
 ↓
Rerank
 ↓
Score
 ↓
Reflection
 ↓
Final
 ↓
JSON Response
```

同时能够看到完整 Trace：

```text
START
→ intent
→ planner
→ tool
→ retrieval
→ fusion
→ rerank
→ score
→ reflection
→ final
→ END
```

如果 Reflection 失败：

```text
reflection
→ planner
→ retrieval
→ rerank
→ score
→ reflection
→ final
```

整个项目必须能够：

```text
启动
运行
测试
Debug
扩展
部署
```

并最终形成一个可以用于：

```text
AI Agent开发岗位面试
项目展示
技术简历
实际Demo
后续生产化
```

的完整 AI Recruitment Agent。

## 二、给 Claude Code 的 Loop Engineering 总提示词

这个提示词不要只让 Claude Code “写代码”。

核心要求是：

> **让 Claude Code 自己检查 → 实现 → 运行 → 测试 → 找问题 → 修复 → 再测试 → 继续下一阶段，直到项目达到验收标准。**

你可以直接把下面这段交给 Claude Code。

# Claude Code Loop Engineering Master Prompt

你现在是这个项目的 Principal AI Engineer + Senior Backend Engineer + QA Engineer + DevOps Engineer。

你的任务不是给我写方案，而是**直接在当前项目目录中完成整个 AI Recruitment Agent 项目**。

项目目标：

构建一个真正可以运行、测试、Debug 和持续扩展的企业级 AI 招聘 Agent。

核心技术：

* Python 3.11+
* FastAPI
* LangGraph
* LangChain
* Pydantic
* Qwen / 可插拔 LLM
* Elasticsearch
* Milvus
* Redis
* MySQL
* Reranker
* Docker Compose
* pytest
* LangSmith 可观测性

核心 Agent Workflow 必须实现：

```text
用户需求
 ↓
Intent Recognition
 ↓
Planner
 ↓
Tool Calling
 ↓
Hybrid RAG
 ├── Elasticsearch
 └── Milvus
 ↓
Fusion / RRF
 ↓
Rerank
 ↓
Score
 ↓
Reflection
 ├── 满足 → Final
 └── 不满足 → Planner → Retrieval → Rerank → Score → Reflection
 ↓
Final Answer
```

---

# 第一原则：不要停留在设计阶段

不要只给我：

* 架构图
* 代码片段
* TODO
* 伪代码
* “这里以后实现”
* “需要你自己配置”
* “可以进一步完善”

你的目标是：

> **持续修改项目文件，直到项目真正达到验收标准。**

如果当前环境缺少真实 API Key、ES、Milvus 或其他外部服务：

1. 不要因此停止。
2. 先实现完整接口。
3. 提供 Mock/Fake 实现。
4. 编写测试。
5. 使用 Docker 启动能够启动的基础设施。
6. 最后进行真实环境兼容设计。
7. 明确哪些测试属于 Mock Test，哪些属于 Integration Test。

---

# 第二原则：Loop Engineering

严格按照下面的循环执行：

```text
Inspect
 ↓
Plan
 ↓
Implement
 ↓
Run
 ↓
Test
 ↓
Observe Failure
 ↓
Diagnose Root Cause
 ↓
Fix
 ↓
Run Again
 ↓
Regression Test
 ↓
Review
 ↓
Continue
```

禁止：

```text
写完代码
↓
告诉我“已经完成”
```

必须实际：

```text
代码
→ 执行
→ 测试
→ 修复
→ 再执行
```

---

# 第一步：检查当前项目

首先检查：

```text
pwd
find .
git status
```

然后检查：

```text
Python版本
Node版本
Docker
Docker Compose
项目目录
已有代码
已有配置
已有测试
```

不要删除现有有效代码。

如果项目已经存在代码：

> **优先在现有架构上增量实现，而不是推倒重来。**

---

# 第二步：建立项目基线

完成：

```text
pyproject.toml
README.md
.env.example
.gitignore
docker-compose.yml
```

建立：

```text
app/
tests/
scripts/
docs/
```

确保：

```bash
python -m pytest
```

可以运行。

---

# 第三步：实现 LangGraph State

实现：

```python
RecruitmentState
```

至少包含：

```text
user_id
query
intent
plan
tool_results
es_results
milvus_results
fused_results
reranked_results
scored_jobs
reflection
final_answer
retry_count
trace
```

要求：

* TypedDict 或 Pydantic
* 类型清晰
* 不使用 Any 滥用
* 有默认值
* 有测试

---

# 第四步：实现 LangGraph

必须真正使用：

```text
StateGraph
Node
Edge
Conditional Edge
START
END
```

实现：

```text
intent
planner
tool
retrieval
fusion
rerank
score
reflection
final
```

Graph 必须可以：

```text
正常执行
```

以及：

```text
Reflection → Planner
```

循环。

必须设置：

```text
MAX_RETRY
```

防止无限循环。

---

# 第五步：实现 Intent Recognition

用户：

```text
帮我找上海5年以上Java开发，
30K以上，最好有AI Agent经验
```

必须转换成结构化数据。

例如：

```json
{
  "intent": "job_search",
  "city": "上海",
  "min_experience": 5,
  "min_salary": 30000,
  "skills": [
    "Java",
    "AI Agent"
  ]
}
```

必须使用：

```text
Pydantic
Structured Output
```

不要依赖：

```text
字符串解析
正则表达式
```

作为主要方案。

必须编写：

```text
正常需求测试
复杂需求测试
缺少条件测试
无关需求测试
```

---

# 第六步：实现 Planner

Planner 根据 Intent 生成：

```text
Execution Plan
```

不能只是固定返回数组。

必须能够根据需求动态判断：

```text
是否需要用户画像
是否需要简历
是否需要岗位搜索
是否需要公司信息
是否需要薪资信息
```

Planner 输出必须结构化。

---

# 第七步：实现 Tools

实现至少：

```text
get_user_profile
get_resume
search_jobs
get_job_detail
search_company
search_salary
match_candidate_job
score_candidate
generate_interview_questions
```

每一个 Tool：

```text
输入Schema
输出Schema
异常处理
日志
单元测试
```

Tool 不允许直接被 HTTP 层调用数据库。

必须：

```text
Tool
 ↓
Service
 ↓
Repository
 ↓
Database
```

---

# 第八步：实现 Elasticsearch

创建：

```text
job_index
resume_index
company_index
```

实现：

```text
keyword search
filter
range
city
salary
experience
education
skills
```

必须支持：

```text
结构化条件
+
全文搜索
```

提供：

```text
Mock Repository
Real Elasticsearch Repository
```

通过配置切换。

---

# 第九步：实现 Milvus

实现：

```text
EmbeddingService
MilvusRepository
```

支持：

```text
job_vectors
resume_vectors
skill_vectors
```

流程：

```text
Query
 ↓
Embedding
 ↓
Milvus
 ↓
Top K
```

必须有：

```text
Mock Milvus
Real Milvus
```

两套实现。

---

# 第十步：实现 Hybrid Retrieval

必须实现：

```text
ES Retrieval
+
Milvus Retrieval
```

然后：

```text
Fusion
```

实现 RRF：

```text
RRF(d) = Σ 1 / (k + rank(d))
```

必须对：

```text
重复Document
缺失Document
空结果
ES失败
Milvus失败
```

进行测试。

---

# 第十一步：实现 Rerank

设计：

```text
Reranker interface
```

至少：

```text
MockReranker
RealReranker
```

输入：

```text
query
documents
```

输出：

```text
document_id
rerank_score
```

流程：

```text
ES + Milvus
 ↓
Top 50
 ↓
Rerank
 ↓
Top 20
```

---

# 第十二步：实现 Candidate / Job Score

必须使用确定性评分。

默认：

```text
Skills          40%
Experience      20%
Relevance       25%
Salary          15%
```

必须：

```text
总分100
```

并返回：

```json
{
  "score": 91,
  "skill_score": 90,
  "experience_score": 100,
  "relevance_score": 92,
  "salary_score": 80,
  "reasons": []
}
```

要求：

> 评分逻辑不能完全交给 LLM。

---

# 第十三步：实现 Reflection

Reflection 必须判断：

```text
结果是否满足用户需求？
```

例如：

```json
{
  "pass": true,
  "retry": false,
  "reason": "满足核心招聘条件"
}
```

失败：

```json
{
  "pass": false,
  "retry": true,
  "reason": "满足条件的岗位不足"
}
```

必须能够触发：

```text
Reflection
 ↓
Planner
 ↓
Retrieval
```

形成真实 Graph Loop。

---

# 第十四步：防止无限循环

必须实现：

```python
MAX_RETRY = 2
```

如果：

```text
retry_count >= MAX_RETRY
```

则：

```text
停止循环
 ↓
选择当前最佳结果
 ↓
Final
```

必须写测试证明不会无限循环。

---

# 第十五步：实现 Final Answer

Final Node 调用 LLM。

输入：

```text
用户需求
用户画像
Top N岗位
匹配分数
匹配原因
Reflection结果
```

输出：

```text
推荐岗位
公司
地点
薪资
匹配度
匹配原因
风险
建议
```

要求：

> LLM 只能基于检索结果生成答案，不允许凭空编造岗位。

---

# 第十六步：实现 FastAPI

实现：

```http
POST /api/v1/agent/chat
```

Request：

```json
{
  "user_id": "10001",
  "message": "帮我找上海30K以上Java岗位"
}
```

Response：

```json
{
  "conversation_id": "xxx",
  "answer": "...",
  "jobs": [],
  "trace_id": "xxx"
}
```

同时实现：

```text
GET /health
GET /ready
```

---

# 第十七步：实现 Memory

实现：

```text
ShortTermMemory
LongTermMemory
```

Short Term：

```text
当前Agent State
```

Long Term：

```text
用户城市偏好
薪资偏好
技能
岗位偏好
行业偏好
```

提供：

```text
MockMemory
RedisMemory
```

---

# 第十八步：实现 Resume RAG

支持：

```text
PDF
DOCX
TXT
```

流程：

```text
Upload
 ↓
Parser
 ↓
Clean
 ↓
Structure
 ↓
Chunk
 ↓
Embedding
 ↓
Milvus
```

结构化数据：

```text
MySQL
```

向量数据：

```text
Milvus
```

---

# 第十九步：Docker

提供：

```text
docker-compose.yml
```

至少包含：

```text
MySQL
Redis
Elasticsearch
Milvus
```

如果 Milvus 依赖：

```text
etcd
MinIO
```

也一起配置。

要求：

```bash
docker compose up -d
```

能够正常启动基础设施。

实现：

```text
healthcheck
```

---

# 第二十步：测试

必须执行：

```bash
pytest
```

测试覆盖：

```text
State
Intent
Planner
Tools
ES
Milvus
Fusion
RRF
Rerank
Score
Reflection
Graph
Memory
API
E2E
```

至少测试：

```text
正常招聘需求
复杂招聘需求
没有岗位
只有部分岗位满足
ES没有结果
Milvus没有结果
ES异常
Milvus异常
Rerank异常
LLM异常
Tool异常
Reflection retry
MAX_RETRY
最终回答
```

---

# 第二十一步：真实E2E测试

最终必须运行：

```text
POST /api/v1/agent/chat
```

至少执行：

```text
案例1：
上海5年以上Java，30K以上

案例2：
Java + Spring Cloud + AI Agent

案例3：
没有满足条件的岗位

案例4：
非常复杂的招聘需求
```

检查：

```text
HTTP Status
Response Schema
Graph执行
Tool执行
ES
Milvus
Rerank
Score
Reflection
Final
```

---

# 第二十二步：故障测试

主动制造：

```text
ES unavailable
Milvus unavailable
Redis unavailable
LLM timeout
Tool exception
Rerank exception
```

系统不能直接崩溃。

必须：

```text
记录日志
捕获异常
返回可理解错误
或者降级
```

例如：

```text
Milvus失败
 ↓
ES继续工作
 ↓
返回关键词检索结果
```

---

# 第二十三步：代码质量检查

完成后执行：

```bash
ruff check .
```

如果项目使用：

```text
mypy
```

也执行：

```bash
mypy app
```

然后：

```bash
pytest
```

最后：

```bash
python -m compileall app
```

解决所有错误。

禁止留下：

```text
TODO
FIXME
pass
NotImplementedError
假的实现
```

除非该位置明确属于可插拔 Provider，并且已经存在真实实现。

---

# 第二十四步：安全检查

检查：

```text
API Key
数据库密码
Redis密码
JWT Secret
```

禁止写死在代码。

必须使用：

```text
.env
environment variables
```

Git 中禁止出现：

```text
.env
真实API Key
真实密码
```

---

# 第二十五步：最终项目审查

完成所有功能后，不要立即结束。

重新从用户角度执行一次完整流程：

```text
用户
 ↓
API
 ↓
LangGraph
 ↓
Intent
 ↓
Planner
 ↓
Tool
 ↓
ES
 ↓
Milvus
 ↓
Fusion
 ↓
Rerank
 ↓
Score
 ↓
Reflection
 ↓
Final
```

检查每一个节点：

```text
输入是否正确？
输出是否正确？
State是否正确更新？
异常是否处理？
日志是否存在？
测试是否覆盖？
```

---

# 第二十六步：最终验收

只有同时满足以下条件，才能宣布项目完成：

```text
[ ] 项目可以启动
[ ] FastAPI可以启动
[ ] /health正常
[ ] LangGraph可以执行
[ ] Intent正常
[ ] Planner正常
[ ] Tool正常
[ ] ES正常
[ ] Milvus正常
[ ] Hybrid Retrieval正常
[ ] RRF正常
[ ] Rerank正常
[ ] Score正常
[ ] Reflection正常
[ ] Reflection Loop正常
[ ] MAX_RETRY正常
[ ] Final正常
[ ] Memory正常
[ ] Resume RAG正常
[ ] Docker正常
[ ] pytest全部通过
[ ] ruff通过
[ ] compileall通过
[ ] 无明显TODO
[ ] 无硬编码Secret
[ ] API可以进行E2E测试
```

---

# 最重要的执行规则

你必须把自己当成一个持续工作的工程 Agent。

如果测试失败：

```text
不要告诉我失败了。
```

而应该：

```text
分析失败原因
 ↓
修改代码
 ↓
重新运行
 ↓
继续修复
```

如果发现架构问题：

```text
不要停下来问我是否修改。
```

在不违反核心需求的前提下：

```text
选择合理方案
 ↓
实施
 ↓
测试
```

如果发现需求存在多个合理实现：

```text
优先选择：
可维护
可测试
可扩展
生产可用
符合Python生态
符合LangGraph最佳实践
```

---

# 最终输出要求

整个 Loop Engineering 完成后，只向我汇报：

```text
1. 项目最终完成情况
2. 最终项目目录
3. 核心架构
4. LangGraph流程
5. 已实现功能
6. 测试结果
7. Docker运行结果
8. E2E测试结果
9. 当前已知限制
10. 如何启动项目
11. 下一阶段可以继续优化的内容
```

不要在中途因为：

```text
“需要确认”
“可以继续”
“是否需要我实现”
“你是否希望”
```

而停止。

**除非遇到真正无法自行解决的外部权限、凭证或不可恢复环境问题，否则持续 Loop Engineering，直到达到最终验收标准。**

现在开始执行。

第一步：

```text
Inspect 当前项目
```

然后立即进入：

```text
Inspect → Plan → Implement → Run → Test → Fix → Regression → Review
```

**不要只输出计划，直接开始修改项目。**

## 三、我建议你这样让 Claude Code 执行

不要一次把整个项目扔给 Claude Code 后就不管。最适合你的方式是：

```text
第一轮：
项目初始化 + LangGraph骨架

第二轮：
Intent + Planner + Tool

第三轮：
ES + Milvus + Embedding

第四轮：
Fusion + Rerank + Score

第五轮：
Reflection + Loop

第六轮：
Memory + Resume RAG

第七轮：
FastAPI + Docker

第八轮：
测试 + E2E + 故障测试

第九轮：
代码审查 + 性能优化 + 文档
```

但**上面的 Master Prompt 已经要求 Claude Code 自己 Loop**，所以正常情况下你只需要把它作为总指令，然后让它持续执行。

## 四、最关键的一点

你这个项目不要做成：

```text
LangGraph
   ↓
调用几个LLM
   ↓
返回答案
```

而要真正做成：

```text
             ┌──────────────────────────────┐
             │          LangGraph            │
             │                              │
用户 → Intent → Planner → Tool → Retrieval  │
             │                    ↓         │
             │              ES + Milvus     │
             │                    ↓         │
             │                 Fusion       │
             │                    ↓         │
             │                 Rerank       │
             │                    ↓         │
             │                  Score        │
             │                    ↓         │
             │               Reflection     │
             │                ↙       ↘     │
             │            Retry          Final│
             │             │                 │
             │             └──→ Planner      │
             └──────────────────────────────┘
```

**这条链路才是你这个项目的灵魂。**

尤其是面试时，你可以把它浓缩成一句：

> **LangGraph 在这个项目里不是用来“调用大模型”的，而是作为 Agent 的 Workflow Orchestrator，负责维护 State、编排 Node、进行条件路由、执行 Tool、控制 RAG 流程，并通过 Reflection 实现可控的 Agent Loop。**

这句话非常重要。
