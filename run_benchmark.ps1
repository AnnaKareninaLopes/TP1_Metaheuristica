#!/usr/bin/pwsh


function Run-Benchmark {
    param (
        [string]$OutputDir,
        [string]$InstancesDir,
        [string]$StartNode
    )

    # Create output directory if not exists
    New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null

    # Loop through instance files and process each
    Get-ChildItem -Path $InstancesDir | ForEach-Object {
        $file = $_.Name
        Write-Output "Running instance: $file"

        $InstanceDir = Join-Path $OutputDir ($file -replace '\..+$')
        New-Item -ItemType Directory -Force -Path $InstanceDir | Out-Null

        # Define heuristics
        $heuristics = @("agm", "nn", "ci")

        foreach ($heuristic in $heuristics) {
            Write-Output "Running $heuristic heuristic"
            $ResultFile = "$InstanceDir\result.$file.$heuristic.txt"
            python3 main.py "$InstancesDir\$file" $ResultFile $heuristic $StartNode > $null 2>&1
        }
    }
}

function Run-Benchmark-And-Store-Output-By-InstanceFile {
    param (
        [string]$OutputDir,
        [string]$InstancesDir,
        [string]$StartNode
    )

    # Define local search methods
    $searchMethods = @("ls2opt", "vndtsr", "vndtrs", "vndstr", "vndsrt", "vndrts", "vndrst", "cstsr")

    # Create directories for each search method
    foreach ($method in $searchMethods) {
        New-Item -ItemType Directory -Force -Path (Join-Path $OutputDir $method) | Out-Null
    }

    # Loop through instance files and process each
    Get-ChildItem -Path $InstancesDir | ForEach-Object {
        $file = $_.Name
        Write-Output "Running instance: $file"

        foreach ($method in $searchMethods) {
            Write-Output "Running $method local search"
            $ResultFile = "$OutputDir\$method\results.txt"
            python3 main.py "$InstancesDir\$file" $ResultFile $StartNode --local-search $method > $null 2>&1
        }
    }
}

function Show-Help {
    param ([int]$ExitCode = 0)

    Write-Output "Usage: ./script.ps1 <OutputDir> <InstancesDir> <StartNode>"
    Write-Output "Arguments:"
    Write-Output "  OutputDir: Directory to save the results"
    Write-Output "  InstancesDir: Directory containing instance files"
    Write-Output "  StartNode: Starting node for heuristics"
    exit $ExitCode
}

function Main {
    param (
        [string]$OutputDir,
        [string]$InstancesDir,
        [string]$StartNode
    )

    if ($OutputDir -eq "-h") {
        Show-Help 0
        return
    }

    if (!$OutputDir -or !$InstancesDir -or !$StartNode) {
        Show-Help 1
        return
    }

    Run-Benchmark-And-Store-Output-By-InstanceFile -OutputDir $OutputDir -InstancesDir $InstancesDir -StartNode $StartNode
}

Main @args