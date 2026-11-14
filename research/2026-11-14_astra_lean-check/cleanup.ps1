$ErrorActionPreference = 'Stop'
$taskCloneRoot = [System.IO.Path]::GetFullPath('E:\lb2')
if ($taskCloneRoot -cne 'E:\lb2') { throw 'Unexpected cleanup target' }
$taskCloneItem = Get-Item -LiteralPath $taskCloneRoot
if (($taskCloneItem.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0) { throw 'Clone root is a reparse point' }
$taskCloneHead = git -C $taskCloneRoot rev-parse HEAD
if ($taskCloneHead -ne '4eaee87548250b2682affda7d05d947c05554bae') { throw 'Unexpected clone HEAD' }
Write-Output "Verified cleanup target: $taskCloneRoot, HEAD $taskCloneHead"
Write-Output "Started: $(Get-Date -Format o)"
Remove-Item -LiteralPath $taskCloneRoot -Recurse -Force
Write-Output "Clone exists after cleanup: $(Test-Path -LiteralPath $taskCloneRoot)"
Write-Output "Preserved cache exists: $(Test-Path -LiteralPath 'E:\lbb')"
Write-Output "Finished: $(Get-Date -Format o)"
