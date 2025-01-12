#!/usr/bin/pwsh

function GetPythonCommand {
    if (Get-Command python3 -ErrorAction SilentlyContinue) {
        return "python3"
    } elseif (Get-Command python -ErrorAction SilentlyContinue) {
        return "python"
    } elseif (Get-Command py -ErrorAction SilentlyContinue) {
        return "py"
    } else {
        Write-Error "Python não encontrado no sistema."
        exit 1
    }
}
function Run-Benchmark-And-Store-Output-By-InstanceFile {
    param (
        [string]$OutputDir,
        [string]$InstancesDir,
        [string]$StartNode,
        [float]$GraspAlpha,
        [int]$GraspMaxIt
    )

    # Define local search methods
    $searchMethods = @("ls2opt", "vndtsr", "vndtrs", "vndstr", "vndsrt", "vndrts", "vndrst", "cstsr")

    # Create directories for each search method
    foreach ($method in $searchMethods) {
        New-Item -ItemType Directory -Force -Path (Join-Path $OutputDir $method) | Out-Null
    }
    $python_command = GetPythonCommand
    $NullDevice = if ($IsWindows) { "NUL" } else { "/dev/null" }

    # Loop through instance files and process each
    Get-ChildItem -Path $InstancesDir | ForEach-Object {
        $file = $_.Name
        Write-Output "Running instance: $file"

        foreach ($method in $searchMethods) {
            Write-Output "Running $method local search"
            $ResultFile = [IO.Path]::Combine($OutputDir, $method, "results.txt")
            $InputFile = [IO.Path]::Combine($InstancesDir, $file)
            $WithVnd = if ($method.Contains("vnd")) { "true" } else { "false" }
            Invoke-Expression "$python_command main.py $InputFile $ResultFile $StartNode grasp --grasp-max-it $GraspMaxIt --grasp-alpha $GraspAlpha --with-vnd $WithVnd > $NullDevice 2>&1"
        }
    }
}

function Show-Help {
    param ([int]$ExitCode = 0)

    Write-Output "Usage: ./script.ps1 <OutputDir> <InstancesDir> <StartNode> <GraspAlpha> <GraspMaxIt>"
    Write-Output "Arguments:"
    Write-Output "  OutputDir: Directory to save the results"
    Write-Output "  InstancesDir: Directory containing instance files"
    Write-Output "  StartNode: Starting node for heuristics"
    Write-Output "  GraspAlpha: Alpha parameter for GRASP"
    Write-Output "  GraspMaxIt: Maximum number of iterations for GRASP"
    exit $ExitCode
}

function Main {
    param (
        [string]$OutputDir,
        [string]$InstancesDir,
        [string]$StartNode,
        [float]$GraspAlpha,
        [int]$GraspMaxIt
    )

    if ($OutputDir -eq "-h") {
        Show-Help 0
        return
    }
    if (!$OutputDir -or !$InstancesDir -or !$StartNode -or !$GraspAlpha -or !$GraspMaxIt) {
        Show-Help 1
        return
    }

    Run-Benchmark-And-Store-Output-By-InstanceFile -OutputDir $OutputDir -InstancesDir $InstancesDir -StartNode $StartNode -GraspAlpha $GraspAlpha -GraspMaxIt $GraspMaxIt
}

Main @args