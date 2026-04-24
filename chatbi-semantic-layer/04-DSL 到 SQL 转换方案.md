# 04-DSL 到 SQL 转换方案

## 📖 概述

本文档描述 DSL（领域特定语言）到 SQL 的转换引擎设计，包括语法解析、语义校验、查询优化和 SQL 生成等核心模块。

---

## 🎯 设计目标

1. **准确性** - SQL 生成准确率 > 99%
2. **性能** - 转换延迟 < 100ms
3. **兼容性** - 支持多种 SQL 方言（Hive/MySQL/Presto）
4. **可优化** - 支持查询优化和重写

---

## 🏗️ 整体架构

```
DSL 输入
  ↓
┌───────────────────┐
│   DSL 解析器       │
│ - 词法分析        │
│ - 语法分析        │
│ - AST 构建        │
└───────────────────┘
  ↓
┌───────────────────┐
│   语义校验器       │
│ - 类型检查        │
│ - 权限验证        │
│ - 逻辑校验        │
└───────────────────┘
  ↓
┌───────────────────┐
│   查询优化器       │
│ - 谓词下推        │
│ - 列裁剪          │
│ - 连接优化        │
└───────────────────┘
  ↓
┌───────────────────┐
│   SQL 生成器       │
│ - 方言适配        │
│ - 模板渲染        │
│ - 格式化输出      │
└───────────────────┘
  ↓
SQL 输出
```

---

## 🔧 DSL 语法设计

### 1. 基本语法

```
<query> ::= SELECT <metrics>
            [WHERE <conditions>]
            [GROUP BY <dimensions>]
            [ORDER BY <order_clause>]
            [LIMIT <limit>]

<metrics> ::= <metric> [, <metric>]*
<metric> ::= 指标 (<metric_name>) | 聚合函数 (<metric_name>)

<conditions> ::= <condition> [AND <condition>]*
<condition> ::= 维度 (<dim_name>, <op>, <value>)
              | 指标 (<metric_name>, <op>, <value>)
              | <condition> <logic_op> <condition>

<op> ::= = | != | > | < | >= | <= | BETWEEN | IN | LIKE
<logic_op> ::= AND | OR

<dimensions> ::= <dimension> [, <dimension>]*
<dimension> ::= 维度 (<dim_name>)

<order_clause> ::= <metric> [ASC | DESC]
<limit> ::= <number>
```

### 2. DSL 示例

**简单查询：**
```
SELECT 指标 (销售额)
WHERE 维度 (地区，=，华东)
  AND 维度 (时间，=，2024-Q1)
```

**分组聚合：**
```
SELECT 指标 (销售额), 指标 (订单量)
WHERE 维度 (时间，BETWEEN，2024-01-01, 2024-12-31)
GROUP BY 维度 (城市)
ORDER BY 指标 (销售额) DESC
LIMIT 100
```

**复杂条件：**
```
SELECT 指标 (GMV), 指标 (用户数)
WHERE (维度 (平台，=，APP) OR 维度 (平台，=，Web))
  AND 维度 (用户等级，IN，["VIP", "黄金"])
  AND 指标 (消费金额，>=，1000)
GROUP BY 维度 (平台), 维度 (用户等级)
```

---

## 📐 解析器设计

### 1. 词法分析 (Lexer)

**Token 类型：**
```
KEYWORD: SELECT, WHERE, GROUP, BY, ORDER, LIMIT, AND, OR
IDENTIFIER: 指标，维度，函数名
STRING: "华东", '2024-Q1'
NUMBER: 100, 1000
OPERATOR: =, !=, >, <, >=, <=, BETWEEN, IN, LIKE
PUNCTUATION: (, ), ,, [, ]
```

**实现方式：**
- 正则表达式匹配
- 状态机处理
- 支持自定义分隔符

### 2. 语法分析 (Parser)

**语法规则 (EBNF))：**
```
使用 ANTLR4 或 PLY 构建解析器
生成抽象语法树 (AST)
```

**AST 节点类型：**
```
SelectNode
  ├── metrics: [MetricNode]
  ├── where: ConditionNode (optional)
  ├── groupBy: [DimensionNode] (optional)
  ├── orderBy: OrderNode (optional)
  └── limit: NumberNode (optional)

MetricNode
  ├── name: string
  └── aggregation: string (optional)

ConditionNode
  ├── left: ExpressionNode
  ├── operator: string
  └── right: ValueNode
```

### 3. 语义校验

**校验规则：**
1. **指标存在性** - 指标必须在语义层注册
2. **维度合法性** - 关系校验
3. **类型匹配** - 条件值与维度类型匹配
4. **权限检查** - 用户是否有数据访问权限

**校验流程：**
```
AST
  ↓
符号表查询
  ↓
规则引擎校验
  ↓
通过/失败 + 详细错误信息
```

---

## ⚡ 查询优化器

### 1. 谓词下推 (Predicate Pushdown)

