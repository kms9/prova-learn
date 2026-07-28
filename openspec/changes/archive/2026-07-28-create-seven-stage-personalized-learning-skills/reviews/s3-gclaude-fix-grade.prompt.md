你是独立、只读、严格的 Skill Eval grader。cwd=/Users/logo/self_repo/learn_case/auto_learn。

读取：
- `.agents/skills/build-capability-concept-graph/evals/evals.json` 中 `id=3` 的六条 `expectations`
- `openspec/changes/create-seven-stage-personalized-learning-skills/reviews/s3-gclaude-fix-eval.outer.json` 的 `.result`（这是待评分输出）

不要读取 example.md，不要修改任何文件，不要把未写出的事实推断为已满足。

逐条判断六条 expectation。结果本身必须是一个 JSON 对象，不得在 JSON 前后输出解释或 Markdown fence，形状严格为：

{
  "audit_id": "s3-gclaude-fix-grade",
  "expectation_results": [
    {
      "expectation": "<逐字复制 expectation>",
      "passed": true,
      "evidence": "<短证据>"
    }
  ],
  "summary": {
    "passed": 0,
    "failed": 0,
    "total": 6,
    "pass_rate": 0.0
  },
  "overall_passed": true,
  "blocking_findings": [],
  "major_findings": [],
  "minor_findings": []
}
