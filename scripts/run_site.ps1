param(
  [int]$StartPort = 8080
)

$ErrorActionPreference = 'Stop'
$RootDir = Split-Path -Parent $PSScriptRoot

function Get-PythonCommand {
  if (Get-Command py -ErrorAction SilentlyContinue) {
    return @('py', '-3')
  }
  if (Get-Command python -ErrorAction SilentlyContinue) {
    return @('python')
  }
  if (Get-Command python3 -ErrorAction SilentlyContinue) {
    return @('python3')
  }
  throw 'No Python interpreter found (py/python/python3).'
}

function Test-PortInUse {
  param([int]$Port)

  try {
    $listener = [System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Loopback, $Port)
    $listener.Start()
    $listener.Stop()
    return $false
  } catch {
    return $true
  }
}

function Get-FreePort {
  param([int]$Port)

  for ($i = 0; $i -lt 200; $i++) {
    $candidate = $Port + $i
    if (-not (Test-PortInUse -Port $candidate)) {
      return $candidate
    }
  }

  throw "Unable to find free port from $Port."
}

$pythonCmd = Get-PythonCommand
$pythonExe = $pythonCmd[0]
$pythonArgs = @()
if ($pythonCmd.Length -gt 1) {
  $pythonArgs = $pythonCmd[1..($pythonCmd.Length - 1)]
}

$port = Get-FreePort -Port $StartPort
$buildScript = Join-Path $RootDir 'scripts/build_site.py'
$siteDir = Join-Path $RootDir 'site'

& $pythonExe @pythonArgs $buildScript

Write-Host "Serving site at http://127.0.0.1:$port using $($pythonCmd -join ' ')"
& $pythonExe @pythonArgs (Join-Path $RootDir 'scripts/serve_site.py') --host 127.0.0.1 --port $port --site-dir $siteDir
