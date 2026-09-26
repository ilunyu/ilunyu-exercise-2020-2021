# 开发与发布规范

仓库长期保留 `dev` 与 `main` 两个分支。`dev` 用于日常新增、修订和校对题目；`main` 保存已经正式发布、可供应用安装的版本。

日常工作直接提交到 `dev`。准备发布时，在 `dev` 中更新 `resource.json`：`versionName` 使用语义化版本，`versionCode` 在每次发布时严格递增。随后创建 `dev → main` Pull Request。

Pull Request 会校验题目、资源元数据、版本递增和资源包构建。合并到 `main` 后，GitHub Actions 自动创建 `v<versionName>` 标签和同名 GitHub Release。年度题库仓库的 Release 同时包含 `resource.ilunyupack`、`release.json` 和 SHA-256 文件。

`main` 应启用分支保护：禁止直接推送和强制推送，要求通过 Pull Request，并要求资源校验工作流通过。仓库默认分支设为 `dev`。

模板仓库没有根目录正式题目，因此其 Release 只记录模板版本；由模板创建的年度题库仓库在加入正式题目后自动发布可安装资源包。
