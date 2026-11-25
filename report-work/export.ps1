param([string]$InputDoc,[string]$OutputPdf,[switch]$Refresh)
$InputDoc = (Resolve-Path -LiteralPath $InputDoc).Path
$OutputPdf = $OutputPdf.Replace('/','\')
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {
 $doc = $word.Documents.Open($InputDoc,$false,(-not $Refresh.IsPresent))
 if ($Refresh) { $doc.Fields.Update() | Out-Null; foreach ($toc in $doc.TablesOfContents) { $toc.Update() }; $doc.Repaginate(); $doc.Save() }
 $doc.ExportAsFixedFormat($OutputPdf,17)
 Write-Output "Pages: $($doc.ComputeStatistics(2))"
 $doc.Close(0)
} finally { $word.Quit() }
