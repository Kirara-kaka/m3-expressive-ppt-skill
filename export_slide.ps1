param(
    [string]$PptxPath,
    [string]$PngPath,
    [string]$OutputDir
)

$ppt = New-Object -ComObject PowerPoint.Application
try {
    # Open(FileName, ReadOnly, Untitled, WithWindow)
    $presentation = $ppt.Presentations.Open($PptxPath, 2, 0, 0)
    
    if ($OutputDir) {
        if (-not (Test-Path $OutputDir)) {
            New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
        }
        $count = $presentation.Slides.Count
        for ($i = 1; $i -le $count; $i++) {
            $outPath = Join-Path $OutputDir ("slide_{0}.png" -f $i)
            $presentation.Slides.Item($i).Export($outPath, "PNG", 1920, 1080)
            Write-Host "Exported slide $i to $outPath"
        }
        Write-Host "SUCCESS: Exported all $count slides to $OutputDir"
    } elseif ($PngPath) {
        $presentation.Slides.Item(1).Export($PngPath, "PNG", 1920, 1080)
        Write-Host "SUCCESS: Exported to $PngPath"
    }
    $presentation.Close()
} catch {
    Write-Error $_
} finally {
    $ppt.Quit()
    [System.GC]::Collect()
}
