---
name: c-drive-cleanup
description: Scan and clean up C drive disk space on Windows. Use when the user asks to check disk usage, free up C drive space, clean disk, or mentions C盘清理 or 空间不足. Scans folders recursively, identifies large files and folders, and asks for user confirmation before deletion.
version: 1.0.0
---

# C 盘清理工作流

## 核心原则

- **删除前必须询问用户确认**，不能自动删除任何文件或文件夹
- 只关注 **超过 1 GB** 的项目，忽略小文件
- 扫描要穿透到子目录，展示层级结构，让用户看清空间去向

## 第一步：扫描 C 盘一级目录

使用 PowerShell 脚本扫描 C:\ 下每个一级目录的大小。注意：必须写入 .ps1 文件再执行，避免 cmd 转义 $ 符号导致报错。

```powershell
$folders = Get-ChildItem -Path 'C:\' -Directory -Force -ErrorAction SilentlyContinue
$results = @()
foreach ($folder in $folders) {
    $size = 0
    try {
        $size = (Get-ChildItem -Path $folder.FullName -Recurse -Force -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum -ErrorAction SilentlyContinue).Sum
    } catch { $size = 0 }
    if ($null -eq $size) { $size = 0 }
    $results += [PSCustomObject]@{
        Folder = $folder.Name
        SizeGB = [math]::Round($size / 1GB, 2)
        SizeMB = [math]::Round($size / 1MB, 0)
    }
}
$results | Sort-Object SizeGB -Descending | Format-Table -AutoSize
```

## 第二步：逐层穿透扫描

对每个超过 1 GB 的目录继续向下扫描子目录，直到找到空间去向。重点关注：

- C:\Users\{用户名}\AppData\Local — 应用缓存和更新包
- C:\Users\{用户名}\AppData\Roaming — 应用数据和配置
- C:\Users\{用户名}\Documents — 文档和聊天缓存
- C:\Users\{用户名}\Desktop — 桌面大文件
- C:\Users\{用户名}\ 下以 . 开头的隐藏文件夹
- C:\Windows — 系统文件
- C:\Program Files 和 C:\Program Files (x86) — 已安装程序

穿透扫描通用模板：

```powershell
function Scan-Folder($path, $depth, $maxDepth) {
    if ($depth -gt $maxDepth) { return }
    $indent = "  " * $depth
    $folders = Get-ChildItem -Path $path -Directory -Force -ErrorAction SilentlyContinue
    foreach ($folder in $folders) {
        $size = 0
        try {
            $size = (Get-ChildItem -Path $folder.FullName -Recurse -Force -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum -ErrorAction SilentlyContinue).Sum
        } catch { $size = 0 }
        if ($null -eq $size) { $size = 0 }
        if ($size -gt 1GB) {
            $sizeGB = [math]::Round($size / 1GB, 2)
            Write-Host "$indent[$($sizeGB) GB] $($folder.FullName)"
            Scan-Folder $folder.FullName ($depth + 1) $maxDepth
        }
    }
}
```

## 第三步：查找大文件

扫描 C 盘所有超过 1 GB 的单个文件：

```powershell
Get-ChildItem -Path 'C:\' -Recurse -File -Force -ErrorAction SilentlyContinue |
    Where-Object { $_.Length -gt 1GB } |
    ForEach-Object {
        [PSCustomObject]@{
            SizeGB = [math]::Round($_.Length / 1GB, 2)
            FileName = $_.Name
            FullPath = $_.FullName
        }
    } | Sort-Object SizeGB -Descending | Format-Table -AutoSize
```

常见系统大文件说明：

- pagefile.sys — 虚拟内存，系统管理，不建议手动删
- hiberfil.sys — 休眠文件，关闭休眠可释放（powercfg /hibernate off）
- swapfile.sys — UWP 交换文件

## 第四步：汇总报告并询问用户

将扫描结果按层级结构整理成报告，标注每项的性质和清理风险：

- 缓存类：pip cache、npm cache、浏览器缓存等，无风险可删
- 更新包类：各应用的 updater 目录、upgrade 目录，旧版本可删
- 崩溃报告类：Crashpad/reports、CrashDumps 等，无风险可删
- 应用数据类：聊天缓存、编辑器数据等，删除后丢失聊天记录或配置
- 系统文件类：WinSxS、DriverStore 等，需用系统工具清理
- 用户文件类：桌面上的 PDF、文档等，需用户自行判断

**必须用 AskUserQuestion 工具或明确文字询问用户要删除哪些项目，得到确认后再执行。**

## 第五步：执行删除

用户确认后，使用 Remove-Item 删除（不经过回收站）：

```powershell
Remove-Item -Path $targetPath -Recurse -Force -ErrorAction SilentlyContinue
```

删除后验证目录是否已不存在：

```powershell
if (Test-Path $targetPath) {
    Write-Host "FAILED: $targetPath still exists"
} else {
    Write-Host "OK: $targetPath deleted"
}
```

## 第六步：报告结果

删除完成后汇报：每项删除结果（成功或失败）、本轮释放空间、累计释放空间、当前 C 盘可用空间。

查看 C 盘空间：

```powershell
$drive = Get-PSDrive C
$usedGB = [math]::Round($drive.Used / 1GB, 2)
$freeGB = [math]::Round($drive.Free / 1GB, 2)
$totalGB = [math]::Round(($drive.Used + $drive.Free) / 1GB, 2)
Write-Host "Total: $totalGB GB | Used: $usedGB GB | Free: $freeGB GB"
```

## 常见可安全清理的项目

- pip 缓存：路径 %LOCALAPPDATA%\pip\cache，命令 pip cache purge
- npm 缓存：路径 %LOCALAPPDATA%\npm-cache，命令 npm cache clean --force
- 回收站：Clear-RecycleBin -Force
- VS Code 扩展缓存：%APPDATA%\Code\CachedExtensionVSIXs，直接删除目录
- VS Code Cline 扩展数据：%APPDATA%\Code\User\globalStorage\*cline*，直接删除目录
- 浏览器崩溃报告：Crashpad\reports 目录，直接删除
- 应用更新缓存：*-updater、upgrade 目录，直接删除
- Windows 事件日志：C:\Windows\System32\winevt\Logs\*.evtx，可删除旧日志
- 联想驱动缓存：C:\Windows\LVUAAgentInstBaseRoot，直接删除

## 注意事项

- PowerShell 脚本务必写成 .ps1 文件再执行，不要内联在命令行中（cmd 会转义 $ 符号导致语法错误）
- 扫描大型目录时设置较长的 timeout（如 600000ms）
- 系统目录（WinSxS、DriverStore）不要直接删除，建议用 Dism.exe /Online /Cleanup-Image /StartComponentCleanup 清理
- 如果应用正在运行，其目录可能被锁定导致删除失败，提示用户先关闭应用