**优化前：**
```sql
SELECT * FROM (
  SELECT user_id, order_amount FROM orders WHERE status = 'completed'
) t
WHERE order_amount > 1000
```

**优化后：**
```sql
SELECT user_id, order_amount
FROM orders
WHERE status = 'completed' AND order_amount > 1000
```

### 2. 列裁剪 (Column Pruning)

**优化前：**
```sql
SELECT * FROM users WHERE age > 18
```

**优化后：**
```sql
SELECT user_id, age FROM users WHERE age > 18
```

### 3. 连接优化 (Join Optimization)

**优化策略：**
- 小表驱动大表
- 广播连接 vs Shuffle 连接
- 连接顺序重排

### 4. 聚合下推

**优化前：**
```sql
SELECT region, SUM(amount)
FROM (
  SELECT region, amount FROM orders WHERE date >= '2024-01-01'
)
GROUP BY region
```

**优化后：**
```sql
SELECT region, SUM(amount)
FROM orders
WHERE date >= '2024-01-01'
GROUP BY region
```

---

## 🔌 SQL 生成器

### 1. 方言适配

**支持的 SQL 方言：**
- Hive SQL
- MySQL
- Presto/Trino
- PostgreSQL
- Oracle

**方言差异处理：**
```
日期函数：
  - Hive: from_unixtime(), unix_timestamp()
  - MySQL: FROM_UNIXTIME(), UNIX_TIMESTAMP()
  - Presto: from_unixtime(), to_unixtime()

字符串函数：
  - Hive: concat(), substr()
  - MySQL: CONCAT(), SUBSTRING()
  - Presto: concat(), substr()

聚合函数：
  - 标准 SQL: COUNT(), SUM(), AVG()
  - Hive: COUNT(), SUM(), AVG(), COLLECT_LIST()
```

### 2. 模板引擎

**模板示例：**
```
SELECT
{{#metrics}}
  {{metric_mapping}} AS {{metric_alias}}{{#has_next}},{{/has_next}}
{{/metrics}}
FROM {{table}}
{{#where}}
WHERE {{where_clause}}
{{/where}}
{{#groupBy}}
GROUP BY {{group_clause}}
{{/groupBy}}
{{#orderBy}}
ORDER BY {{order_clause}}
{{/orderBy}}
{{#limit}}
LIMIT {{limit_value}}
{{/limit}}
```

### 3. SQL 生成流程

```
AST
  ↓
中间表示 (IR)
  ↓
优化规则应用
  ↓
方言适配
  ↓
模板渲染
  ↓
格式化输出
  ↓
SQL 字符串
```

---

## 📊 性能优化

### 1. 缓存策略

**AST 缓存：**
- 相同 DSL 结构复用 AST
- LRU 缓存，容量 10000

**SQL 缓存：**
- 参数化 SQL 缓存
- 结果集缓存（可选）

### 2. 并行处理

**多查询并行：**
- 独立 DSL 查询并行解析
- 线程池管理

**AST 遍历并行：**
- 大型 AST 分片处理

### 3. 增量编译

**变更检测：**
- DSL 差异分析
- 仅重新编译变更部分

---

## 🔍 错误处理

### 1. 错误类型

| 错误类型 | 描述 | 处理方式 |
|----------|------|----------|
| 语法错误 | DSL 语法不合法 | 返回错误位置 + 建议 |
| 语义错误 | 指标/维度不存在 | 推荐相似实体 |
| 权限错误 | 无数据访问权限 | 提示申请权限 |
| 优化失败 | 查询无法优化 | 降级处理 |
| 生成失败 | SQL 生成异常 | 回滚 + 告警 |

### 2. 错误码设计

```
DSL_PARSE_ERROR (1001-1999)
DSL_SEMANTIC_ERROR (2001-2999)
SQL_GENERATION_ERROR (3001-3999)
OPTIMIZATION_ERROR (4001-4999)
PERMISSION_ERROR (5001-5999)
```

### 3. 用户友好提示

```
错误：指标"销售金额"不存在
建议：
  - 您是否想查询"销售额"？
  - 或"订单金额"？
  - 查看指标词典：[链接]
```

---

## 📈 质量保障

### 1. 单元测试

- 解析器测试覆盖率 > 90%
- 生成器测试覆盖率 > 85%
- 优化器测试覆盖率 > 80%

### 2. 集成测试

- 端到端 DSL→SQL 测试
- 多方言兼容性测试
- 性能基准测试

### 3. 回归测试

- 历史用例回归
- 边界条件测试
- 异常场景测试

---

## 🚀 实施计划

### Phase 1: 基础解析 (M3)
- DSL 语法设计
- 解析器开发
- 基础校验

### Phase 2: SQL 生成 (M4)
- 模板引擎
- 方言适配
- 基础优化

### Phase 3: 高级优化 (M5)
- 查询优化器
- 缓存机制
- 性能调优

### Phase 4: 生产验证 (M6)
- 试点运行
- 问题修复
- 全量上线

---

*最后更新：2026-04-23*
*版本：v1.0*
