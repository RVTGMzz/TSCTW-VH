param([switch]$Restore, [string]$GameRoot)
$ErrorActionPreference = 'Stop'
function Hash($p) { (Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash.ToLowerInvariant() }
try {
 if (Get-Process SimsCS -ErrorAction SilentlyContinue) { throw 'Hay tat game truoc khi cai hoac go ban thu.' }
 if (!$GameRoot) {
  foreach ($candidate in @($PSScriptRoot, (Split-Path $PSScriptRoot -Parent), (Split-Path (Split-Path $PSScriptRoot -Parent) -Parent), 'G:\Castaway-Portable')) {
   if (Test-Path -LiteralPath (Join-Path $candidate 'TSBin\SimsCS.exe')) { $GameRoot=$candidate; break }
  }
 }
 if (!$GameRoot) {
  Add-Type -AssemblyName System.Windows.Forms
  $dlg=New-Object System.Windows.Forms.FolderBrowserDialog
  $dlg.Description='Chon thu muc Castaway co TSBin va TSData'
  if ($dlg.ShowDialog() -ne 'OK') { throw 'Chua chon thu muc game.' }
  $GameRoot=$dlg.SelectedPath
 }
 if (!(Test-Path -LiteralPath (Join-Path $GameRoot 'TSBin\SimsCS.exe'))) { throw 'Sai thu muc game.' }
 $GameRoot=(Resolve-Path -LiteralPath $GameRoot).Path
 $backup=Join-Path $GameRoot 'VietHoa\Backups\v06'
 $state=Join-Path $backup 'state.json'
 $items = ConvertFrom-Json -InputObject (Get-Content -LiteralPath (Join-Path $PSScriptRoot 'manifest.json') -Raw)
 foreach ($entry in $items) {
  if ($entry.path -isnot [string] -or [string]::IsNullOrWhiteSpace($entry.path)) { throw 'Danh sach file khong hop le.' }
 }
 function RestoreFiles {
  foreach ($it in $items) {
   $target=Join-Path $GameRoot $it.path
   if ($it.original) {
    Copy-Item -LiteralPath (Join-Path $backup $it.path) -Destination $target -Force
   } elseif (Test-Path -LiteralPath $target) { Remove-Item -LiteralPath $target -Force }
  }
 }
 if ($Restore) {
  if (!(Test-Path -LiteralPath $state)) { throw 'Khong tim thay ban sao luu cua ban thu nay.' }
  $saved = ConvertFrom-Json -InputObject (Get-Content -LiteralPath $state -Raw)
  if (($saved | ConvertTo-Json -Depth 5 -Compress) -ne ($items | ConvertTo-Json -Depth 5 -Compress)) { throw 'Ban sao luu khong khop phien ban.' }
  $saved = ConvertFrom-Json -InputObject (Get-Content -LiteralPath $state -Raw)
  if (($saved | ConvertTo-Json -Depth 5 -Compress) -ne ($items | ConvertTo-Json -Depth 5 -Compress)) { throw 'Ban sao luu khong khop phien ban.' }
  foreach ($it in $items) {
   if ($it.original -and ((Hash (Join-Path $backup $it.path)) -ne $it.original)) { throw 'Ban sao luu bi thay doi. Dung khoi phuc.' }
   $target=Join-Path $GameRoot $it.path
   if (Test-Path -LiteralPath $target) {
    $h=Hash $target
    if ($h -ne $it.patched -and $h -ne $it.original) { throw "File da duoc sua boi ban khac: $($it.path). Dung de tranh ghi de." }
   }
  }
  RestoreFiles
  Write-Host 'Da quay ve ban chu truoc v06 (Text05). Font duoc giu nguyen.' -ForegroundColor Green
 } else {
  foreach ($it in $items) {
   $src=Join-Path (Join-Path $PSScriptRoot 'Payload') $it.path
   if ((Hash $src) -ne $it.patched) { throw "Goi cai bi loi: $($it.path)" }
   $target=Join-Path $GameRoot $it.path
   if (Test-Path -LiteralPath $target) {
    $h=Hash $target
    if ($h -ne $it.original -and !($h -eq $it.patched -and (Test-Path -LiteralPath $state))) { throw "Can ban Text05 dang chay on, file khong khop: $($it.path)" }
   } elseif ($it.original) { throw "Thieu file game: $($it.path)" }
  }
  if (!(Test-Path -LiteralPath $state)) {
   foreach ($it in $items) {
    if ($it.original) {
     $dest=Join-Path $backup $it.path
     New-Item -ItemType Directory -Path (Split-Path $dest -Parent) -Force | Out-Null
     $sourceOriginal=Join-Path $GameRoot $it.path
     if ((Hash $sourceOriginal) -ne $it.original) { throw 'Khong tim thay ban chu goc hop le. Dung cai dat.' }
     Copy-Item -LiteralPath $sourceOriginal -Destination $dest -Force
     if ((Hash $dest) -ne $it.original) { throw 'Sao luu khong thanh cong.' }
    }
   }
   $items | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $state -Encoding UTF8
  }
  $saved = ConvertFrom-Json -InputObject (Get-Content -LiteralPath $state -Raw)
  if (($saved | ConvertTo-Json -Depth 5 -Compress) -ne ($items | ConvertTo-Json -Depth 5 -Compress)) { throw 'Ban sao luu khong khop phien ban.' }
  foreach ($it in $items) {
   if ($it.original -and ((Hash (Join-Path $backup $it.path)) -ne $it.original)) { throw 'Ban sao luu khong hop le.' }
  }
  try {
   foreach ($it in $items) {
    $target=Join-Path $GameRoot $it.path
    Copy-Item -LiteralPath (Join-Path (Join-Path $PSScriptRoot 'Payload') $it.path) -Destination $target -Force
    if ((Hash $target) -ne $it.patched) { throw "Ghi file that bai: $($it.path)" }
   }
  } catch { RestoreFiles; throw }
  Write-Host 'Da cai chu v06.' -ForegroundColor Green
  try {
   $manager=Join-Path $GameRoot 'VietHoa\v06'
   New-Item -ItemType Directory -Path $manager -Force | Out-Null
   foreach ($name in @('Setup.ps1','manifest.json','GO-BAN-DICH06.cmd','HUONG-DAN.txt')) {
    $from=Join-Path $PSScriptRoot $name
    $to=Join-Path $manager $name
    if ([IO.Path]::GetFullPath($from) -ne [IO.Path]::GetFullPath($to)) { Copy-Item -LiteralPath $from -Destination $to -Force }
   }
   Write-Host 'Go v06: chay VietHoa\v06\GO-BAN-DICH06.cmd. Giu ban sao luu de co the quay lai v05.' -ForegroundColor Green
  } catch { Write-Warning ('Ban dich da cai, nhung chua don xong: ' + $_.Exception.Message) }
 }
 Write-Host "Thu muc game: $GameRoot"
} catch {
 Write-Host $_.Exception.Message -ForegroundColor Red
 Write-Host ('Dong loi: ' + $_.InvocationInfo.ScriptLineNumber)
 Write-Host $_.InvocationInfo.Line
 exit 1
}
